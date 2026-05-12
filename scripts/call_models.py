"""
Day 1 - Step 2: 三模型并发调用 (API 版本，零人工)

对每条种子问题，并发调用 DeepSeek / GLM / Qwen 获取回答。
- 断点续传：已完成的 id 不会重复调用
- 实时写入 JSONL：中途挂了也不会丢数据
- 并发限流：每个 provider 独立 semaphore
- 进度条 + 实时统计

使用:
    python scripts/call_models.py              # 处理所有 seeds.jsonl
    python scripts/call_models.py --mvp        # 只处理前 60 条
    python scripts/call_models.py --limit 100  # 只处理前 N 条
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

from providers import ProviderConfig, load_providers, make_client

SEEDS_PATH = Path(__file__).parent.parent / "data" / "seeds.jsonl"
RAW_RESPONSES_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"

DATA_SOURCES = ["deepseek", "glm", "qwen"]  # Kimi reserved for judge

SYSTEM_PROMPT = """You are a deterministic answer API.

## Answer Rules
1. Answer from your internal parameter knowledge. DO NOT add "I need to search" or "please consult an expert".
2. Each answer must be 80-160 words. No shorter, no longer.
3. Plain text only. No markdown, no bullets, no headers, no bold.
4. Do NOT add disclaimers like "consult a doctor/lawyer". Answer the actual question directly.
5. Maintain your natural reasoning style: if you are confident, be confident; if uncertain, express it. Do not artificially hedge or over-commit.
6. Reply in the SAME LANGUAGE as the question (English in, English out; 中文问,中文答).
7. Do NOT show reasoning steps. Just the final answer.
8. Output the answer as plain text, no preamble like "Here is the answer:"."""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
async def call_one_model(client, model: str, question: str) -> str:
    """Call a single model, with retry."""
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
    clients: dict[str, tuple],  # name -> (client, model)
    semaphores: dict[str, asyncio.Semaphore],
) -> dict:
    """Query all configured data-source models for one question."""
    async def _one(provider_name: str) -> tuple[str, str | None, str | None]:
        client, model = clients[provider_name]
        sem = semaphores[provider_name]
        async with sem:
            try:
                answer = await call_one_model(client, model, seed["question"])
                return provider_name, answer, None
            except Exception as e:
                return provider_name, None, f"{type(e).__name__}: {str(e)[:120]}"

    results = await asyncio.gather(*[_one(name) for name in clients.keys()])

    responses = {}
    errors = {}
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


def load_seeds() -> list[dict]:
    if not SEEDS_PATH.exists():
        print(f"ERROR: {SEEDS_PATH} not found. Run generate_seeds.py first.",
              file=sys.stderr)
        sys.exit(1)
    seeds = []
    with open(SEEDS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))
    return seeds


def load_completed_ids() -> set[int]:
    """Read already-processed ids from the output file (for resume)."""
    done = set()
    if RAW_RESPONSES_PATH.exists():
        with open(RAW_RESPONSES_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    # Require at least 2 valid responses to count as "done"
                    if len(obj.get("responses", {})) >= 2:
                        done.add(obj["id"])
                except json.JSONDecodeError:
                    continue
    return done


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mvp", action="store_true", help="Process only first 60 seeds")
    parser.add_argument("--limit", type=int, help="Process only first N seeds")
    parser.add_argument("--no-resume", action="store_true",
                        help="Ignore existing output and reprocess all")
    args = parser.parse_args()

    # Load providers
    providers = load_providers()
    missing = [name for name in DATA_SOURCES if name not in providers]
    if missing:
        print(f"ERROR: missing data-source providers: {missing}", file=sys.stderr)
        print(f"Configured: {list(providers.keys())}", file=sys.stderr)
        sys.exit(1)

    clients: dict[str, tuple] = {}
    for name in DATA_SOURCES:
        p = providers[name]
        clients[name] = (make_client(p), p.model)

    # Per-provider semaphore (each provider has its own rate limits)
    max_concurrent = int(os.getenv("MAX_CONCURRENT", "5"))
    semaphores = {name: asyncio.Semaphore(max_concurrent) for name in DATA_SOURCES}

    # Load seeds + filter
    seeds = load_seeds()
    if args.mvp:
        seeds = seeds[:60]
    elif args.limit:
        seeds = seeds[:args.limit]

    done_ids = set() if args.no_resume else load_completed_ids()
    todo = [s for s in seeds if s["id"] not in done_ids]

    print(f"Total seeds: {len(seeds)} | Already done: {len(done_ids)} | TODO: {len(todo)}")
    if not todo:
        print("Nothing to do. Use --no-resume to reprocess.")
        return

    # Process with progress bar; write as we go
    RAW_RESPONSES_PATH.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if args.no_resume else "a"

    t0 = time.time()
    success = 0
    partial = 0
    failed = 0

    with open(RAW_RESPONSES_PATH, mode, encoding="utf-8") as fout:
        tasks = [process_one_seed(seed, clients, semaphores) for seed in todo]
        for coro in atqdm.as_completed(tasks, total=len(tasks), desc="Calling models"):
            result = await coro
            n_valid = len(result["responses"])
            if n_valid == 3:
                success += 1
            elif n_valid >= 2:
                partial += 1
            else:
                failed += 1
                continue  # skip writing records with <2 valid responses
            fout.write(json.dumps(result, ensure_ascii=False) + "\n")
            fout.flush()

    dt = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"Done in {dt:.1f}s ({len(todo)/dt*60:.1f} req/min)")
    print(f"  Full success (3/3):  {success}")
    print(f"  Partial (2/3):       {partial}")
    print(f"  Failed (<2/3):       {failed}")
    print(f"  Output: {RAW_RESPONSES_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
