"""
Day 1 - Step 3: 结构化标注脚本
用 GPT-4o 作为 Meta-Judge，对每组多模型回答进行结构化风险评估。
核心原则：不是字符串相似度！而是语义层面的分歧判断。
"""

import json
import os
import asyncio
from pathlib import Path
from typing import Optional

# --- Configuration ---
RAW_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "labeled_train.jsonl"
STATS_PATH = Path(__file__).parent.parent / "data" / "stats.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_CONCURRENT = 3

# --- Meta-Judge Prompt ---
JUDGE_SYSTEM_PROMPT = """You are a Reliability Risk Meta-Judge. Your job is to analyze multiple AI model responses to the same question and assess the RELIABILITY RISK level.

You are NOT judging who is correct. You are assessing HOW MUCH RISK exists in trusting these answers.

## Risk Dimensions (score 0-10 each):

1. **Hallucination Risk**: Are any responses likely fabricated? Do they contain suspiciously specific details that seem invented? Do they contradict well-established knowledge?

2. **Semantic Contradiction**: Do the responses fundamentally disagree on key claims? Not just phrasing differences, but actual contradictions in substance, numbers, recommendations, or conclusions.

3. **Uncertainty Signals**: Do responses contain hedging language? Do they acknowledge limitations? Does one model sound certain while others equivocate? Overconfidence in uncertain areas is a risk signal.

## Risk Level Rules:
- **low**: All models substantially agree, no hallucination indicators, appropriate confidence levels
- **medium**: Some disagreement on details/nuances, OR one model shows uncertainty signals, OR minor factual discrepancies that don't affect core message
- **high**: Fundamental contradictions between models, OR clear hallucination indicators, OR dangerous overconfidence on uncertain topics

## Output Format (strict JSON):
{
  "hallucination_risk": <0-10>,
  "semantic_contradiction": <0-10>,  
  "uncertainty_signals": <0-10>,
  "final_risk_level": "<low|medium|high>",
  "reasoning": "<2-3 sentences explaining the key risk factors>"
}"""

JUDGE_USER_TEMPLATE = """Analyze the following multi-model responses:

**Question:** {question}

**Response A (GPT-4o):**
{response_gpt4o}

**Response B (Claude 3.5):**
{response_claude}

**Response C (Gemini 1.5):**
{response_gemini}

Provide your structured risk assessment as JSON."""


async def judge_single(semaphore, item: dict) -> Optional[dict]:
    """用 GPT-4o 对单条数据进行结构化标注"""
    async with semaphore:
        user_prompt = JUDGE_USER_TEMPLATE.format(
            question=item["question"],
            response_gpt4o=item["responses"].get("gpt4o", "[No response]"),
            response_claude=item["responses"].get("claude", "[No response]"),
            response_gemini=item["responses"].get("gemini", "[No response]"),
        )

        # TODO: 替换为真实 API 调用
        # import openai
        # client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        # response = await client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=[
        #         {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        #         {"role": "user", "content": user_prompt},
        #     ],
        #     temperature=0,
        #     response_format={"type": "json_object"},
        # )
        # judgment = json.loads(response.choices[0].message.content)

        # Placeholder
        judgment = {
            "hallucination_risk": 5,
            "semantic_contradiction": 5,
            "uncertainty_signals": 5,
            "final_risk_level": "medium",
            "reasoning": "[PLACEHOLDER - replace with real GPT-4o judge output]",
        }

        return {
            **item,
            "judgment": judgment,
        }


def compute_stats(labeled_data: list) -> dict:
    """计算数据分布统计"""
    total = len(labeled_data)
    distribution = {"low": 0, "medium": 0, "high": 0}
    domain_dist = {}
    
    for item in labeled_data:
        level = item["judgment"]["final_risk_level"]
        distribution[level] = distribution.get(level, 0) + 1
        
        domain = item.get("domain", "unknown")
        if domain not in domain_dist:
            domain_dist[domain] = {"low": 0, "medium": 0, "high": 0}
        domain_dist[domain][level] += 1

    return {
        "total_samples": total,
        "distribution": distribution,
        "distribution_pct": {k: round(v/total*100, 1) for k, v in distribution.items()},
        "domain_distribution": domain_dist,
        "quality_check": {
            "min_class_pct": min(v/total*100 for v in distribution.values()),
            "max_class_pct": max(v/total*100 for v in distribution.values()),
            "balanced": all(20 <= v/total*100 <= 50 for v in distribution.values()),
        }
    }


async def main():
    # Load raw responses
    raw_data = []
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            raw_data.append(json.loads(line))

    print(f"📋 Loaded {len(raw_data)} response sets for labeling")

    # Run judge
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = [judge_single(semaphore, item) for item in raw_data]
    results = await asyncio.gather(*tasks)

    # Filter valid results
    labeled = [r for r in results if r is not None]

    # Write labeled data
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for item in labeled:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # Compute and write stats
    stats = compute_stats(labeled)
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Labeled {len(labeled)} samples")
    print(f"   Distribution: {stats['distribution']}")
    print(f"   Percentages:  {stats['distribution_pct']}")
    print(f"   Balanced:     {stats['quality_check']['balanced']}")
    print(f"\n   Output: {OUTPUT_PATH}")
    print(f"   Stats:  {STATS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
