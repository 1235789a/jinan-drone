"""
Day 1 - Step 3: Meta-Judge structured labeling (API, zero human touch)

Uses CLAUDE (via proxy) as the primary judge, with automatic fallback to GEMINI
if Claude is not configured. Rationale:
  - Claude Sonnet 4.6 gives the most structured, reliable JSON output
  - Independent from all 4 data sources (no self-preference bias)
  - Gemini fallback lets you run MVP without paying for Claude first

- Resume-safe
- Real-time JSONL writes
- Strict JSON validation

Usage:
    python scripts/label_judge.py              # process all raw_responses.jsonl
    python scripts/label_judge.py --mvp        # only first 60
    python scripts/label_judge.py --judge gemini   # force gemini as judge
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm.asyncio import tqdm as atqdm

from providers import load_providers, make_client

RAW_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"
LABELED_PATH = Path(__file__).parent.parent / "data" / "labeled_train.jsonl"
STATS_PATH = Path(__file__).parent.parent / "data" / "stats.json"

# Preference order: claude proxy first, then gemini as fallback
JUDGE_PREFERENCE = ["claude", "gemini"]

JUDGE_SYSTEM_PROMPT = """You are a RELIABILITY RISK META-JUDGE. You evaluate groups of LLM responses to identify risk signals. You are NOT judging correctness - you assess TRUST RISK.

## Three Risk Dimensions (each 0-10)

### 1. hallucination_risk
Signs: suspiciously specific numbers without citation, invented studies/people/laws, claims violating known consensus, overconfidence on known-uncertain topics.
- 0: all responses cite well-known consensus facts
- 5: one response has plausible but unverifiable specifics
- 10: at least one response contains clearly fabricated content

### 2. semantic_contradiction
Signs: opposing final recommendations, incompatible numeric answers (not just precision differences), mutually exclusive factual claims.
- 0: all responses agree on core claims
- 5: partial disagreement on secondary details, core aligned
- 10: direct contradictions on the central question

### 3. uncertainty_signals
Signs: inconsistent hedging across models (one certain, others hedging), overconfidence on genuinely uncertain topics.
- 0: all well-calibrated
- 5: mild mismatch
- 10: one response dangerously overconfident on an uncertain topic

## Final Risk Level (decisive rules)
- "low":    all dimensions <= 3 AND no red flags
- "medium": any dimension 4-6, OR mixed signals without clear danger
- "high":   any dimension >= 7, OR clear hallucination, OR fundamental contradictions on high-stakes topics (medical/legal)

## Calibration Anchors

Example 1 (low): "Capital of France?" all say Paris -> halluc=0 contra=0 uncert=0 -> low
Example 2 (high): "Max acetaminophen for cirrhosis?" 3000mg vs 2000mg vs 4000mg -> halluc=6 contra=9 uncert=7 -> high
Example 3 (medium): "Best PostgreSQL pool size for 1000 users?" 50 / 100-200 / 50-100 -> halluc=1 contra=4 uncert=3 -> medium

## Output Format (STRICT JSON, one line, no markdown, no preamble)

{"hallucination_risk": <0-10>, "semantic_contradiction": <0-10>, "uncertainty_signals": <0-10>, "final_risk_level": "<low|medium|high>", "reasoning": "<2 short sentences>"}
"""


def build_judge_prompt(record: dict) -> str:
    """Format the record's 2-4 model responses into a judge-ready prompt."""
    resp = record["responses"]
    # Map internal names to human-readable labels used by the judge prompt
    display = {
        "deepseek": "A (DeepSeek)",
        "glm": "B (GLM)",
        "qwen": "C (Qwen)",
        "gemini": "D (Gemini)",
    }
    blocks = [f"Q: {record['question']}\n"]
    for key, label in display.items():
        content = resp.get(key)
        if content:
            blocks.append(f"{label}: {content}\n")
    blocks.append("\nOutput your structured risk assessment as a single JSON line.")
    return "\n".join(blocks)


def extract_json(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None


def validate_label(label) -> bool:
    if not isinstance(label, dict):
        return False
    for k in ("hallucination_risk", "semantic_contradiction", "uncertainty_signals"):
        v = label.get(k)
        if not isinstance(v, (int, float)) or not 0 <= v <= 10:
            return False
    if label.get("final_risk_level") not in ("low", "medium", "high"):
        return False
    return True


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=30), reraise=True)
async def judge_one(client, model: str, record: dict):
    prompt = build_judge_prompt(record)
    resp = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=300,
    )
    text = (resp.choices[0].message.content or "").strip()
    label = extract_json(text)
    if not validate_label(label):
        return None
    for k in ("hallucination_risk", "semantic_contradiction", "uncertainty_signals"):
        label[k] = int(label[k])
    return label


