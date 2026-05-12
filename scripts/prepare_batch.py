"""
Day 1 工具: 从 seeds.jsonl 中取出第 N 批（30 条），格式化为可粘贴到 Trae 的文本。

使用:
    python scripts/prepare_batch.py 1         # 输出第 1 批
    python scripts/prepare_batch.py 1 --copy  # 同时复制到剪贴板（需 pyperclip）
    python scripts/prepare_batch.py --all     # 生成所有 34 批到 data/batches/inputs/
"""

import argparse
import json
import sys
from pathlib import Path

SEEDS_PATH = Path(__file__).parent.parent / "data" / "seeds.jsonl"
BATCH_SIZE = 30
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "batches" / "inputs"


def load_seeds():
    if not SEEDS_PATH.exists():
        print(f"ERROR: {SEEDS_PATH} not found. Run Step 1 first.", file=sys.stderr)
        sys.exit(1)
    seeds = []
    with open(SEEDS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))
    return seeds


def format_batch(seeds_slice):
    """格式化为 Trae 输入格式"""
    lines = []
    for i, seed in enumerate(seeds_slice, 1):
        lines.append(f"Q{i}: {seed['question']}")
    return "\n".join(lines)


def save_batch(batch_num, text):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"batch_{batch_num:02d}_input.txt"
    path.write_text(text, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_num", type=int, nargs="?", help="Batch number (1-34)")
    parser.add_argument("--all", action="store_true", help="Generate all batches")
    parser.add_argument("--copy", action="store_true", help="Copy to clipboard")
    args = parser.parse_args()

    seeds = load_seeds()
    total_batches = (len(seeds) + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"Loaded {len(seeds)} seeds → {total_batches} batches of {BATCH_SIZE}")

    if args.all:
        for n in range(1, total_batches + 1):
            start = (n - 1) * BATCH_SIZE
            end = start + BATCH_SIZE
            batch = seeds[start:end]
            text = format_batch(batch)
            path = save_batch(n, text)
            print(f"  Batch {n:02d}: {len(batch)} questions → {path}")
        print(f"\nAll batches saved to {OUTPUT_DIR}/")
        return

    if args.batch_num is None:
        parser.print_help()
        sys.exit(1)

    n = args.batch_num
    if n < 1 or n > total_batches:
        print(f"ERROR: batch_num must be 1-{total_batches}", file=sys.stderr)
        sys.exit(1)

    start = (n - 1) * BATCH_SIZE
    end = start + BATCH_SIZE
    batch = seeds[start:end]
    text = format_batch(batch)

    path = save_batch(n, text)

    print(f"\n=== Batch {n}/{total_batches} ({len(batch)} questions) ===\n")
    print(text)
    print(f"\n→ Saved to: {path}")

    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(text)
            print("→ Copied to clipboard!")
        except ImportError:
            print("(install pyperclip for --copy: pip install pyperclip)")


if __name__ == "__main__":
    main()
