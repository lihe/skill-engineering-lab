"""Optional Anthropic provider adapter."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from typing import Any

from .base import ProviderResult, SkillContext
from .openai import build_prompt
from .routing import should_trigger


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def generate(
        self,
        *,
        case: dict[str, Any],
        config: str,
        skill_context: SkillContext,
    ) -> ProviderResult:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY 未设置，无法使用 anthropic provider。")

        triggered = should_trigger(config, case)
        prompt = build_prompt(case=case, config=config, triggered=triggered, skill_context=skill_context)
        payload = {
            "model": self.model,
            "max_tokens": 2600,
            "messages": [{"role": "user", "content": prompt}],
        }

        start = time.perf_counter()
        response = self._post_json("https://api.anthropic.com/v1/messages", payload)
        duration_ms = int((time.perf_counter() - start) * 1000)

        output_text = "\n".join(
            block.get("text", "") for block in response.get("content", []) if block.get("type") == "text"
        ).strip()
        usage = response.get("usage", {})
        token_estimate = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
        if not token_estimate:
            token_estimate = max(1, len(prompt + output_text) // 2)

        return ProviderResult(
            output_text=output_text,
            actual_triggered=triggered,
            token_estimate=int(token_estimate),
            duration_ms=duration_ms,
            simulated=False,
            provider=self.name,
            model=self.model,
            raw_usage=usage,
            trace_events=[
                {
                    "event": "provider_generate",
                    "provider": self.name,
                    "model": self.model,
                    "simulated": False,
                    "routing_policy": config,
                }
            ],
        )

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": self.api_key or "",
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
