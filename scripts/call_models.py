"""
Day 1 - Step 2: 多模型并发调用脚本
对每个种子问题，分别调用 GPT-4o, Claude 3.5, Gemini 1.5 获取回答。
"""

import json
import asyncio
import os
from pathlib import Path
from typing import Optional

# --- Configuration ---
SEEDS_PATH = Path(__file__).parent.parent / "seeds" / "generated_seeds.jsonl"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "raw_responses.jsonl"

# API Keys (从环境变量读取)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Rate limiting
MAX_CONCURRENT = 5
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds


async def call_openai(question: str) -> Optional[str]:
    """调用 GPT-4o"""
    # TODO: 实现真实 API 调用
    # import openai
    # client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    # response = await client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[{"role": "user", "content": question}],
    #     temperature=0.7,
    #     max_tokens=500,
    # )
    # return response.choices[0].message.content
    return f"[GPT-4o placeholder response for: {question[:50]}...]"


async def call_anthropic(question: str) -> Optional[str]:
    """调用 Claude 3.5 Sonnet"""
    # TODO: 实现真实 API 调用
    # import anthropic
    # client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    # response = await client.messages.create(
    #     model="claude-3-5-sonnet-20241022",
    #     max_tokens=500,
    #     messages=[{"role": "user", "content": question}],
    # )
    # return response.content[0].text
    return f"[Claude placeholder response for: {question[:50]}...]"


async def call_gemini(question: str) -> Optional[str]:
    """调用 Gemini 1.5 Pro"""
    # TODO: 实现真实 API 调用
    # import google.generativeai as genai
    # genai.configure(api_key=GOOGLE_API_KEY)
    # model = genai.GenerativeModel("gemini-1.5-pro")
    # response = await model.generate_content_async(question)
    # return response.text
    return f"[Gemini placeholder response for: {question[:50]}...]"


async def process_single_question(semaphore, seed: dict) -> dict:
    """处理单个问题：并发调用三个模型"""
    async with semaphore:
        question = seed["question"]
        
        # 并发调用三个模型
        results = await asyncio.gather(
            call_openai(question),
            call_anthropic(question),
            call_gemini(question),
            return_exceptions=True,
        )

        return {
            "question": question,
            "domain": seed["domain"],
            "subtopic": seed["subtopic"],
            "responses": {
                "gpt4o": results[0] if not isinstance(results[0], Exception) else None,
                "claude": results[1] if not isinstance(results[1], Exception) else None,
                "gemini": results[2] if not isinstance(results[2], Exception) else None,
            },
            "errors": {
                "gpt4o": str(results[0]) if isinstance(results[0], Exception) else None,
                "claude": str(results[1]) if isinstance(results[1], Exception) else None,
                "gemini": str(results[2]) if isinstance(results[2], Exception) else None,
            },
        }


async def main():
    # Load seeds
    seeds = []
    with open(SEEDS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            seeds.append(json.loads(line))

    print(f"📋 Loaded {len(seeds)} seed questions")
    print(f"🔄 Processing with max {MAX_CONCURRENT} concurrent requests...")

    # Process with rate limiting
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = [process_single_question(semaphore, seed) for seed in seeds]
    results = await asyncio.gather(*tasks)

    # Write results
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    success_count = 0
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for result in results:
            # Only write if at least 2 models responded
            valid_responses = sum(1 for v in result["responses"].values() if v is not None)
            if valid_responses >= 2:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                success_count += 1

    print(f"\n✅ Collected {success_count}/{len(seeds)} complete response sets")
    print(f"   Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
