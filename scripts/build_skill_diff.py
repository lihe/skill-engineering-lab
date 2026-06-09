#!/usr/bin/env python3
"""Build static Skill version-diff data for the dashboard."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return {}

    meta: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def load_skill_md(skill: str, version: str) -> tuple[Path, str, dict[str, str]]:
    path = ROOT / "skills" / skill / version / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    return path, text, parse_frontmatter(text)


def diff_rows(old_text: str, new_text: str) -> list[dict[str, str]]:
    rows = []
    for line in difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile="v1/SKILL.md",
        tofile="v2/SKILL.md",
        lineterm="",
    ):
        if line.startswith("@@"):
            kind = "hunk"
        elif line.startswith("+") and not line.startswith("+++"):
            kind = "add"
        elif line.startswith("-") and not line.startswith("---"):
            kind = "remove"
        elif line.startswith(("---", "+++")):
            kind = "file"
        else:
            kind = "context"
        rows.append({"type": kind, "text": line})
    return rows


def build_payload(skill: str) -> dict[str, Any]:
    _, v1_text, v1_meta = load_skill_md(skill, "v1")
    _, v2_text, v2_meta = load_skill_md(skill, "v2")
    versions = load_json(ROOT / "governance" / "versions.json")["versions"]
    reason_archive = load_json(ROOT / "governance" / "reason_archive.json")["badcases"]
    regression_set = load_json(ROOT / "governance" / "regression_set.json")

    latest = versions[-1]
    previous = versions[-2] if len(versions) > 1 else versions[-1]
    pass_delta = latest["observed_metrics"]["pass_rate"] - previous["observed_metrics"]["pass_rate"]
    over_trigger_delta = latest["observed_metrics"]["over_trigger_rate"] - previous["observed_metrics"]["over_trigger_rate"]
    token_delta = latest["observed_metrics"]["avg_tokens"] - previous["observed_metrics"]["avg_tokens"]

    return {
        "skill": skill,
        "fromVersion": "v1",
        "toVersion": "v2",
        "description": {
            "from": v1_meta.get("description", ""),
            "to": v2_meta.get("description", ""),
            "impact": "v2 明确了正向触发词和负向边界，让路由从宽泛宣传任务收敛到视频创作任务。",
        },
        "metricDelta": {
            "passRate": round(pass_delta * 100, 1),
            "overTriggerRate": round(over_trigger_delta * 100, 1),
            "avgTokens": token_delta,
        },
        "changedParts": latest["changed_parts"],
        "hypothesis": latest["main_hypothesis"],
        "decision": latest["decision"],
        "knownRisks": latest["known_risks"],
        "badcaseFixMap": [
            {
                "caseId": item["case_id"],
                "failurePattern": item["failure_pattern"],
                "rootCause": item["root_cause"],
                "fix": item["suggested_action"],
                "shouldRegress": item["should_regress"],
            }
            for item in reason_archive
        ],
        "regressionSet": regression_set,
        "skillMdDiff": diff_rows(v1_text, v2_text),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", default="ai-video-creator-style")
    parser.add_argument("--output", default=str(ROOT / "dashboard" / "skill_diff.js"))
    args = parser.parse_args()

    payload = build_payload(args.skill)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "window.SKILL_DIFF_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"已生成 Skill Diff 数据：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
