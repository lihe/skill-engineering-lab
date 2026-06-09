"""Provider interfaces for Skill Engineering Lab."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True)
class SkillContext:
    """Shared context passed to model providers."""

    skill: str
    iteration: str
    root: Path
    skill_dir: Path


@dataclass
class ProviderResult:
    """Normalized result returned by every provider."""

    output_text: str
    actual_triggered: bool
    token_estimate: int
    duration_ms: int
    simulated: bool
    provider: str
    model: str | None = None
    raw_usage: dict[str, Any] = field(default_factory=dict)
    trace_events: list[dict[str, Any]] = field(default_factory=list)


class Provider(Protocol):
    """Minimal provider contract used by scripts/run_eval.py."""

    name: str
    model: str | None

    def generate(
        self,
        *,
        case: dict[str, Any],
        config: str,
        skill_context: SkillContext,
    ) -> ProviderResult:
        """Generate one output for a single case/config pair."""
