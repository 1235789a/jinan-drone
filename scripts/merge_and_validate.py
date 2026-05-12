"""
Day 1 工具: 合并 raw_responses.jsonl 和 labels (从 Meta-Judge 收集的 JSON)，
进行数据质量验证，输出最终的 labeled_train.jsonl。

使用:
    python scripts/merge_and_validate.py
    
输入:
    data/raw_responses.jsonl       (三模型回答)
    data/judge_batches/outputs/    (Meta-Judge 输出的 txt 文件)
    data/judge_batches/inputs/*_ids.json  (ID 映射)

输出:
    data/labeled_train.jsonl       (最终标注数据)
    data/stats.json                (分布统计)
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"
JUDGE_INPUTS_DIR = Path(__file__).parent.parent / "data" / "judge_batches" / "inputs"
JUDGE_OUTPUTS_DIR = Path(__file__).parent.parent / "data" / "judge_batches" / "outputs"
LABELED_PATH = Path(__file__).parent.parent / "data" / "labeled_train.jsonl"
STATS_PATH = Path(__file__).parent.parent / "data" / "stats.json"


def parse_judge_output(text: str) -> list[dict]:
    """从 Meta-Judge 的文本输出中提取 JSON lines"""
    labels = []
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
            # Validate required fields
            required = ["group", "hallucination_risk", "semantic_contradiction",
                        "uncertainty_signals", "final_risk_level"]
            if all(k in obj for k in required):
                labels.append(obj)
        except json.JSONDecodeError:
            continue
    return labels


def collect_all_labels() -> dict[int, dict]:
    """收集所有 Meta-Judge 输出，按 record_id 索引"""
    id_to_label = {}
    
    if not JUDGE_OUTPUTS_DIR.exists():
        print(f"ERROR: {JUDGE_OUTPUTS_DIR} not found", file=sys.stderr)
        sys.exit(1)
    
    output_files = sorted(JUDGE_OUTPUTS_DIR.glob("judge_batch_*_output.txt"))
    print(f"Found {len(output_files)} judge output files")
    
    for out_file in output_files:
        # Match corresponding ids file
        match = re.search(r"judge_batch_(\d+)_output", out_file.name)
        if not match:
            continue
        batch_num = match.group(1)
        ids_file = JUDGE_INPUTS_DIR / f"judge_batch_{batch_num}_ids.json"
        
        if not ids_file.exists():
            print(f"  ⚠️  Missing IDs file for batch {batch_num}, skipping")
            continue
        
        ids = json.loads(ids_file.read_text(encoding="utf-8"))
        text = out_file.read_text(encoding="utf-8")
        labels = parse_judge_output(text)
        
        # Align labels (group N) with record IDs
        for label in labels:
            group_idx = label["group"] - 1  # groups are 1-indexed
            if 0 <= group_idx < len(ids):
                record_id = ids[group_idx]
                id_to_label[record_id] = label
    
    return id_to_label


def validate_label(label: dict) -> bool:
    """基本校验"""
    try:
        for field in ["hallucination_risk", "semantic_contradiction", "uncertainty_signals"]:
            val = label[field]
            if not isinstance(val, int) or val < 0 or val > 10:
                return False
        if label["final_risk_level"] not in ["low", "medium", "high"]:
            return False
        return True
    except (KeyError, TypeError):
        return False


def main():
    # Load raw responses
    raw = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                raw.append(json.loads(line))
    print(f"Loaded {len(raw)} raw responses")
    
    # Collect labels
    id_to_label = collect_all_labels()
    print(f"Collected {len(id_to_label)} labels")
    
    # Merge
    merged = []
    skipped_no_label = 0
    skipped_invalid = 0
    
    for record in raw:
        label = id_to_label.get(record["id"])
        if not label:
            skipped_no_label += 1
            continue
        if not validate_label(label):
            skipped_invalid += 1
            continue
        
        merged.append({
            **record,
            "judgment": {
                "hallucination_risk": label["hallucination_risk"],
                "semantic_contradiction": label["semantic_contradiction"],
                "uncertainty_signals": label["uncertainty_signals"],
                "final_risk_level": label["final_risk_level"],
                "reasoning": label.get("reasoning", ""),
            }
        })
    
    # Write labeled data
    LABELED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LABELED_PATH, "w", encoding="utf-8") as f:
        for item in merged:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    # Compute stats
    levels = Counter(m["judgment"]["final_risk_level"] for m in merged)
    domains = Counter(m["domain"] for m in merged)
    langs = Counter(m["lang"] for m in merged)
    
    domain_level_dist = {}
    for m in merged:
        d = m["domain"]
        lv = m["judgment"]["final_risk_level"]
        domain_level_dist.setdefault(d, Counter())[lv] += 1
    
    total = len(merged)
    stats = {
        "total_samples": total,
        "skipped_no_label": skipped_no_label,
        "skipped_invalid_label": skipped_invalid,
        "level_distribution": dict(levels),
        "level_percentage": {k: round(v / total * 100, 1) for k, v in levels.items()} if total else {},
        "domain_distribution": dict(domains),
        "language_distribution": dict(langs),
        "domain_level_cross": {k: dict(v) for k, v in domain_level_dist.items()},
        "quality_check": {
            "balanced": all(15 <= v / total * 100 <= 55 for v in levels.values()) if total else False,
            "min_class_pct": min(v / total * 100 for v in levels.values()) if total else 0,
            "max_class_pct": max(v / total * 100 for v in levels.values()) if total else 0,
        }
    }
    
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'=' * 60}")
    print(f"📊 Data Quality Report")
    print(f"{'=' * 60}")
    print(f"Total merged: {total}")
    print(f"Skipped (no label): {skipped_no_label}")
    print(f"Skipped (invalid): {skipped_invalid}")
    print(f"\nRisk Level Distribution:")
    for lv in ["low", "medium", "high"]:
        cnt = levels.get(lv, 0)
        pct = cnt / total * 100 if total else 0
        print(f"  {lv:8s}: {cnt:4d} ({pct:5.1f}%)")
    print(f"\nBalanced: {stats['quality_check']['balanced']}")
    print(f"\n→ Labeled data: {LABELED_PATH}")
    print(f"→ Stats: {STATS_PATH}")


if __name__ == "__main__":
    main()
