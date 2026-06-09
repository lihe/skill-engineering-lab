#!/usr/bin/env python3
"""Build static dashboard data from evaluation and governance assets."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_LABELS = {
    "without_skill": "无 Skill",
    "with_skill_v1": "Skill v1",
    "with_skill_v2": "Skill v2",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(value: float) -> float:
    return round(value * 100, 1)


def results_for(benchmark: dict[str, Any], config: str) -> list[dict[str, Any]]:
    return [item for item in benchmark["results"] if item["config"] == config]


def pass_rate(results: list[dict[str, Any]]) -> float:
    return sum(1 for item in results if item["overall_pass"]) / len(results) if results else 0.0


def trigger_recall(results: list[dict[str, Any]]) -> float | None:
    positives = [item for item in results if item["should_trigger"]]
    if not positives:
        return None
    return sum(1 for item in positives if item["actual_triggered"]) / len(positives)


def over_trigger_rate(results: list[dict[str, Any]]) -> float | None:
    negatives = [item for item in results if not item["should_trigger"]]
    if not negatives:
        return None
    return sum(1 for item in negatives if item["actual_triggered"]) / len(negatives)


def avg_number(results: list[dict[str, Any]], field: str) -> float:
    return round(mean(item[field] for item in results), 1) if results else 0.0


def metric_rows(benchmark: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for config in benchmark["configs"]:
        rows_for_config = results_for(benchmark, config)
        recall = trigger_recall(rows_for_config)
        over = over_trigger_rate(rows_for_config)
        rows.append(
            {
                "config": config,
                "label": CONFIG_LABELS.get(config, config),
                "passRate": pct(pass_rate(rows_for_config)),
                "triggerRecall": None if config == "without_skill" else pct(recall or 0),
                "overTriggerRate": None if config == "without_skill" else pct(over or 0),
                "avgTokens": avg_number(rows_for_config, "token_estimate"),
                "avgDurationMs": avg_number(rows_for_config, "duration_ms"),
            }
        )
    return rows


def failure_pattern_rows(benchmark: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for config in benchmark["configs"]:
        for result in results_for(benchmark, config):
            grouped[config].update(result["failure_patterns"])
    patterns = sorted({pattern for counter in grouped.values() for pattern in counter})
    return [
        {
            "pattern": pattern,
            "withoutSkill": grouped["without_skill"][pattern],
            "skillV1": grouped["with_skill_v1"][pattern],
            "skillV2": grouped["with_skill_v2"][pattern],
        }
        for pattern in patterns
    ]


def case_type_rows(benchmark: dict[str, Any]) -> list[dict[str, Any]]:
    seen = {}
    for result in benchmark["results"]:
        seen[result["case_id"]] = result["case_type"]
    counter = Counter(seen.values())
    labels = {
        "core": "核心",
        "boundary": "边界",
        "extension": "扩展",
        "negative": "负向",
    }
    return [{"type": key, "label": labels.get(key, key), "count": counter[key]} for key in sorted(counter)]


def top_badcases(benchmark: dict[str, Any], config: str) -> list[dict[str, Any]]:
    failures = [item for item in results_for(benchmark, config) if not item["overall_pass"]]
    failures.sort(key=lambda item: (item["score_ratio"], item["case_id"]))
    return [
        {
            "caseId": item["case_id"],
            "caseType": item["case_type"],
            "score": pct(item["score_ratio"]),
            "failurePatterns": item["failure_patterns"],
        }
        for item in failures[:5]
    ]


def case_matrix(benchmark: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for item in benchmark["results"]:
        case = grouped.setdefault(
            item["case_id"],
            {
                "caseId": item["case_id"],
                "caseType": item["case_type"],
                "shouldTrigger": item["should_trigger"],
                "configs": {},
            },
        )
        case["configs"][item["config"]] = {
            "pass": item["overall_pass"],
            "score": pct(item["score_ratio"]),
            "triggered": item["actual_triggered"],
            "tokens": item["token_estimate"],
            "durationMs": item["duration_ms"],
            "failurePatterns": item["failure_patterns"],
        }
    return list(grouped.values())


def build_payload(run_dir: Path) -> dict[str, Any]:
    benchmark = load_json(run_dir / "benchmark.json")
    versions = load_json(ROOT / "governance" / "versions.json")
    reason_archive = load_json(ROOT / "governance" / "reason_archive.json")
    regression_set = load_json(ROOT / "governance" / "regression_set.json")

    metrics = metric_rows(benchmark)
    base = next(item for item in metrics if item["config"] == "without_skill")
    v1 = next(item for item in metrics if item["config"] == "with_skill_v1")
    v2 = next(item for item in metrics if item["config"] == "with_skill_v2")

    return {
        "generatedAt": benchmark["finished_at"],
        "skill": benchmark["skill"],
        "iteration": benchmark["iteration"],
        "cases": benchmark["cases"],
        "metrics": metrics,
        "headline": {
            "passLiftV2VsBase": round(v2["passRate"] - base["passRate"], 1),
            "passLiftV2VsV1": round(v2["passRate"] - v1["passRate"], 1),
            "overTriggerDrop": round(v1["overTriggerRate"] - v2["overTriggerRate"], 1),
            "tokenDeltaV2VsV1": round((v2["avgTokens"] - v1["avgTokens"]) / v1["avgTokens"] * 100, 1),
        },
        "failurePatterns": failure_pattern_rows(benchmark),
        "caseTypes": case_type_rows(benchmark),
        "topBadcasesV1": top_badcases(benchmark, "with_skill_v1"),
        "topBadcasesV2": top_badcases(benchmark, "with_skill_v2"),
        "caseMatrix": case_matrix(benchmark),
        "versions": versions["versions"],
        "reasonArchive": reason_archive["badcases"],
        "regressionSet": regression_set,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default=str(ROOT / "runs" / "iteration-001"))
    parser.add_argument("--output", default=str(ROOT / "dashboard" / "data.js"))
    args = parser.parse_args()

    payload = build_payload(Path(args.run_dir))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    js = "window.SKILL_DASHBOARD_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    output.write_text(js, encoding="utf-8")
    print(f"已生成 Dashboard 数据：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
