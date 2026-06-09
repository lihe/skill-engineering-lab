---
name: ai-video-creator-style
description: Use when turning an AI product, developer tool, model release, cloud service, or creator brief into Bilibili-style video title candidates, cover text, demo ideas, a three-part outline, or a spoken script. Do not use for press releases, generic articles, project plans, issue triage, or non-video content strategy.
version: v2
---

# AI Video Creator Style v2

Turn AI product briefs into a complete Bilibili-style creative package: titles, cover text, demo plan, outline, and spoken script.

## Core Contract

For positive video-creative requests, produce:

1. 8-12 title candidates.
2. 6-10 cover text candidates.
3. A visible demo plan.
4. A three-part outline.
5. A spoken script split into the same three parts.
6. A short self-check summary.

## Trigger Boundaries

Use this Skill for:

- AI product video planning.
- Bilibili titles, cover text, demo ideas, outlines, and spoken scripts.
- Creator-facing launch videos for AI tools, models, cloud services, hardware, or agent workflows.

Do not use this Skill for:

- Press releases or official blog posts.
- Generic marketing strategy.
- Project management plans.
- Issue triage or implementation planning.
- Non-video writing tasks.

## Reference Loading

- Titles: read `references/title-formulas.md`.
- Cover text: read `references/cover-style.md`.
- Outline and demo: read `references/outline-patterns.md` and `references/demo-design.md`.
- Script: read `references/script-style.md` and `references/checklist.md`.
- Final review: run `scripts/validate_package.py` when available.

## Required Checks

- Title count is 8-12.
- At least four titles use different high-hook buckets.
- Cover text uses 2-3 lines with readable line length.
- The first 10 seconds sell a visible result.
- The script includes old-way vs new-way contrast.
- Unsupported extreme claims are softened.
- Product name is not the only hook.
