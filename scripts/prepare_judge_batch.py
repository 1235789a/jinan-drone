"""
Day 1 工具: 从 raw_responses.jsonl 取 10 组数据，格式化为 Meta-Judge 输入。

使用:
    python scripts/prepare_judge_batch.py 1        # 第 1 个 judge 批次 (前 10 组)
    python scripts/prepare_judge_batch.py --all    # 生成所有 judge 批次
"""

import argparse
import json
import sys
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "judge_batches" / "inputs"
JUDGE_BATCH_SIZE = 10


def load_raw():
    if not RAW_PATH.exists():
        print(f"ERROR: {RAW_PATH} not found. Run parse_batch_output.py first.", file=sys.stderr)
        sys.exit(1)
    records = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def format_judge_batch(records_slice):
    """格式化为 Meta-Judge 输入格式"""
    blocks = []
    for i, rec in enumerate(records_slice, 1):
        resp = rec["responses"]
        block = f"""GROUP {i}:
Q: {rec['question']}
A (DeepSeek): {resp.get('deepseek', '[missing]')}
B (GLM): {resp.get('glm', '[missing]')}
C (Qwen): {resp.get('qwen', '[missing]')}"""
        blocks.append(block)
    return "\n\n".join(blocks)


def save_batch(batch_num, text, record_ids):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # Save the prompt text
    path = OUTPUT_DIR / f"judge_batch_{batch_num:03d}_input.txt"
    path.write_text(text, encoding="utf-8")
    # Save the record ID mapping (for later alignment)
    ids_path = OUTPUT_DIR / f"judge_batch_{batch_num:03d}_ids.json"
    ids_path.write_text(json.dumps(record_ids), encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_num", type=int, nargs="?")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    
    records = load_raw()
    total_batches = (len(records) + JUDGE_BATCH_SIZE - 1) // JUDGE_BATCH_SIZE
    
    print(f"Loaded {len(records)} records → {total_batches} judge batches")
    
    if args.all:
        for n in range(1, total_batches + 1):
            start = (n - 1) * JUDGE_BATCH_SIZE
            end = start + JUDGE_BATCH_SIZE
            batch = records[start:end]
            text = format_judge_batch(batch)
            ids = [r["id"] for r in batch]
            path = save_batch(n, text, ids)
            print(f"  Judge batch {n:03d}: {len(batch)} groups → {path}")
        return
    
    if args.batch_num is None:
        parser.print_help()
        sys.exit(1)
    
    n = args.batch_num
    start = (n - 1) * JUDGE_BATCH_SIZE
    end = start + JUDGE_BATCH_SIZE
    batch = records[start:end]
    text = format_judge_batch(batch)
    ids = [r["id"] for r in batch]
    path = save_batch(n, text, ids)
    
    print(f"\n=== Judge Batch {n}/{total_batches} ({len(batch)} groups) ===\n")
    print(text)
    print(f"\n→ Saved to: {path}")
    print(f"→ IDs: {ids}")


if __name__ == "__main__":
    main()
