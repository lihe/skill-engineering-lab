#!/usr/bin/env python3
"""Summarize a Skill Engineering Lab run as Markdown."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


CONFIG_LABELS = {
    "without_skill": "without_skill",
    "with_skill_v1": "with_skill v1",
    "with_skill_v2": "with_skill v2",
}


def load_benchmark(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "benchmark.json").read_text(encoding="utf-8"))


def config_results(benchmark: dict[str, Any], config: str) -> list[dict[str, Any]]:
    return [result for result in benchmark["results"] if result["config"] == config]


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def pass_rate(results: list[dict[str, Any]]) -> float:
    if not results:
        return 0.0
    return sum(1 for result in results if result["overall_pass"]) / len(results)


def trigger_recall(results: list[dict[str, Any]]) -> float:
    positives = [result for result in results if result["should_trigger"]]
    if not positives:
        return 0.0
    return sum(1 for result in positives if result["actual_triggered"]) / len(positives)


def over_trigger_rate(results: list[dict[str, Any]]) -> float:
    negatives = [result for result in results if not result["should_trigger"]]
    if not negatives:
        return 0.0
    return sum(1 for result in negatives if result["actual_triggered"]) / len(negatives)


def avg_token(results: list[dict[str, Any]]) -> float:
    return mean(result["token_estimate"] for result in results) if results else 0.0


def avg_duration(results: list[dict[str, Any]]) -> float:
    return mean(result["duration_ms"] for result in results) if results else 0.0


def failure_summary(results: list[dict[str, Any]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for result in results:
        counter.update(result["failure_patterns"])
    return counter


def top_badcases(benchmark: dict[str, Any], config: str, limit: int = 5) -> list[dict[str, Any]]:
    results = [result for result in config_results(benchmark, config) if not result["overall_pass"]]
    return sorted(results, key=lambda result: (result["score_ratio"], result["case_id"]))[:limit]


def decision(v2_results: list[dict[str, Any]], v1_results: list[dict[str, Any]]) -> str:
    v2_pass = pass_rate(v2_results)
    v1_pass = pass_rate(v1_results)
    v2_over = over_trigger_rate(v2_results)
    if v2_pass >= 0.85 and v2_over == 0:
        return "ship"
    if v2_pass > v1_pass:
        return "iterate"
    return "split_or_rewrite"


def metric_table(benchmark: dict[str, Any]) -> str:
    lines = [
        "| Config | Pass Rate | Trigger Recall | Over-trigger | Avg Tokens | Avg Time |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for config in benchmark["configs"]:
        results = config_results(benchmark, config)
        lines.append(
            "| {label} | {pass_rate} | {trigger} | {over} | {tokens:.0f} | {time:.0f} ms |".format(
                label=CONFIG_LABELS[config],
                pass_rate=pct(pass_rate(results)),
                trigger="n/a" if config == "without_skill" else pct(trigger_recall(results)),
                over="n/a" if config == "without_skill" else pct(over_trigger_rate(results)),
                tokens=avg_token(results),
                time=avg_duration(results),
            )
        )
    return "\n".join(lines)


def lift_table(benchmark: dict[str, Any]) -> str:
    base = config_results(benchmark, "without_skill")
    v1 = config_results(benchmark, "with_skill_v1")
    v2 = config_results(benchmark, "with_skill_v2")
    base_pass = pass_rate(base)
    v1_pass = pass_rate(v1)
    v2_pass = pass_rate(v2)
    base_tokens = avg_token(base)
    v1_tokens = avg_token(v1)
    v2_tokens = avg_token(v2)
    return "\n".join(
        [
            "| Comparison | Quality Lift | Token Delta |",
            "| --- | ---: | ---: |",
            f"| v1 vs baseline | {pct(v1_pass - base_pass)} | {pct((v1_tokens - base_tokens) / base_tokens)} |",
            f"| v2 vs baseline | {pct(v2_pass - base_pass)} | {pct((v2_tokens - base_tokens) / base_tokens)} |",
            f"| v2 vs v1 | {pct(v2_pass - v1_pass)} | {pct((v2_tokens - v1_tokens) / v1_tokens)} |",
        ]
    )


def badcase_table(benchmark: dict[str, Any], config: str) -> str:
    badcases = top_badcases(benchmark, config)
    if not badcases:
        return "No failing badcases."
    lines = [
        "| Case | Type | Score | Failure Patterns |",
        "| --- | --- | ---: | --- |",
    ]
    for result in badcases:
        lines.append(
            f"| `{result['case_id']}` | {result['case_type']} | {pct(result['score_ratio'])} | {', '.join(result['failure_patterns']) or 'none'} |"
        )
    return "\n".join(lines)


def failure_pattern_table(benchmark: dict[str, Any]) -> str:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for config in benchmark["configs"]:
        grouped[config] = failure_summary(config_results(benchmark, config))
    all_patterns = sorted({pattern for counter in grouped.values() for pattern in counter})
    if not all_patterns:
        return "No failure patterns recorded."
    lines = [
        "| Pattern | without_skill | v1 | v2 | Suggested Action |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    actions = {
        "trigger_mismatch": "Tighten or broaden `description` boundaries.",
        "outcome_incomplete": "Harden required output checklist.",
        "style_weak": "Improve references and examples.",
        "efficiency_cost": "Move deterministic checks into scripts and trim references.",
        "generalization_risk": "Add paraphrase/boundary cases to regression set.",
    }
    for pattern in all_patterns:
        lines.append(
            "| {pattern} | {base} | {v1} | {v2} | {action} |".format(
                pattern=pattern,
                base=grouped["without_skill"][pattern],
                v1=grouped["with_skill_v1"][pattern],
                v2=grouped["with_skill_v2"][pattern],
                action=actions.get(pattern, "Review badcase."),
            )
        )
    return "\n".join(lines)


def summarize(run_dir: Path) -> str:
    benchmark = load_benchmark(run_dir)
    base = config_results(benchmark, "without_skill")
    v1 = config_results(benchmark, "with_skill_v1")
    v2 = config_results(benchmark, "with_skill_v2")
    final_decision = decision(v2, v1)

    return f"""# Skill Engineering Lab Report

