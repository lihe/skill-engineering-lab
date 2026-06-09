#!/usr/bin/env python3
"""Deterministic validator for AI video creative packages."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SECTION_PATTERNS = {
    "titles": r"##\s+Title Candidates|##\s+标题候选",
    "cover": r"##\s+Cover Text|##\s+封面文案",
    "demo": r"##\s+Demo Plan|##\s+Demo 方案",
    "outline": r"##\s+Outline|##\s+三段式大纲",
    "script": r"##\s+Script|##\s+口播稿",
    "self_check": r"##\s+Self Check|##\s+自检",
}


@dataclass
class ValidationResult:
    ok: bool
    title_count: int
    cover_count: int
    has_demo: bool
    has_outline: bool
    has_script: bool
    cover_line_length_ok: bool
    issues: list[str]


def count_numbered_items(section_text: str) -> int:
    return len(re.findall(r"^\s*\d+[\.)、]", section_text, flags=re.MULTILINE))


def extract_section(text: str, heading_regex: str) -> str:
    match = re.search(heading_regex, text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def cover_line_length_ok(cover_section: str) -> bool:
    candidates = re.findall(r"^\s*\d+[\.)、]\s*(.+)$", cover_section, flags=re.MULTILINE)
    if not candidates:
        return False
    ok_count = 0
    for candidate in candidates:
        lines = [line.strip() for line in candidate.split("/") if line.strip()]
        if len(lines) not in (2, 3):
            continue
        limits = (10, 10) if len(lines) == 2 else (7, 7, 7)
        if all(len(line) <= limit for line, limit in zip(lines, limits)):
            ok_count += 1
    return ok_count >= max(1, min(3, len(candidates)))


def validate(text: str) -> ValidationResult:
    issues: list[str] = []
    title_section = extract_section(text, SECTION_PATTERNS["titles"])
    cover_section = extract_section(text, SECTION_PATTERNS["cover"])

    title_count = count_numbered_items(title_section)
    cover_count = count_numbered_items(cover_section)
    has_demo = bool(re.search(SECTION_PATTERNS["demo"], text))
    has_outline = bool(re.search(SECTION_PATTERNS["outline"], text))
    has_script = bool(re.search(SECTION_PATTERNS["script"], text))
    line_ok = cover_line_length_ok(cover_section)

    if not 8 <= title_count <= 12:
        issues.append(f"title_count_out_of_range:{title_count}")
    if cover_count < 6:
        issues.append(f"cover_count_too_low:{cover_count}")
    if not has_demo:
        issues.append("missing_demo_plan")
    if not has_outline:
        issues.append("missing_outline")
    if not has_script:
        issues.append("missing_script")
    if cover_section and not line_ok:
        issues.append("cover_line_length_failed")

    return ValidationResult(
        ok=not issues,
        title_count=title_count,
        cover_count=cover_count,
        has_demo=has_demo,
        has_outline=has_outline,
        has_script=has_script,
        cover_line_length_ok=line_ok,
        issues=issues,
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_package.py <output.md>", file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    result = validate(text)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
