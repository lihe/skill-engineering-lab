#!/usr/bin/env python3
"""运行 Skill Engineering Lab 的评测。"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grade_output import grade
from providers import PROVIDER_NAMES, get_provider
from providers.base import ProviderResult, SkillContext

CONFIGS = ["without_skill", "with_skill_v1", "with_skill_v2"]
BASELINE_TOKENS = 900


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["cases"]


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def stamp_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stamped = []
    for event in events:
        stamped.append({"ts": datetime.now(timezone.utc).isoformat(), **event})
    return stamped


def write_trace(path: Path, *, case: dict[str, Any], config: str, result: ProviderResult) -> None:
    events = [
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": "case_start",
            "case_id": case["id"],
            "config": config,
        },
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": "skill_routing",
            "skill": "ai-video-creator-style",
            "triggered": result.actual_triggered,
            "expected": case["should_trigger"],
            "provider": result.provider,
            "model": result.model,
        },
    ]
    events.extend(stamp_events(result.trace_events))
    path.write_text("\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n", encoding="utf-8")


def run_eval(
    skill: str,
    cases_path: Path,
    iteration: str,
    write_report: bool,
    provider_name: str,
    model: str | None,
) -> Path:
    cases = load_cases(cases_path)
    run_dir = ROOT / "runs" / iteration
    run_dir.mkdir(parents=True, exist_ok=True)
    provider = get_provider(provider_name, model=model)
    skill_context = SkillContext(
        skill=skill,
        iteration=iteration,
        root=ROOT,
        skill_dir=ROOT / "skills" / skill,
    )

    all_results = []
    started = datetime.now(timezone.utc).isoformat()

    for case in cases:
        case_dir = run_dir / case["id"]
        case_dir.mkdir(parents=True, exist_ok=True)
        write_json(case_dir / "case.json", case)

        for config in CONFIGS:
            cfg_dir = case_dir / config
            cfg_dir.mkdir(parents=True, exist_ok=True)
            provider_result = provider.generate(case=case, config=config, skill_context=skill_context)

            output_path = cfg_dir / "output.md"
            output_path.write_text(provider_result.output_text, encoding="utf-8")
            write_trace(cfg_dir / "trace.jsonl", case=case, config=config, result=provider_result)
            timing = {
                "duration_ms": provider_result.duration_ms,
                "token_estimate": provider_result.token_estimate,
                "simulated": provider_result.simulated,
                "provider": provider_result.provider,
                "model": provider_result.model,
            }
            write_json(cfg_dir / "timing.json", timing)
            write_json(
                cfg_dir / "provider.json",
                {
                    "provider": provider_result.provider,
                    "model": provider_result.model,
                    "simulated": provider_result.simulated,
                    "raw_usage": provider_result.raw_usage,
                },
            )

            grading = grade(
                case=case,
                config=config,
                output_text=provider_result.output_text,
                actual_triggered=provider_result.actual_triggered,
                token_estimate=provider_result.token_estimate,
                baseline_tokens=BASELINE_TOKENS,
            )
            write_json(cfg_dir / "grading.json", grading)
            all_results.append(
                {
                    "case_id": case["id"],
                    "case_type": case["case_type"],
                    "config": config,
                    "should_trigger": case["should_trigger"],
                    "actual_triggered": provider_result.actual_triggered,
                    "overall_pass": grading["overall_pass"],
                    "score_ratio": grading["score_ratio"],
                    "failure_patterns": grading["failure_patterns"],
                    "token_estimate": provider_result.token_estimate,
                    "duration_ms": provider_result.duration_ms,
                    "provider": provider_result.provider,
                    "model": provider_result.model,
                    "simulated": provider_result.simulated,
                }
            )

    benchmark = {
        "skill": skill,
        "iteration": iteration,
        "provider": provider.name,
        "model": provider.model,
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "cases": len(cases),
        "configs": CONFIGS,
        "results": all_results,
    }
    write_json(run_dir / "benchmark.json", benchmark)

    if write_report:
        from summarize_report import summarize

        report = summarize(run_dir)
        (run_dir / "report.md").write_text(report, encoding="utf-8")
        (ROOT / "report.md").write_text(report, encoding="utf-8")

    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", default="ai-video-creator-style")
    parser.add_argument("--cases", default=str(ROOT / "evals" / "cases.json"))
    parser.add_argument("--iteration", default="iteration-001")
    parser.add_argument("--provider", choices=PROVIDER_NAMES, default="mock")
    parser.add_argument("--model", default=None)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args()

    run_dir = run_eval(
        skill=args.skill,
        cases_path=Path(args.cases),
        iteration=args.iteration,
        write_report=not args.no_report,
        provider_name=args.provider,
        model=args.model,
    )
    print(f"已写入评测产物：{run_dir}")
    if not args.no_report:
        print(f"已写入报告：{run_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
