"""
Day 1 - Step 4: Convert labeled data into Gemma chat-template JSONL
Supports 4 data sources: DeepSeek / GLM / Qwen / Gemini
Splits into train / val.

Usage:
    python scripts/format_for_training.py
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

LABELED_PATH = Path(__file__).parent.parent / "data" / "labeled_train.jsonl"
TRAIN_OUTPUT = Path(__file__).parent.parent / "data" / "train_chat.jsonl"
VAL_OUTPUT = Path(__file__).parent.parent / "data" / "val_chat.jsonl"

DEFAULT_VAL_RATIO = 0.15

USER_TEMPLATE = """You are a Reliability Risk Judge. Analyze the following multi-LLM responses and assess the reliability risk level.

Question: {question}

Response A (DeepSeek): {a}

Response B (GLM): {b}

Response C (Qwen): {c}

Response D (Gemini): {d}

Evaluate along these dimensions:
1. Hallucination Risk (0-10)
2. Semantic Contradiction (0-10)
3. Uncertainty Signals (0-10)

Output your assessment in the required format."""

ASSISTANT_TEMPLATE = """Risk Level: {risk}
Hallucination Risk: {h}
Semantic Contradiction: {c}
Uncertainty Signals: {u}
Reasoning: {r}"""


def format_one(item: dict):
    resp = item.get("responses", {})
    a = resp.get("deepseek")
    b = resp.get("glm")
    c = resp.get("qwen")
    d = resp.get("gemini")
    # Need at least 2 valid responses (3 is ideal, 4 is best)
    if sum(1 for x in (a, b, c, d) if x) < 2:
        return None

    j = item.get("judgment")
    if not j:
        return None

    user = USER_TEMPLATE.format(
        question=item["question"],
        a=a or "[no response available]",
        b=b or "[no response available]",
        c=c or "[no response available]",
        d=d or "[no response available]",
    )
    assistant = ASSISTANT_TEMPLATE.format(
        risk=j["final_risk_level"],
        h=j["hallucination_risk"],
        c=j["semantic_contradiction"],
        u=j["uncertainty_signals"],
        r=j.get("reasoning", ""),
    )
    return {"messages": [
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


def rough_token_count(sample: dict) -> int:
    total = sum(len(m["content"]) for m in sample["messages"])
    return total // 3  # rough chars-to-tokens heuristic for mixed en+zh


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--val-ratio", type=float, default=DEFAULT_VAL_RATIO)
    parser.add_argument("--max-tokens", type=int, default=2000,
                        help="Skip samples estimated above this token count")
    args = parser.parse_args()

    labeled = []
    with open(LABELED_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                labeled.append(json.loads(line))
    print(f"Loaded {len(labeled)} labeled samples")

    formatted = []
    skipped_invalid, skipped_long = 0, 0
    for item in labeled:
        f = format_one(item)
        if not f:
            skipped_invalid += 1
            continue
        if rough_token_count(f) > args.max_tokens:
            skipped_long += 1
            continue
        formatted.append(f)
    print(f"Formatted {len(formatted)} (skipped invalid={skipped_invalid} long={skipped_long})")

    random.seed(42)
    random.shuffle(formatted)
    val_size = int(len(formatted) * args.val_ratio)
    val_data = formatted[:val_size]
    train_data = formatted[val_size:]

    TRAIN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(TRAIN_OUTPUT, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    with open(VAL_OUTPUT, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Train: {len(train_data)} -> {TRAIN_OUTPUT}")
    print(f"Val:   {len(val_data)} -> {VAL_OUTPUT}")
    if train_data:
        sample = train_data[0]
        print(f"\nSample stats (first train item):")
        print(f"  User len:      {len(sample['messages'][0]['content'])} chars")
        print(f"  Assistant len: {len(sample['messages'][1]['content'])} chars")


if __name__ == "__main__":
    main()
