"""
Day 2: Gemma 4 2B (E2B) QLoRA 微调训练脚本
设计用于 Kaggle T4/P100 环境运行。
比赛要求: Gemma 4 Good Hackathon - 必须使用 Gemma 4 模型
"""

import json
import torch
from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# === Configuration ===
MODEL_ID = "google/gemma-4-2b-it"
OUTPUT_DIR = "./checkpoints"
FINAL_MODEL_DIR = "./model/adapter"

TRAIN_DATA_PATH = "./data/train_chat.jsonl"
VAL_DATA_PATH = "./data/val_chat.jsonl"

# QLoRA Config
QUANTIZATION_CONFIG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

LORA_CONFIG = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)

# Training hyperparameters
TRAINING_ARGS = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
    bf16=True,
    gradient_checkpointing=True,
    max_grad_norm=0.3,
    optim="paged_adamw_8bit",
    report_to="none",
    seed=42,
)

MAX_SEQ_LENGTH = 1024


# === Data Loading ===
def load_data(path: str) -> Dataset:
    """Load JSONL chat data into HuggingFace Dataset"""
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            # Combine into single text for SFT
            data.append(item)
    return Dataset.from_list(data)


def format_chat(example, tokenizer):
    """Format messages using tokenizer's chat template"""
    text = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False,
        add_generation_prompt=False,
    )
    return {"text": text}


# === Main Training Loop ===
def main():
    print("=" * 60)
    print("🚀 AI Reliability Judge - QLoRA Training")
    print("=" * 60)

    # 1. Load tokenizer
    print("\n📦 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 2. Load model with quantization
    print("📦 Loading model with 4-bit quantization...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=QUANTIZATION_CONFIG,
        device_map="auto",
        torch_dtype=torch.bfloat16,
    )
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, LORA_CONFIG)

    # Print trainable params
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   Trainable: {trainable_params:,} / {total_params:,} "
          f"({100 * trainable_params / total_params:.2f}%)")

    # 3. Load and format data
    print("\n📊 Loading training data...")
    train_dataset = load_data(TRAIN_DATA_PATH)
    val_dataset = load_data(VAL_DATA_PATH)

    train_dataset = train_dataset.map(
        lambda x: format_chat(x, tokenizer), remove_columns=["messages"]
    )
    val_dataset = val_dataset.map(
        lambda x: format_chat(x, tokenizer), remove_columns=["messages"]
    )

    print(f"   Train: {len(train_dataset)} samples")
    print(f"   Val:   {len(val_dataset)} samples")

    # 4. Train
    print("\n🏋️ Starting training...")
    trainer = SFTTrainer(
        model=model,
        args=TRAINING_ARGS,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        max_seq_length=MAX_SEQ_LENGTH,
        dataset_text_field="text",
    )

    trainer.train()

    # 5. Save
    print("\n💾 Saving adapter...")
    trainer.save_model(FINAL_MODEL_DIR)
    tokenizer.save_pretrained(FINAL_MODEL_DIR)

    print(f"\n✅ Training complete! Adapter saved to: {FINAL_MODEL_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
