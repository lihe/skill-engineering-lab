# Skill Engineering Lab

This lab shows how a Skill moves through the engineering loop:

```text
without_skill -> with_skill_v1 -> with_skill_v2
```

The theme is an AI video creative Skill: given an AI product brief, produce a Bilibili-style creative package with titles, cover text, demo plan, outline, and spoken script.

The lab is deterministic. It does not call an LLM API. Instead, it simulates three agent states and runs rule-based grading so the lab is stable for sharing.

## Run

```bash
python3 scripts/run_eval.py --skill ai-video-creator-style --cases evals/cases.json
python3 scripts/summarize_report.py runs/iteration-001
```

The report is written to:

```text
runs/iteration-001/report.md
report.md
```

## What It Demonstrates

- Whether the Skill triggers correctly.
- Whether output quality improves.
- Whether token/time costs change.
- How badcases point to `description`, `SKILL.md`, references, or scripts.
- How a Skill becomes a governed asset with cases, traces, grading, and reports.

## Structure

```text
skill-engineering-lab/
├── skills/
│   └── ai-video-creator-style/
│       ├── v1/
│       ├── v2/
│       └── references/
├── evals/
│   └── cases.json
├── runs/
├── scripts/
│   ├── grade_output.py
│   ├── run_eval.py
│   └── summarize_report.py
└── report.md
```
