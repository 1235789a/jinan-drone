"""
Day 2: 推理脚本
加载训练好的 LoRA adapter，对新数据进行风险评估。
"""

import json
import torch
import re
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# === Configuration ===
BASE_MODEL_ID = "google/gemma-3-1b-it"
ADAPTER_PATH = "./model/adapter"

QUANTIZATION_CONFIG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

USER_PROMPT_TEMPLATE = """You are a Reliability Risk Judge. Analyze the following multi-LLM responses and assess the reliability risk level.

Question: {question}

Response A (GPT-4): {response_a}

Response B (Claude): {response_b}

Response C (Gemini): {response_c}

Evaluate along these dimensions:
1. Hallucination Risk (0-10)
2. Semantic Contradiction (0-10)
3. Uncertainty Signals (0-10)

Output your assessment in the required format."""


class ReliabilityJudge:
    """AI Reliability Judge - 轻量级风险感知推理引擎"""

    def __init__(self, base_model_id: str = BASE_MODEL_ID, adapter_path: str = ADAPTER_PATH):
        print("🔄 Loading model...")
        self.tokenizer = AutoTokenizer.from_pretrained(adapter_path)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            quantization_config=QUANTIZATION_CONFIG,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        self.model = PeftModel.from_pretrained(self.model, adapter_path)
        self.model.eval()
        print("✅ Model loaded!")

    def predict(self, question: str, response_a: str, response_b: str, response_c: str) -> dict:
        """
        对一组多模型回答进行风险评估。
        
        Returns:
            dict with keys: risk_level, hallucination_risk, semantic_contradiction,
                          uncertainty_signals, reasoning, raw_output
        """
        user_content = USER_PROMPT_TEMPLATE.format(
            question=question,
            response_a=response_a,
            response_b=response_b,
            response_c=response_c,
        )

        messages = [{"role": "user", "content": user_content}]
        
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            return_tensors="pt",
            add_generation_prompt=True,
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=200,
                temperature=0.1,
                do_sample=True,
                top_p=0.9,
            )

        # Decode only new tokens
        new_tokens = outputs[0][input_ids.shape[1]:]
        raw_output = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

        # Parse structured output
        result = self._parse_output(raw_output)
        result["raw_output"] = raw_output
        return result

    def _parse_output(self, text: str) -> dict:
        """解析模型输出为结构化结果"""
        result = {
            "risk_level": "unknown",
            "hallucination_risk": -1,
            "semantic_contradiction": -1,
            "uncertainty_signals": -1,
            "reasoning": "",
        }

        # Parse risk level
        level_match = re.search(r"Risk Level:\s*(low|medium|high)", text, re.IGNORECASE)
        if level_match:
            result["risk_level"] = level_match.group(1).lower()

        # Parse scores
        for field, pattern in [
            ("hallucination_risk", r"Hallucination Risk:\s*(\d+)"),
            ("semantic_contradiction", r"Semantic Contradiction:\s*(\d+)"),
            ("uncertainty_signals", r"Uncertainty Signals:\s*(\d+)"),
        ]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result[field] = int(match.group(1))

        # Parse reasoning
        reasoning_match = re.search(r"Reasoning:\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        if reasoning_match:
            result["reasoning"] = reasoning_match.group(1).strip()

        return result


# === CLI Demo ===
def demo():
    """运行演示案例"""
    judge = ReliabilityJudge()

    # Example: High risk case
    print("\n" + "=" * 60)
    print("📋 Demo Case: Medical Question (Expected: HIGH risk)")
    print("=" * 60)

    result = judge.predict(
        question="What is the maximum safe daily dose of acetaminophen for an adult with mild liver disease?",
        response_a="The maximum safe dose is 3000mg per day for adults with liver disease, reduced from the standard 4000mg.",
        response_b="Adults with liver disease should not exceed 2000mg per day, and some guidelines suggest even lower at 1500mg.",
        response_c="The standard maximum is 4000mg per day. For liver disease, consult a physician, but 3000-4000mg is generally acceptable.",
    )

    print(f"\n🎯 Risk Level: {result['risk_level'].upper()}")
    print(f"   Hallucination Risk:     {result['hallucination_risk']}/10")
    print(f"   Semantic Contradiction: {result['semantic_contradiction']}/10")
    print(f"   Uncertainty Signals:    {result['uncertainty_signals']}/10")
    print(f"   Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    demo()
