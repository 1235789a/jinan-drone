"""
Day 1 - Step 1: 种子问题生成脚本
基于 taxonomy.json 中的领域和子话题，调用 LLM 生成高质量种子问题。
"""

import json
import os
from pathlib import Path

# --- Configuration ---
TAXONOMY_PATH = Path(__file__).parent.parent / "seeds" / "taxonomy.json"
OUTPUT_PATH = Path(__file__).parent.parent / "seeds" / "generated_seeds.jsonl"
SEEDS_PER_SUBTOPIC = 5  # 5 subtopics × 8 topics × 5 = 200 seeds


def load_taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_seeds_with_llm(domain: dict, subtopic: str, n: int = 5) -> list[str]:
    """
    用 LLM (GPT-4o) 为每个子话题生成 n 个高风险种子问题。
    问题设计原则：
    1. 具体、不模糊
    2. 有潜在争议性或不确定性
    3. 需要专业知识才能回答
    4. 容易产生模型间分歧
    """
    # TODO: 替换为真实 API 调用
    prompt = f"""Generate {n} specific, potentially controversial questions about "{subtopic}" 
in the domain of "{domain['name']}". 

Requirements:
- Questions should be specific enough that different AI models might give different answers
- Questions should touch on areas where hallucination is likely
- Questions should require expert knowledge
- Mix of factual questions (where one model might hallucinate) and judgment questions (where models may disagree)
- Output as JSON array of strings

Domain context: {domain['seed_template'].replace('{subtopic}', subtopic)}"""

    # Placeholder - replace with actual API call
    print(f"  [TODO] Generate {n} seeds for: {domain['name']} > {subtopic}")
    return [f"[PLACEHOLDER] {domain['name']} - {subtopic} - Q{i+1}" for i in range(n)]


def main():
    taxonomy = load_taxonomy()
    all_seeds = []

    for domain in taxonomy["domains"]:
        print(f"\n=== Domain: {domain['name']} ===")
        for subtopic in domain["subtopics"]:
            questions = generate_seeds_with_llm(domain, subtopic, SEEDS_PER_SUBTOPIC)
            for q in questions:
                all_seeds.append({
                    "domain": domain["id"],
                    "domain_name": domain["name"],
                    "subtopic": subtopic,
                    "question": q,
                })

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for seed in all_seeds:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")

    print(f"\n✅ Generated {len(all_seeds)} seeds → {OUTPUT_PATH}")
    print(f"   Distribution: {len(taxonomy['domains'])} domains × "
          f"{len(taxonomy['domains'][0]['subtopics'])} subtopics × "
          f"{SEEDS_PER_SUBTOPIC} questions")


if __name__ == "__main__":
    main()
