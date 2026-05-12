"""
Day 1 - Step 1: 种子问题生成 (API 版本，零人工)

用 DeepSeek-V4 批量生成 1000 条高风险种子问题。
分 5 轮生成（每轮 200 条），每轮指定一个 domain，避免单次输出过长导致截断。

使用:
    python scripts/generate_seeds.py              # 生成 1000 条
    python scripts/generate_seeds.py --mvp        # MVP 模式，只生成 60 条
    python scripts/generate_seeds.py --resume     # 跳过已生成的 domain
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from providers import load_providers, make_client

SEEDS_PATH = Path(__file__).parent.parent / "data" / "seeds.jsonl"

DOMAINS = [
    {
        "id": "medical",
        "name": "Medical & Health",
        "lang": "en",
        "subtopics": [
            "Drug interactions & dosage edge cases",
            "Differential diagnosis of atypical presentations",
            "Post-op risk assessments",
            "Pediatric vs adult dosing conflicts",
            "Alternative therapy efficacy claims",
            "Rare disease diagnostic criteria",
            "Lab result interpretation edge cases",
            "Emergency triage decision points",
        ],
    },
    {
        "id": "legal",
        "name": "Legal & Compliance",
        "lang": "en",
        "subtopics": [
            "Cross-jurisdictional conflicts (US state vs federal, EU vs US)",
            "Contract clause interpretation disputes",
            "IP boundary cases (AI-generated content, fair use)",
            "Labor law gray zones",
            "Data privacy compliance (GDPR/CCPA/PIPL conflicts)",
            "Criminal liability thresholds",
            "Administrative penalty standards",
            "Arbitration vs litigation strategic choices",
        ],
    },
    {
        "id": "science",
        "name": "Science & Research",
        "lang": "en",
        "subtopics": [
            "Dark matter / dark energy interpretations",
            "Quantum computing practical limits",
            "CRISPR ethics and boundary cases",
            "Climate model divergences",
            "Neuroscience of consciousness debates",
            "Nutrition controversies with conflicting studies",
            "Evolutionary biology edge cases",
            "Cosmological hypotheses under contention",
        ],
    },
    {
        "id": "tech",
        "name": "Technology & Engineering",
        "lang": "en",
        "subtopics": [
            "API version compatibility traps",
            "Framework best-practice disputes",
            "Performance optimization tradeoffs",
            "Security vulnerability mitigation choices",
            "System architecture pattern selection",
            "Config parameter tuning for specific workloads",
            "Deprecation migration paths",
            "Concurrency model selection",
        ],
    },
    {
        "id": "history",
        "name": "History & Society",
        "lang": "mixed",  # 50/50 en/zh
        "subtopics": [
            "有争议历史事件的归因 / Contested historical attributions",
            "具体数字考证（伤亡、经济数据）/ Specific figure verification",
            "历史人物评价分歧 / Contested historical figure evaluations",
            "文明起源理论 / Civilization origin theories",
            "战争决策动机 / Wartime decision motivations",
            "文化遗产归属争议 / Cultural heritage ownership disputes",
            "历史分期与定性 / Periodization disputes",
            "社会政策效果评估 / Social policy impact assessments",
        ],
    },
]

PROMPT_TEMPLATE = """You are a dataset architect building a RELIABILITY RISK detection benchmark. Generate {n} high-quality seed questions designed to trigger DISAGREEMENT among frontier LLMs.

## Design Principles
Each question must trigger at least one of:
1. Hallucination-prone: specific numbers, dates, citations, technical parameters
2. Contradiction-prone: contested interpretations, jurisdiction-specific, version-specific
3. Uncertainty-prone: edge cases, recent developments, expert-level nuance

AVOID:
- Trivia with clear single answers
- Pure opinion questions
- Questions requiring real-time data

## This Batch

Domain: {domain_name}
Subtopics (distribute evenly across these): {subtopics}
Language: {lang_instruction}

## Quality Bar
- Answerable in 80-200 words
- Mentions specific entities (drugs, laws, APIs, events, versions, numbers)
- Not Googleable to a single canonical answer
- Triggers hallucination / contradiction / uncertainty

