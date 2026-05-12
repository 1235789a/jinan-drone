"""
Day 1 - Step 4: 数据格式转换脚本
将标注数据转换为 Gemma chat template 格式，用于 QLoRA 微调。
"""

import json
from pathlib import Path

# --- Configuration ---
LABELED_PATH = Path(__file__).parent.parent / "data" / "labeled_train.jsonl"
TRAIN_OUTPUT = Path(__file__).parent.parent / "data" / "train_chat.jsonl"
VAL_OUTPUT = Path(__file__).parent.parent / "data" / "val_chat.jsonl"

VAL_RATIO = 0.15  # 15% for validation

# --- Prompt Template ---
USER_TEMPLATE = """You are a Reliability Risk Judge. Analyze the following multi-LLM responses and assess the reliability risk level.

Question: {question}

Response A (GPT-4): {response_gpt4o}

Response B (Claude): {response_claude}

Response C (Gemini): {response_gemini}

Evaluate along these dimensions:
1. Hallucination Risk (0-10)
2. Semantic Contradiction (0-10)
3. Uncertainty Signals (0-10)

Output your assessment in the required format."""

ASSISTANT_TEMPLATE = """Risk Level: {final_risk_level}
Hallucination Risk: {hallucination_risk}
Semantic Contradiction: {semantic_contradiction}
Uncertainty Signals: {uncertainty_signals}
Reasoning: {reasoning}"""


def format_single(item: dict) -> dict:
    """将单条标注数据转换为 chat format"""
    user_content = USER_TEMPLATE.format(
        question=item["question"],
        response_gpt4o=item["responses"].get("gpt4o", "[No response available]"),
        response_claude=item["responses"].get("claude", "[No response available]"),
        response_gemini=item["responses"].get("gemini", "[No response available]"),
    )

    assistant_content = ASSISTANT_TEMPLATE.format(
        final_risk_level=item["judgment"]["final_risk_level"],
        hallucination_risk=item["judgment"]["hallucination_risk"],
        semantic_contradiction=item["judgment"]["semantic_contradiction"],
        uncertainty_signals=item["judgment"]["uncertainty_signals"],
        reasoning=item["judgment"]["reasoning"],
    )

    return {
        "messages": [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
        ]
    }


def validate_token_length(item: dict, max_tokens: int = 2048) -> bool:
    """粗略验证 token 长度（按字符数 / 4 估算）"""
    total_chars = sum(len(m["content"]) for m in item["messages"])
    estimated_tokens = total_chars / 4
    return estimated_tokens < max_tokens


def main():
    # Load labeled data
    labeled = []
    with open(LABELED_PATH, "r", encoding="utf-8") as f:
        for line in f:
            labeled.append(json.loads(line))

    print(f"📋 Loaded {len(labeled)} labeled samples")

    # Convert to chat format
    formatted = []
    skipped = 0
    for item in labeled:
        chat_item = format_single(item)
        if validate_token_length(chat_item):
            formatted.append(chat_item)
        else:
            skipped += 1

    print(f"✅ Formatted {len(formatted)} samples (skipped {skipped} too-long)")

    # Split train/val
    import random
    random.seed(42)
    random.shuffle(formatted)
    
    val_size = int(len(formatted) * VAL_RATIO)
    val_data = formatted[:val_size]
    train_data = formatted[val_size:]

    # Write output
    TRAIN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    
    with open(TRAIN_OUTPUT, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(VAL_OUTPUT, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\n📊 Split: {len(train_data)} train / {len(val_data)} val")
    print(f"   Train: {TRAIN_OUTPUT}")
    print(f"   Val:   {VAL_OUTPUT}")

    # Sanity check
    print(f"\n🔍 Sample (first item):")
    sample = train_data[0] if train_data else formatted[0]
    print(f"   User prompt length: {len(sample['messages'][0]['content'])} chars")
    print(f"   Assistant length:   {len(sample['messages'][1]['content'])} chars")


if __name__ == "__main__":
    main()