## Summary

Skill: `{benchmark['skill']}`  
Iteration: `{benchmark['iteration']}`  
Cases: {benchmark['cases']}  
Decision: **{final_decision}**

This lab compares the same evaluation set across three states:

```text
without_skill -> with_skill v1 -> with_skill v2
```

The point is not that the generated video copy is beautiful. The point is that Skill behavior becomes observable, gradable, and improvable.

## Metrics

{metric_table(benchmark)}

## Lift

{lift_table(benchmark)}

## What Changed From v1 To v2

- `description` now includes negative boundaries: no press releases, project plans, issue triage, or generic non-video writing.
- `SKILL.md` now has a clear output contract: titles, cover text, demo plan, outline, script, self-check.
- Required checks are hardened: title count, cover line length, demo-first opening, old/new contrast.
- A deterministic verifier script exists for package structure and line-length checks.

## Top v1 Badcases

{badcase_table(benchmark, "with_skill_v1")}

## Top v2 Badcases

{badcase_table(benchmark, "with_skill_v2")}

## Failure Pattern Diagnosis

{failure_pattern_table(benchmark)}

## Governance Assets Created

- `evals/cases.json`: 12-case seed eval set.
- `runs/{benchmark['iteration']}/benchmark.json`: benchmark summary.
- `runs/{benchmark['iteration']}/*/trace.jsonl`: routing and reference-loading traces.
- `runs/{benchmark['iteration']}/*/grading.json`: structured grading output.
- `skills/ai-video-creator-style/scripts/validate_package.py`: deterministic verifier.
- `governance/versions.json`: version hypotheses, risks, metrics, and decisions.
- `governance/reason_archive.json`: badcase root-cause archive.
- `governance/regression_set.json`: must-keep regression cases.

## Next Actions

1. Add 3-5 real product briefs from past work as regression cases.
2. Replace the deterministic simulator with real LLM calls behind the same grading interface.
3. Add a small HTML dashboard if this will be used in live workshops.
4. Track future v3 changes in `governance/versions.json`.
5. Keep negative cases in the regression set to prevent over-triggering.
"""


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    report = summarize(run_dir)
    (run_dir / "report.md").write_text(report, encoding="utf-8")
    (run_dir.parents[1] / "report.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