## Output Format (STRICT JSONL, no preamble, no markdown fences)

Output exactly {n} lines. Each line:
{{"id": <int starting from {start_id}>, "domain": "{domain_id}", "subtopic": "<subtopic>", "question": "<question>", "lang": "<en|zh>"}}

Start now. No commentary before or after."""


def build_prompt(domain: dict, n: int, start_id: int) -> str:
    if domain["lang"] == "mixed":
        lang_instruction = "Half in English (lang=en), half in Chinese (lang=zh). Alternate."
    elif domain["lang"] == "zh":
        lang_instruction = "All in Chinese (lang=zh)."
    else:
        lang_instruction = "All in English (lang=en)."

    return PROMPT_TEMPLATE.format(
        n=n,
        domain_name=domain["name"],
        domain_id=domain["id"],
        subtopics="; ".join(domain["subtopics"]),
        lang_instruction=lang_instruction,
        start_id=start_id,
    )


def parse_jsonl_response(text: str) -> list[dict]:
    """Extract valid JSON lines from the model's response."""
    seeds = []
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        # Strip markdown fence leftovers
        if line.startswith("```") or line.endswith("```"):
            continue
        try:
            obj = json.loads(line)
            required = {"id", "domain", "subtopic", "question", "lang"}
            if required.issubset(obj.keys()):
                seeds.append(obj)
        except json.JSONDecodeError:
            continue
    return seeds


async def generate_for_domain(client, model: str, domain: dict, n: int, start_id: int) -> list[dict]:
    prompt = build_prompt(domain, n, start_id)
    print(f"  [{domain['id']}] requesting {n} seeds starting at id={start_id}...")

    # Some models (reasoning models) may take 30-60s for a large JSON output
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=16000,
    )

    text = response.choices[0].message.content
    seeds = parse_jsonl_response(text)
    print(f"  [{domain['id']}] parsed {len(seeds)}/{n} valid seeds")

    # Fix IDs just in case the model messed up
    for i, seed in enumerate(seeds):
        seed["id"] = start_id + i
        seed["domain"] = domain["id"]

    return seeds


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mvp", action="store_true", help="60 seeds total (12 per domain)")
    parser.add_argument("--target", type=int, default=1000,
                        help="Total seeds to generate (default 1000)")
    parser.add_argument("--provider", default="deepseek",
                        help="Which provider to use (default deepseek)")
    args = parser.parse_args()

    if args.mvp:
        args.target = 60

    providers = load_providers()
    if args.provider not in providers:
        print(f"ERROR: provider '{args.provider}' not configured. "
              f"Available: {list(providers.keys())}", file=sys.stderr)
        sys.exit(1)

    provider = providers[args.provider]
    client = make_client(provider)

    per_domain = args.target // len(DOMAINS)
    print(f"Target: {args.target} total, {per_domain}/domain")
    print(f"Using provider: {provider.name} (model={provider.model})")

    all_seeds = []
    tasks = []
    for i, domain in enumerate(DOMAINS):
        start_id = 1 + i * per_domain
        tasks.append(generate_for_domain(client, provider.model, domain, per_domain, start_id))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for res in results:
        if isinstance(res, Exception):
            print(f"  ERROR: {res}", file=sys.stderr)
            continue
        all_seeds.extend(res)

    # Re-number globally
    for i, seed in enumerate(all_seeds, 1):
        seed["id"] = i

    SEEDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEDS_PATH, "w", encoding="utf-8") as f:
        for seed in all_seeds:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")

    # Stats
    from collections import Counter
    domain_counts = Counter(s["domain"] for s in all_seeds)
    lang_counts = Counter(s["lang"] for s in all_seeds)

    print(f"\n{'=' * 60}")
    print(f"Generated {len(all_seeds)} seeds -> {SEEDS_PATH}")
    print(f"  By domain: {dict(domain_counts)}")
    print(f"  By lang: {dict(lang_counts)}")


if __name__ == "__main__":
    asyncio.run(main())
