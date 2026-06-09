"""Provider registry for Skill Engineering Lab."""

from __future__ import annotations

from .anthropic import AnthropicProvider
from .mock import MockProvider
from .openai import OpenAIProvider


PROVIDER_NAMES = ("mock", "openai", "anthropic")


def get_provider(name: str, model: str | None = None):
    normalized = name.strip().lower()
    if normalized == "mock":
        return MockProvider(model=model)
    if normalized == "openai":
        return OpenAIProvider(model=model)
    if normalized == "anthropic":
        return AnthropicProvider(model=model)
    raise ValueError(f"未知 provider：{name}，可选值：{', '.join(PROVIDER_NAMES)}")
