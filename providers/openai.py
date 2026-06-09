"""Optional OpenAI provider adapter.

The default project path uses the mock provider so the public demo stays
deterministic. This adapter exists to show the real-model boundary and can be
enabled with OPENAI_API_KEY.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from typing import Any

from .base import ProviderResult, SkillContext
from .routing import should_trigger


class OpenAIProvider:
    name = "openai"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate(
        self,
        *,
        case: dict[str, Any],
        config: str,
        skill_context: SkillContext,
    ) -> ProviderResult:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY 未设置，无法使用 openai provider。")

        triggered = should_trigger(config, case)
        prompt = build_prompt(case=case, config=config, triggered=triggered, skill_context=skill_context)
        payload = {"model": self.model, "input": prompt}

        start = time.perf_counter()
        response = self._post_json("https://api.openai.com/v1/responses", payload)
        duration_ms = int((time.perf_counter() - start) * 1000)

        output_text = extract_responses_text(response)
        usage = response.get("usage", {})
        token_estimate = usage.get("total_tokens") or usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
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
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))


def build_prompt(
    *,
    case: dict[str, Any],
    config: str,
    triggered: bool,
    skill_context: SkillContext,
) -> str:
    skill_text = ""
    if triggered and config != "without_skill":
        version = "v2" if config == "with_skill_v2" else "v1"
        skill_path = skill_context.skill_dir / version / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")

    return f"""你正在运行 Skill Engineering Lab 的真实模型适配层。

评测配置：{config}
是否路由 Skill：{triggered}

用户原始请求：
{case["prompt"]}

产品 brief：
{json.dumps(case["brief"], ensure_ascii=False, indent=2)}

Skill 说明：
{skill_text or "本轮不加载 Skill，请按普通助手输出。"}

请只输出最终交付内容，不要解释评测系统。"""


def extract_responses_text(response: dict[str, Any]) -> str:
    if response.get("output_text"):
        return str(response["output_text"])

    texts: list[str] = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                texts.append(text)
    return "\n".join(texts).strip()