async def process_one(record: dict, client, model: str, sem: asyncio.Semaphore):
    async with sem:
        try:
            label = await judge_one(client, model, record)
        except Exception as e:
            print(f"  [id={record['id']}] judge error: {type(e).__name__}: {str(e)[:100]}",
                  file=sys.stderr)
            return None
        if not label:
            return None
        return {**record, "judgment": label}


def load_raw() -> list:
    if not RAW_PATH.exists():
        print(f"ERROR: {RAW_PATH} not found. Run call_models.py first.", file=sys.stderr)
        sys.exit(1)
    records = []
    with open(RAW_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_labeled_ids() -> set:
    done = set()
    if LABELED_PATH.exists():
        with open(LABELED_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if "judgment" in obj:
                        done.add(obj["id"])
                except json.JSONDecodeError:
                    continue
    return done


def compute_stats(labeled: list) -> dict:
    from collections import Counter
    levels = Counter(r["judgment"]["final_risk_level"] for r in labeled)
    domains = Counter(r["domain"] for r in labeled)
    langs = Counter(r["lang"] for r in labeled)
    cross = {}
    for r in labeled:
        d, lv = r["domain"], r["judgment"]["final_risk_level"]
        cross.setdefault(d, Counter())[lv] += 1
    total = len(labeled)
    return {
        "total_samples": total,
        "level_distribution": dict(levels),
        "level_pct": {k: round(v / total * 100, 1) for k, v in levels.items()} if total else {},
        "domain_distribution": dict(domains),
        "lang_distribution": dict(langs),
        "domain_x_level": {k: dict(v) for k, v in cross.items()},
        "balanced": all(15 <= v / total * 100 <= 55 for v in levels.values()) if total else False,
    }


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mvp", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--judge", choices=["claude", "gemini"],
                        help="Force specific judge provider")
    args = parser.parse_args()

    providers = load_providers()

    # Select judge: user override > preference order
    if args.judge:
        judge_name = args.judge
    else:
        judge_name = next((n for n in JUDGE_PREFERENCE if n in providers), None)

    if not judge_name or judge_name not in providers:
        print(f"ERROR: no judge provider configured. Set ANTHROPIC_* or GOOGLE_API_KEY in .env",
              file=sys.stderr)
        print(f"Available providers: {list(providers.keys())}", file=sys.stderr)
        sys.exit(1)

    p = providers[judge_name]
    client = make_client(p)
    print(f"Meta-Judge: {p.name} ({p.model})")

    records = load_raw()
    if args.mvp:
        records = records[:60]
    elif args.limit:
        records = records[:args.limit]

    done_ids = set() if args.no_resume else load_labeled_ids()
    todo = [r for r in records if r["id"] not in done_ids]
    print(f"Total records: {len(records)} | Done: {len(done_ids)} | TODO: {len(todo)}")

    if not todo:
        print("Nothing to do.")
        if LABELED_PATH.exists():
            with open(LABELED_PATH, encoding="utf-8") as f:
                labeled = [json.loads(l) for l in f if l.strip()]
            stats = compute_stats(labeled)
            with open(STATS_PATH, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            print(json.dumps(stats.get("level_pct", {}), indent=2))
        return

    max_concurrent = int(os.getenv("MAX_CONCURRENT", "5"))
    sem = asyncio.Semaphore(max_concurrent)

    LABELED_PATH.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if args.no_resume else "a"

    t0 = time.time()
    ok, bad = 0, 0
    with open(LABELED_PATH, mode, encoding="utf-8") as fout:
        tasks = [process_one(r, client, p.model, sem) for r in todo]
        for coro in atqdm.as_completed(tasks, total=len(tasks), desc="Judging"):
            result = await coro
            if result:
                fout.write(json.dumps(result, ensure_ascii=False) + "\n")
                fout.flush()
                ok += 1
            else:
                bad += 1

    dt = time.time() - t0

    with open(LABELED_PATH, encoding="utf-8") as f:
        labeled = [json.loads(l) for l in f if l.strip()]
    stats = compute_stats(labeled)
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"Done in {dt:.1f}s ({len(todo)/max(dt, 0.01)*60:.1f} req/min)")
    print(f"  Labeled: {ok} | Failed: {bad}")
    print(f"\nRisk Level Distribution:")
    for lv in ("low", "medium", "high"):
        pct = stats["level_pct"].get(lv, 0)
        cnt = stats["level_distribution"].get(lv, 0)
        print(f"  {lv:8s}: {cnt:4d} ({pct:5.1f}%)")
    print(f"\nBalanced: {stats['balanced']}")
    print(f"Output: {LABELED_PATH}")
    print(f"Stats:  {STATS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
