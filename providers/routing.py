"""Routing policies used by the demo provider adapters."""

from __future__ import annotations

from typing import Any


def should_trigger(config: str, case: dict[str, Any]) -> bool:
    """Return whether the skill should be routed for this config and case."""

    if config == "without_skill":
        return False
    if config == "with_skill_v2":
        return case["should_trigger"]

    # v1 会漏掉部分隐式/边界视频请求，也会误触发新闻稿样例。
    if case["id"] in {"boundary-sparse-brief", "extension-cover-only"}:
        return False
    if case["id"] == "negative-press-release":
        return True
    return case["should_trigger"]
