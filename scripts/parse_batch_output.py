"""
Day 1 工具: 解析从 Trae 复制回来的三模型回答文本，合并为 raw_responses.jsonl。

目录约定:
    data/batches/outputs/batch_01_deepseek.txt
    data/batches/outputs/batch_01_glm.txt
    data/batches/outputs/batch_01_qwen.txt
    data/batches/inputs/batch_01_input.txt  (already generated)

使用:
    python scripts/parse_batch_output.py              # 解析所有批次
    python scripts/parse_batch_output.py --batch 1    # 解析单批次
"""

import argparse
import json
import re
import sys
from pathlib import Path

INPUTS_DIR = Path(__file__).parent.parent / "data" / "batches" / "inputs"
OUTPUTS_DIR = Path(__file__).parent.parent / "data" / "batches" / "outputs"
SEEDS_PATH = Path(__file__).parent.parent / "data" / "seeds.jsonl"
RAW_RESPONSES_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"

MODELS = ["deepseek", "glm", "qwen"]
BATCH_SIZE = 30

# Match lines like: "A1: <answer>" or "A12: <answer>"
ANSWER_PATTERN = re.compile(r"^A(\d+)\s*[:：]\s*(.+?)$", re.MULTILINE | re.DOTALL)


def load_seeds():
    seeds = []
    with open(SEEDS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                seeds.append(json.loads(line))
    return seeds


def parse_answers(text: str) -> dict[int, str]:
    """从一段文本里提取 {question_number: answer}"""
    answers = {}
    # Split by A<number>: pattern
    pattern = re.compile(r"^A(\d+)\s*[:：]\s*", re.MULTILINE)
    
    # Find all match positions
    matches = list(pattern.finditer(text))
    
    for i, match in enumerate(matches):
        num = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        answer = text[start:end].strip()
        # Clean trailing newlines
        answer = re.sub(r"\n{2,}", "\n", answer).strip()
        if answer and answer != "[UNANSWERABLE]":
            answers[num] = answer
    
    return answers


def parse_batch(batch_num: int, seeds: list) -> list[dict]:
    """解析一个批次，返回合并后的记录列表"""
    batch_file_template = OUTPUTS_DIR / f"batch_{batch_num:02d}_{{model}}.txt"
    
    # Check all three files exist
    missing = []
    for model in MODELS:
        path = Path(str(batch_file_template).format(model=model))
        if not path.exists():
            missing.append(model)
    
    if missing:
        print(f"  ⚠️  Batch {batch_num}: missing {missing}, skipping")
        return []
    
    # Parse each model's answers
    model_answers = {}
    for model in MODELS:
        path = Path(str(batch_file_template).format(model=model))
        text = path.read_text(encoding="utf-8")
        model_answers[model] = parse_answers(text)
    
    # Get corresponding seeds
    start = (batch_num - 1) * BATCH_SIZE
    end = start + BATCH_SIZE
    batch_seeds = seeds[start:end]
    
    records = []
    for i, seed in enumerate(batch_seeds, 1):
        ds_ans = model_answers["deepseek"].get(i)
        glm_ans = model_answers["glm"].get(i)
        qwen_ans = model_answers["qwen"].get(i)
        
        # Skip records with fewer than 2 valid answers
        valid_count = sum(1 for a in [ds_ans, glm_ans, qwen_ans] if a)
        if valid_count < 2:
            continue
        
        records.append({
            "id": seed["id"],
            "batch": batch_num,
            "domain": seed["domain"],
            "subtopic": seed.get("subtopic", ""),
            "lang": seed.get("lang", "en"),
            "question": seed["question"],
            "responses": {
                "deepseek": ds_ans,
                "glm": glm_ans,
                "qwen": qwen_ans,
            },
        })
    
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, help="Parse only this batch number")
    args = parser.parse_args()
    
    seeds = load_seeds()
    total_batches = (len(seeds) + BATCH_SIZE - 1) // BATCH_SIZE
    
    batches = [args.batch] if args.batch else range(1, total_batches + 1)
    
    all_records = []
    for n in batches:
        print(f"Processing batch {n}...")
        records = parse_batch(n, seeds)
        print(f"  → {len(records)}/{BATCH_SIZE} valid records")
        all_records.extend(records)
    
    # Write output
    RAW_RESPONSES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_RESPONSES_PATH, "w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    
    print(f"\n✅ Total: {len(all_records)} records → {RAW_RESPONSES_PATH}")
    
    # Stats
    from collections import Counter
    domains = Counter(r["domain"] for r in all_records)
    langs = Counter(r["lang"] for r in all_records)
    print(f"   Domains: {dict(domains)}")
    print(f"   Languages: {dict(langs)}")


if __name__ == "__main__":
    main()
