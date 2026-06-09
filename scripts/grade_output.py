#!/usr/bin/env python3
"""Rule-based grader for the Skill Engineering Lab."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "skills" / "ai-video-creator-style" / "scripts" / "validate_package.py"


HOOK_TERMS = [
    "别再",
    "实测",
    "你现在看到",
    "不是",
    "而是",
    "外挂",
    "接管",
    "真能",
    "一键",
]


@dataclass
class Check:
    id: str
    score: int
    max_score: int
    evidence: str


def numbered_count(text: str, heading: str) -> int:
    section = extract_section(text, heading)
    return len(re.findall(r"^\s*\d+[\.)、]", section, flags=re.MULTILINE))


def extract_section(text: str, heading_regex: str) -> str:
    match = re.search(heading_regex, text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def has_section(text: str, heading_regex: str) -> bool:
    return bool(re.search(heading_regex, text))


def cover_line_length_pass(text: str) -> bool:
    cover = extract_section(text, r"##\s+Cover Text|##\s+封面文案")
    candidates = re.findall(r"^\s*\d+[\.)、]\s*(.+)$", cover, flags=re.MULTILINE)
    if not candidates:
        return False
    passing = 0
    for candidate in candidates:
        lines = [line.strip() for line in candidate.split("/") if line.strip()]
        if len(lines) == 2 and all(len(line) <= 10 for line in lines):
            passing += 1
        elif len(lines) == 3 and all(len(line) <= 7 for line in lines):
            passing += 1
    return passing >= 3


def style_score(text: str) -> Check:
    hits = [term for term in HOOK_TERMS if term in text]
    has_contrast = "不是" in text and "而是" in text
    has_opening = "你现在看到" in text or "别再" in text
    line_ok = cover_line_length_pass(text)
    score = 0
    if len(hits) >= 4:
        score += 1
    if has_contrast and has_opening and line_ok:
        score += 1
    evidence = f"hook_terms={hits}; contrast={has_contrast}; opening={has_opening}; cover_line_length={line_ok}"
    return Check("style_alignment", score, 2, evidence)


def outcome_score(text: str, should_trigger: bool) -> Check:
    if not should_trigger:
        video_sections = [
            has_section(text, r"##\s+Title Candidates|##\s+标题候选"),
            has_section(text, r"##\s+Cover Text|##\s+封面文案"),
            has_section(text, r"##\s+Script|##\s+口播稿"),
        ]
        score = 2 if not any(video_sections) else 0
        return Check("outcome", score, 2, f"negative_case_video_sections={video_sections}")

    title_count = numbered_count(text, r"##\s+Title Candidates|##\s+标题候选")
    cover_count = numbered_count(text, r"##\s+Cover Text|##\s+封面文案")
    has_demo = has_section(text, r"##\s+Demo Plan|##\s+Demo 方案")
    has_outline = has_section(text, r"##\s+Outline|##\s+三段式大纲")
    has_script = has_section(text, r"##\s+Script|##\s+口播稿")

    score = 0
    if 8 <= title_count <= 12 and cover_count >= 6:
        score += 1
    if has_demo and has_outline and has_script:
        score += 1
    evidence = (
        f"title_count={title_count}; cover_count={cover_count}; "
        f"has_demo={has_demo}; has_outline={has_outline}; has_script={has_script}"
    )
    return Check("outcome", score, 2, evidence)


def trigger_score(config: str, actual_triggered: bool, should_trigger: bool) -> Check:
    if config == "without_skill":
        return Check("trigger", 2, 2, "baseline has no skill routing; excluded from trigger metrics")
    score = 2 if actual_triggered == should_trigger else 0
    return Check("trigger", score, 2, f"expected={should_trigger}; actual={actual_triggered}")


def efficiency_score(token_estimate: int, baseline_tokens: int) -> Check:
    delta = (token_estimate - baseline_tokens) / max(1, baseline_tokens)
    if delta <= 0.20:
        score = 2
    elif delta <= 0.50:
        score = 1
    else:
        score = 0
    return Check("efficiency", score, 2, f"token_estimate={token_estimate}; baseline={baseline_tokens}; delta={delta:.2%}")


def generalization_score(case: dict[str, Any], checks: list[Check]) -> Check:
    risky = case.get("case_type") in {"boundary", "extension"} or "implicit_trigger" in case.get("risk_tag", [])
    if not risky:
        return Check("generalization", 2, 2, "not a generalization stress case")
    trigger = next(check for check in checks if check.id == "trigger")
    outcome = next(check for check in checks if check.id == "outcome")
    score = 2 if trigger.score == 2 and outcome.score >= 1 else 0
    return Check("generalization", score, 2, f"risk_tags={case.get('risk_tag', [])}; trigger={trigger.score}; outcome={outcome.score}")


def grade(
    *,
    case: dict[str, Any],
    config: str,
    output_text: str,
    actual_triggered: bool,
    token_estimate: int,
    baseline_tokens: int,
) -> dict[str, Any]:
    checks = [
        trigger_score(config, actual_triggered, case["should_trigger"]),
        outcome_score(output_text, case["should_trigger"]),
        style_score(output_text) if case["should_trigger"] else Check("style_alignment", 2, 2, "negative case; no video style expected"),
        efficiency_score(token_estimate, baseline_tokens),
    ]
    checks.append(generalization_score(case, checks))

    # Trigger is not counted in baseline overall quality because no skill routing exists there.
    counted = [check for check in checks if not (config == "without_skill" and check.id == "trigger")]
    score = sum(check.score for check in counted)
    max_score = sum(check.max_score for check in counted)
    pass_threshold = 0.70
    overall_pass = score / max_score >= pass_threshold

    failure_patterns = []
    if config != "without_skill" and checks[0].score == 0:
        failure_patterns.append("trigger_mismatch")
    if checks[1].score < 2:
        failure_patterns.append("outcome_incomplete")
    if checks[2].score < 2:
        failure_patterns.append("style_weak")
    if checks[3].score < 2:
        failure_patterns.append("efficiency_cost")
    if checks[4].score < 2:
        failure_patterns.append("generalization_risk")

    return {
        "case_id": case["id"],
        "case_type": case["case_type"],
        "config": config,
        "overall_pass": overall_pass,
        "score": score,
        "max_score": max_score,
        "score_ratio": round(score / max_score, 4),
        "actual_triggered": actual_triggered,
        "should_trigger": case["should_trigger"],
        "checks": [asdict(check) for check in checks],
        "failure_patterns": failure_patterns,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--triggered", action="store_true")
    parser.add_argument("--token-estimate", type=int, required=True)
    parser.add_argument("--baseline-tokens", type=int, default=900)
    args = parser.parse_args()

    case = json.loads(Path(args.case).read_text(encoding="utf-8"))
    output_text = Path(args.output).read_text(encoding="utf-8")
    result = grade(
        case=case,
        config=args.config,
        output_text=output_text,
        actual_triggered=args.triggered,
        token_estimate=args.token_estimate,
        baseline_tokens=args.baseline_tokens,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
