"""
Unified LLM provider abstraction.

5 logical providers across 3 physical endpoints:
    deepseek  -]
    glm       -+-- SiliconFlow aggregator   (1 key, 3 models)
    qwen      -]
    gemini        -- Google AI Studio OpenAI-compatible endpoint (free tier)
    claude        -- User's OpenAI-compatible proxy (api123.top style) [Judge]

All endpoints speak OpenAI-compatible HTTP so we reuse the `openai` SDK.
Which provider is data-source vs judge is decided by the caller, not here.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


@dataclass
class ProviderConfig:
    name: str       # logical name in records (deepseek / glm / qwen / gemini / claude)
    model: str      # exact model name sent to the API
    api_key: str
    base_url: str
    label: str      # display name used in prompts ("DeepSeek", "GLM", ...)


# SiliconFlow model routing (2026-05).
# FREE TIER models (confirmed working with 16 CNY signup credit):
#   deepseek-ai/DeepSeek-V3       ← free
#   zai-org/GLM-4.5               ← free
#   Qwen/Qwen3-235B-A22B          ← free
# PAID models (will 403 "Model is private" on free accounts):
#   deepseek-ai/DeepSeek-V4-Pro   ← requires paid plan
#   deepseek-ai/DeepSeek-V4-Flash ← requires paid plan
# Override in .env if you have paid access:
#   DEEPSEEK_SF_MODEL=deepseek-ai/DeepSeek-V4-Pro
# CONFIRMED FREE on SiliconFlow 16 CNY signup credit (May 2026):
SILICONFLOW_MODELS = {
    "deepseek": "deepseek-ai/DeepSeek-V3",
    "qwen": "Qwen/Qwen2.5-7B-Instruct",
    # Below are PAID-ONLY (403 on free accounts), kept for reference:
    # "glm": "zai-org/GLM-4.5",
    # "qwen_big": "Qwen/Qwen3-235B-A22B",
}

GEMINI_DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
GEMINI_DEFAULT_MODEL = "gemini-2.5-flash"


def _siliconflow(name: str, label: str) -> Optional[ProviderConfig]:
    sf_key = os.getenv("SILICONFLOW_API_KEY")
    if not sf_key:
        return None
    sf_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    model = os.getenv(f"{name.upper()}_SF_MODEL", SILICONFLOW_MODELS[name])
    return ProviderConfig(name=name, label=label, api_key=sf_key,
                          base_url=sf_url, model=model)


def _gemini() -> Optional[ProviderConfig]:
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    return ProviderConfig(
        name="gemini", label="Gemini",
        api_key=key,
        base_url=os.getenv("GEMINI_BASE_URL", GEMINI_DEFAULT_BASE_URL),
        model=os.getenv("GEMINI_MODEL", GEMINI_DEFAULT_MODEL),
    )


def _claude() -> Optional[ProviderConfig]:
    key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
    url = os.getenv("ANTHROPIC_BASE_URL") or os.getenv("CLAUDE_BASE_URL")
    model = os.getenv("ANTHROPIC_MODEL") or os.getenv("CLAUDE_MODEL")
    if not (key and url and model):
        return None
    return ProviderConfig(name="claude", label="Claude",
                          api_key=key, base_url=url, model=model)


def load_providers() -> dict[str, ProviderConfig]:
    """Return {provider_name: ProviderConfig} for all configured providers."""
    providers: dict[str, ProviderConfig] = {}
    # Only build SiliconFlow providers for models listed in SILICONFLOW_MODELS
    sf_labels = {"deepseek": "DeepSeek", "qwen": "Qwen"}
    for name, label in sf_labels.items():
        if name in SILICONFLOW_MODELS:
            p = _siliconflow(name, label)
            if p:
                providers[name] = p
    for builder in (_gemini, _claude):
        p = builder()
        if p:
            providers[p.name] = p
    return providers


def make_client(provider: ProviderConfig) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=provider.api_key,
        base_url=provider.base_url,
        timeout=float(os.getenv("REQUEST_TIMEOUT", "60")),
    )


if __name__ == "__main__":
    providers = load_providers()
    if not providers:
        print("No providers configured. Set keys in .env file.")
    else:
        print(f"Configured providers ({len(providers)}):")
        for name, p in providers.items():
            masked = p.api_key[:6] + "..." + p.api_key[-4:] if len(p.api_key) > 10 else "***"
            print(f"  {name:10s} -> model={p.model}")
            print(f"             key={masked}  url={p.base_url}")
