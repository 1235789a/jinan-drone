"""
Day 1 - Step 2: Concurrent multi-model response collection (API, zero human touch)

For each seed question, query all configured DATA-SOURCE models in parallel.
- Resume-safe: already-processed ids in the output file are skipped
- Per-provider rate limiting via independent semaphores
- Real-time JSONL writes (no data loss on crash)
- tqdm progress bar

Usage:
    python scripts/call_models.py              # process all seeds.jsonl
    python scripts/call_models.py --mvp        # only first 60
    python scripts/call_models.py --limit 100  # only first N
    python scripts/call_models.py --no-resume  # ignore existing output
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from tqdm.asyncio import tqdm as atqdm

from providers import load_providers, make_client

SEEDS_PATH = Path(__file__).parent.parent / "data" / "seeds.jsonl"
RAW_RESPONSES_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"

# Data-source providers. `claude` is reserved for the Judge, not queried here.
# Only DeepSeek and Qwen confirmed working on SiliconFlow free tier (May 2026).
# GLM-4.5 and Gemini both 403/rate-limit on free accounts.
DATA_SOURCES = ["deepseek", "qwen"]

SYSTEM_PROMPT = """You are a deterministic answer API.

## Answer Rules
1. Answer from your internal parameter knowledge. Do not hedge with "I need to search" or "consult an expert".
2. Each answer must be 80-160 words. No shorter, no longer.
3. Plain text only. No markdown, no bullets, no headers, no bold.
4. No disclaimers like "consult a doctor/lawyer". Answer the actual question.
5. Keep your natural voice: if confident be confident, if uncertain say so. Do not artificially hedge or over-commit.
6. Reply in the SAME LANGUAGE as the question.
7. Do not show reasoning steps. Output only the final answer.
8. No preamble like "Here is the answer:"."""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
async def call_one_model(client, model: str, question: str) -> str:
    resp = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    return (resp.choices[0].message.content or "").strip()


async def process_one_seed(
    seed: dict,
    clients: dict,
    semaphores: dict,
) -> dict:
    async def _one(provider_name: str):
        client, model = clients[provider_name]
        sem = semaphores[provider_name]
        async with sem:
            try:
                answer = await call_one_model(client, model, seed["question"])
                return provider_name, answer, None
            except Exception as e:
                return provider_name, None, f"{type(e).__name__}: {str(e)[:120]}"

    results = await asyncio.gather(*[_one(name) for name in clients.keys()])
    responses, errors = {}, {}
    for name, answer, err in results:
        if answer:
            responses[name] = answer
        if err:
            errors[name] = err

    return {
        "id": seed["id"],
        "domain": seed["domain"],
        "subtopic": seed.get("subtopic", ""),
        "lang": seed.get("lang", "en"),
        "question": seed["question"],
        "responses": responses,
        "errors": errors,
    }


def load_seeds() -> list:
    if not SEEDS_PATH.exists():
        print(f"ERROR: {SEEDS_PATH} not found. Run generate_seeds.py first.", file=sys.stderr)
        sys.exit(1)
    seeds = []
    with open(SEEDS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))
    return seeds


def load_completed_ids(min_responses: int) -> set:
    """Read already-processed ids with enough valid responses (for resume)."""
    done = set()
    if RAW_RESPONSES_PATH.exists():
        with open(RAW_RESPONSES_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if len(obj.get("responses", {})) >= min_responses:
                        done.add(obj["id"])
                except json.JSONDecodeError:
                    continue
    return done


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mvp", action="store_true", help="Process only first 60 seeds")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--min-responses", type=int, default=3,
                        help="Min valid responses per seed to be considered 'done' (default 3)")
    args = parser.parse_args()

    providers = load_providers()
    configured_sources = [n for n in DATA_SOURCES if n in providers]
    missing = [n for n in DATA_SOURCES if n not in providers]

    if len(configured_sources) < 2:
        print(f"ERROR: need at least 2 data-source providers, got {configured_sources}",
              file=sys.stderr)
        print(f"Configure at least 2 of: {DATA_SOURCES}", file=sys.stderr)
        sys.exit(1)

    if missing:
        print(f"WARN: data-source providers missing from .env: {missing}")
        print(f"      proceeding with {len(configured_sources)} providers: {configured_sources}")

    clients = {}
    for name in configured_sources:
        p = providers[name]
        clients[name] = (make_client(p), p.model)
        print(f"  Data source [{name:8s}] -> {p.model}")

    max_concurrent = int(os.getenv("MAX_CONCURRENT", "5"))
    semaphores = {name: asyncio.Semaphore(max_concurrent) for name in configured_sources}

    seeds = load_seeds()
    if args.mvp:
        seeds = seeds[:60]
    elif args.limit:
        seeds = seeds[:args.limit]

    done_ids = set() if args.no_resume else load_completed_ids(
        min_responses=min(args.min_responses, len(configured_sources)))
    todo = [s for s in seeds if s["id"] not in done_ids]

    print(f"\nTotal seeds: {len(seeds)} | Done: {len(done_ids)} | TODO: {len(todo)}")
    if not todo:
        print("Nothing to do. Use --no-resume to reprocess.")
        return

    RAW_RESPONSES_PATH.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if args.no_resume else "a"

    t0 = time.time()
    success, partial, failed = 0, 0, 0

    with open(RAW_RESPONSES_PATH, mode, encoding="utf-8") as fout:
        tasks = [process_one_seed(seed, clients, semaphores) for seed in todo]
        for coro in atqdm.as_completed(tasks, total=len(tasks), desc="Calling models"):
            result = await coro
            n_valid = len(result["responses"])
            if n_valid == len(configured_sources):
                success += 1
            elif n_valid >= 2:
                partial += 1
            else:
                failed += 1
                continue
            fout.write(json.dumps(result, ensure_ascii=False) + "\n")
            fout.flush()

    dt = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"Done in {dt:.1f}s ({len(todo)/max(dt, 0.01)*60:.1f} req/min)")
    print(f"  Full ({len(configured_sources)}/{len(configured_sources)}): {success}")
    print(f"  Partial (>=2):                    {partial}")
    print(f"  Failed (<2):                      {failed}")
    print(f"  Output: {RAW_RESPONSES_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
