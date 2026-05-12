"""
Unified LLM provider abstraction.
All 4 providers (DeepSeek, Zhipu, DashScope, Moonshot) speak OpenAI-compatible API,
so we use the openai SDK with different base_url/api_key/model for each.

Supports two modes:
1. Native endpoints (DEEPSEEK_BASE_URL, ZHIPU_BASE_URL, etc.)
2. SiliconFlow aggregator (one key, all models routed by model name)

Selection priority: if SILICONFLOW_API_KEY is set, it's used for any provider
that does not have its own native key set. Otherwise the native key is required.
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
    name: str              # logical name used in data records (deepseek / glm / qwen / kimi)
    model: str             # model name sent to the API
    api_key: str
    base_url: str
    label: str             # human-readable label used in judge prompts ("DeepSeek", "GLM", etc.)


# SiliconFlow model routing (when using the aggregator)
# Updated for 2026-05. Using Flash variants where available to stretch the 14 CNY free credit.
# Upgrade to Pro variants if you have paid credits.
SILICONFLOW_MODELS = {
    "deepseek": "deepseek-ai/DeepSeek-V4-Flash",     # or DeepSeek-V4-Pro for flagship quality
    "glm": "zai-org/GLM-4.5",                         # upgrade to GLM-5.1 if listed in your tier
    "qwen": "Qwen/Qwen3-235B-A22B",                   # or Qwen3.6-Plus-equivalent as listed
    "kimi": "moonshotai/Kimi-K2.6",                   # K2.6 for judge (released Apr 2026)
}


def _make_provider(name: str, label: str, native_key_var: str,
                   native_url_var: str, native_model_var: str) -> Optional[ProviderConfig]:
    """Build a ProviderConfig from env vars, with SiliconFlow fallback."""
    native_key = os.getenv(native_key_var)
    native_url = os.getenv(native_url_var)
    native_model = os.getenv(native_model_var)

    if native_key and native_url and native_model:
        return ProviderConfig(
            name=name, label=label,
            api_key=native_key, base_url=native_url, model=native_model,
        )

    # Fall back to SiliconFlow
    sf_key = os.getenv("SILICONFLOW_API_KEY")
    sf_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    if sf_key:
        return ProviderConfig(
            name=name, label=label,
            api_key=sf_key, base_url=sf_url, model=SILICONFLOW_MODELS[name],
        )

    return None


def load_providers() -> dict[str, ProviderConfig]:
    """Return {provider_name: ProviderConfig} for all configured providers."""
    candidates = [
        ("deepseek", "DeepSeek", "DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"),
        ("glm", "GLM", "ZHIPU_API_KEY", "ZHIPU_BASE_URL", "ZHIPU_MODEL"),
        ("qwen", "Qwen", "DASHSCOPE_API_KEY", "DASHSCOPE_BASE_URL", "DASHSCOPE_MODEL"),
        ("kimi", "Kimi", "MOONSHOT_API_KEY", "MOONSHOT_BASE_URL", "MOONSHOT_MODEL"),
    ]
    providers: dict[str, ProviderConfig] = {}
    for args in candidates:
        p = _make_provider(*args)
        if p:
            providers[p.name] = p
    return providers


def make_client(provider: ProviderConfig) -> AsyncOpenAI:
    """Build an AsyncOpenAI client for the given provider."""
    return AsyncOpenAI(
        api_key=provider.api_key,
        base_url=provider.base_url,
        timeout=float(os.getenv("REQUEST_TIMEOUT", "60")),
    )


if __name__ == "__main__":
    # Diagnostic: print which providers are configured
    providers = load_providers()
    if not providers:
        print("No providers configured. Set keys in .env file.")
    else:
        print(f"Configured providers ({len(providers)}):")
        for name, p in providers.items():
            # Mask the key
            masked = p.api_key[:6] + "..." + p.api_key[-4:] if len(p.api_key) > 10 else "***"
            print(f"  {name:10s} -> model={p.model}, key={masked}, url={p.base_url}")
