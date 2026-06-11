---
name: ai-video-creator-style
description: Use when turning an AI product, brand campaign, model release, developer tool, cloud service, hardware device, or creator brief into short-form video title candidates, cover text, demo ideas, a three-part outline, or a 3:00-3:30 spoken script in the established AI product video style.
---

# AI Video Creator Style

This skill turns product briefs into short-form AI product video creative packages: high-hook titles, cover text, demo plan, outline, and a 3:00-3:30口播 script.

Core principle:

> Sell the visible result first. Use the product to explain why that result is now possible. End by showing how the workflow or creation style changes.

## Reference Loading

Load only the files needed for the requested artifact:

- Messy brief, client intake, or brief normalization: read `references/brief-input-template.md`.
- Titles only: read `references/title-formulas.md`.
- Cover text only: read `references/cover-style.md` and `references/title-formulas.md`.
- Outline only: read `references/outline-patterns.md` and `references/demo-design.md`.
- Script only: read `references/script-style.md`, `references/demo-design.md`, and `references/checklist.md`.
- Full creative package: read `references/brief-input-template.md` when the brief is messy, then read the six creative reference files.
- Final review or rewrite: read `references/checklist.md` plus the specific file for the artifact being reviewed.
- Style calibration, "像不像我" review, or high-confidence full-script finalization: also read `references/golden-sample-qclaw.md`.

Reference files:

- `references/brief-input-template.md`: client-facing brief template, normalized brief schema, extraction rules, and clarification rules.
- `references/title-formulas.md`: title formulas, Jack-Cui-inspired B站 hooks, title red flags, product-type title guidance.
- `references/cover-style.md`: cover text formulas, title-cover pairing rules, line-length guidance, and commercial safety replacements.
- `references/outline-patterns.md`: default three-part outline and structure variants.
- `references/script-style.md`:口播 rhythm, Jack-Cui-inspired spoken layer, sentence patterns, character count, duration rules.
- `references/demo-design.md`: opening hook, demo types, product-specific demo design.
- `references/checklist.md`: final title, outline, demo, script, language, and length checks.
- `references/golden-sample-qclaw.md`: standard script sample for judging whether a new script matches the preferred口播 rhythm and structure.

## Default Workflow

When the user provides a product brief and asks for creative output, follow this order.

### 1. Extract The Brief

If the brief is incomplete, scattered, or client-facing, use `references/brief-input-template.md` to normalize it first.

Identify:

- Product name and category.
- Target viewer.
- Main user pain.
- Most visible product result.
- 2-4 core capabilities.
- Required facts, numbers, offers, CTA, and restrictions.
- Available assets or demos.

If the brief lacks facts needed for a factual claim, do not invent them. Either ask briefly or label the line as an assumption/draft.

For a messy brief, produce or internally maintain a `Brief 归一化` block before generating creative output. Keep `待确认问题` limited to facts that affect accuracy, compliance, demo feasibility, CTA, or required brand exposure.

### 2. Classify Product Type

Choose the closest type:

- AI coding / agent / app builder.
- AI video / 3D / image / creative model.
- Cloud / compute / storage / training infrastructure.
- Voice AI / hardware / assistant device.
- Developer community / MCP / contest.

Use the product type to choose title formulas, outline variant, and demo style.

### 3. Design The Demo First

Before writing titles or script, design the demo hook internally or as a separate section when useful:

- Opening result.
- Viewer surprise.
- Product capability proven.
- On-screen steps.
- Optional second-round iteration.
- Old way vs new way.

If the demo is not visible, memorable, or one-sentence explainable, redesign it before writing the final script.

Do not put production labels such as "画面/demo" or "口播重点" inside the client-facing outline unless the user explicitly asks for a shooting plan.

### 4. Generate Titles

Generate 8-12 candidates:

- 3 B站 high-hook titles using the Jack-Cui-inspired hook layer.
- 3 professional but punchy titles.
- 3 scene-based titles.
- 1-3 emotional or CTA-adjacent titles.

At least 4 candidates should borrow from different high-click hook buckets: recognition gap, old-action interception, creator-tested proof, and result shock.

Mark the top 3 and briefly explain why they work.

By default, do not include the product name in titles. Titles should sell the viewer-facing result, pain, contrast, or scene. Only include the product name if the brief explicitly requires title-level brand exposure.

For brand or commercial briefs, run a safety pass after the high-hook pass: soften unsupported absolutes such as "最强", "唯一", "天花板", "全网首发", "吊打", "碾压", and "99%的人不知道". Preserve the excitement by replacing them with demo-backed phrasing like "我实测后有点意外", "很多人可能还没注意", or a specific proven comparison.

### 5. Generate Cover Text

When the user asks for a complete creative package, thumbnails, or封面文案, generate 6-10 cover text candidates using `references/cover-style.md`.

Cover text should:

- Be shorter and harder than the title.
- Sell the first-glance visible result, not the product name.
- Include both 2-line and 3-line options when ideating.
- For 2-line options, each line should be 7-10 Chinese characters, with fuller title-like phrasing.
- For 3-line options, each line should stay 5-7 Chinese characters, with tighter rhythm.
- Vary line lengths within each candidate when possible, such as 7/9 for two lines or 5/6/7 for three lines.
- First borrow a Jack-Cui-inspired title hook, then compress it into cover text.
- Prefer high-tension hooks such as old-action interception, plug-in metaphor, result shock, "this finally works" feeling, or role reversal.
- Pair with the recommended title without pasting the full title onto the cover.
- Avoid unsupported extreme claims in commercial briefs.

If the brief requires brand exposure, keep the product name as a secondary visual element unless title-level or cover-level main text exposure is explicitly required.

### 6. Build The Outline

Use the three-part structure by default:

1. 第一部分｜产品引出
2. 第二部分｜亮点 + 实测展示
3. 第三部分｜价值总结 + 行动号召

The first section should usually end with a brief product intro: product name, one-sentence positioning, and the specific capability used in this video. Do not start with brand background unless the brief requires it.

For each section, include:

- 内容要点 only.

The outline is for the client to understand the content direction. Keep it clean, readable, and free of internal execution labels. It should prove product value through tasks, not feature lists.

Do not put publishing hashtags, platform notes, or operational reminders inside the outline. Put them in a separate publishing notes section if needed.

The third section should include a value elevation line, usually a "一句升华", before CTA or action guidance.

### 7. Write The Script

Write spoken script only unless the user asks for shot notes.

The script must be divided into the same three sections as the outline. Each script section should correspond to the content points in the matching outline section.

Default target:

- Final video length: 3:00-3:30.
- Effective spoken Chinese characters: 850-1050.
- Script document characters: 1000-1200.

Segment targets:

- 产品引出: 180-250 effective spoken characters.
- 亮点 + 实测展示: 550-700 effective spoken characters.
- 价值总结 + 行动号召: 150-220 effective spoken characters.

Style requirements:

- Short,口语化 sentences.
- Start directly from the demo/result whenever possible. Avoid explanatory prefaces before the opening result.
- When a visible result is on screen, prefer a viewer-facing opening such as "你现在看到的这份/这个..." to create a conversational feeling.
- Concrete result in the first 10 seconds.
- Product name appears naturally after the hook, usually as a short product intro at the end of the first section.
- Avoid revealing the product name twice in part 1. If using a reveal line like "这次我用的是 [产品]", keep earlier lines generic ("AI", "这个工具", "它").
- The first section's product intro should connect directly to the following test/demo, not list the whole feature set.
- If the video centers on creating a Skill, Agent, or workflow, transition into the middle section as a process walkthrough, for example: "接下来，我就带你跑一遍 Skill 制作流程。"
- In process walkthroughs, use clear step markers and inclusive action language, such as "首先", "最后再到", and "我们还可以...".
- Technical facts are translated into user-facing outcomes.
- Use old-way vs new-way contrast.
- Include at least one "不是 X，而是 Y" value judgment.
- CTA is natural and usually under 80 characters.
- If the user asks for stronger B站技术区口播感, use the high-density spoken layer in `references/script-style.md`: fast hook, quick test, viewer-guiding lines, old/new compression, and no copied personal sign-off.

### 8. Self-Check

Before final delivery, apply `references/checklist.md`.

When the output includes a full script, compare it against `references/golden-sample-qclaw.md` if style matching matters. Use the sample for rhythm, sequencing, transitions, and value elevation; do not copy QClaw-specific claims into unrelated briefs.

For a complete package, include:

- Title candidates and recommended title.
- Cover text candidates and recommended cover text.
- Demo plan only if useful for testing or production planning.
- Three-part outline.
- Final script divided into the same three parts as the outline.
- Character count and estimated duration.
- Brief self-check summary.

## Output Formats

### Brief Normalization Only

```markdown
## Brief 归一化

### 产品定位

### 内容目标

### 目标观众

### 核心场景

### Demo 方向

### 必露能力

### 口径与禁区

### 发布与转化

### 素材与权限

### 待确认问题

### 生成假设
```

### Full Creative Package

```markdown
## 产品类型判断

## Demo Plan（可选，内部测试或拍摄规划用）
- Opening result:
- Viewer surprise:
- Product capability proven:
- On-screen steps:
- Second-round iteration:
- Old way vs new way:

## 标题候选

## 推荐标题

## 封面文案
- 两行版:
- 三行版:
- 推荐:
- 与标题的配合:

## 三段式大纲
### 第一部分｜产品引出
- 内容要点:

### 第二部分｜亮点 + 实测展示
- 内容要点:

### 第三部分｜价值总结 + 行动号召
- 内容要点:
- 一句升华:

## 脚本
### 第一部分｜产品引出

### 第二部分｜亮点 + 实测展示

### 第三部分｜价值总结 + 行动号召

## 字数与时长
- 有效口播字数:
- 预计时长:

## 自检
```

### Script Only

```markdown
## 标题

## 脚本
### 第一部分｜产品引出

### 第二部分｜亮点 + 实测展示

### 第三部分｜价值总结 + 行动号召

## 字数与时长
- 有效口播字数:
- 预计时长:
```

## Guardrails

- Do not start with brand background unless the user explicitly asks.
- Do not write generic PR copy.
- Do not stack technical terms without translating them into outcomes.
- Do not make cover text a long duplicate of the title; keep it title-like but compressed.
- Do not exceed 1200 script-document characters unless the user asks for a longer video.
- Do not include creator IP names or personal brand identifiers unless the user explicitly requests them.
- Do not fabricate benchmarks, prices, launch dates, model rankings, or customer claims.
- Do not use unverifiable extreme claims such as "最强", "唯一", "全网首发", "吊打", or "碾压" unless the brief explicitly proves and permits them.
 