window.SKILL_DIFF_DATA = {
  "skill": "ai-video-creator-style",
  "fromVersion": "v1",
  "toVersion": "v2",
  "description": {
    "from": "Use when creating AI product videos, Bilibili titles, creative outlines, scripts, demos, or promotional content for AI products.",
    "to": "Use when turning an AI product, developer tool, model release, cloud service, or creator brief into Bilibili-style video title candidates, cover text, demo ideas, a three-part outline, or a spoken script. Do not use for press releases, generic articles, project plans, issue triage, or non-video content strategy.",
    "impact": "v2 明确了正向触发词和负向边界，让路由从宽泛宣传任务收敛到视频创作任务。"
  },
  "metricDelta": {
    "passRate": 25.0,
    "overTriggerRate": -50.0,
    "avgTokens": -207
  },
  "changedParts": [
    "description",
    "SKILL.md 检查清单",
    "scripts/validate_package.py"
  ],
  "hypothesis": "增加触发边界、显式产出契约和确定性检查，可以在提升质量的同时减少无效上下文消耗。",
  "decision": "发布 MVP",
  "knownRisks": [
    "真实 provider adapter 已接入，仍需建立稳定 API 回归环境和密钥管理策略",
    "样例集还需要补充更多历史真实产品信息"
  ],
  "badcaseFixMap": [
    {
      "caseId": "boundary-sparse-brief",
      "failurePattern": "触发不匹配",
      "rootCause": "description 依赖显式的视频或产品措辞，没有覆盖稀疏的创作者风格请求。",
      "fix": "扩展 description，覆盖创作者产品信息、B 站视频标题、封面、Demo、大纲或口播稿请求。",
      "shouldRegress": true
    },
    {
      "caseId": "extension-cover-only",
      "failurePattern": "触发不匹配",
      "rootCause": "description 没有把封面文案明确列为直接触发条件。",
      "fix": "把封面文案、缩略图文案、标题封面搭配加入触发条件。",
      "shouldRegress": true
    },
    {
      "caseId": "negative-press-release",
      "failurePattern": "过度触发",
      "rootCause": "description 缺少新闻稿和通用非视频营销文案的负向边界。",
      "fix": "为新闻稿、官方文章、项目计划和非视频内容增加明确的禁用边界。",
      "shouldRegress": true
    }
  ],
  "regressionSet": {
    "skill": "ai-video-creator-style",
    "iteration": "iteration-001",
    "must_keep_cases": [
      "boundary-sparse-brief",
      "extension-cover-only",
      "negative-press-release",
      "negative-project-plan"
    ],
    "reason": "这些样例用于保护触发召回、只要封面文案的扩展能力，以及防止过度触发。"
  },
  "skillMdDiff": [
    {
      "type": "file",
      "text": "--- v1/SKILL.md"
    },
    {
      "type": "file",
      "text": "+++ v2/SKILL.md"
    },
    {
      "type": "hunk",
      "text": "@@ -1,30 +1,54 @@"
    },
    {
      "type": "context",
      "text": " ---"
    },
    {
      "type": "context",
      "text": " name: ai-video-creator-style"
    },
    {
      "type": "remove",
      "text": "-description: Use when creating AI product videos, Bilibili titles, creative outlines, scripts, demos, or promotional content for AI products."
    },
    {
      "type": "remove",
      "text": "-version: v1"
    },
    {
      "type": "add",
      "text": "+description: Use when turning an AI product, developer tool, model release, cloud service, or creator brief into Bilibili-style video title candidates, cover text, demo ideas, a three-part outline, or a spoken script. Do not use for press releases, generic articles, project plans, issue triage, or non-video content strategy."
    },
    {
      "type": "add",
      "text": "+version: v2"
    },
    {
      "type": "context",
      "text": " ---"
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-# AI Video Creator Style v1"
    },
    {
      "type": "add",
      "text": "+# AI Video Creator Style v2"
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-Turn AI product briefs into video creative ideas."
    },
    {
      "type": "add",
      "text": "+Turn AI product briefs into a complete Bilibili-style creative package: titles, cover text, demo plan, outline, and spoken script."
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-## Workflow"
    },
    {
      "type": "add",
      "text": "+## Core Contract"
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-1. Read the product brief."
    },
    {
      "type": "remove",
      "text": "-2. Generate title candidates."
    },
    {
      "type": "remove",
      "text": "-3. Create cover text."
    },
    {
      "type": "remove",
      "text": "-4. Create a three-part outline."
    },
    {
      "type": "remove",
      "text": "-5. Write a short spoken script."
    },
    {
      "type": "add",
      "text": "+For positive video-creative requests, produce:"
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-## Style"
    },
    {
      "type": "add",
      "text": "+1. 8-12 title candidates."
    },
    {
      "type": "add",
      "text": "+2. 6-10 cover text candidates."
    },
    {
      "type": "add",
      "text": "+3. A visible demo plan."
    },
    {
      "type": "add",
      "text": "+4. A three-part outline."
    },
    {
      "type": "add",
      "text": "+5. A spoken script split into the same three parts."
    },
    {
      "type": "add",
      "text": "+6. A short self-check summary."
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-- Make it catchy and Bilibili-friendly."
    },
    {
      "type": "remove",
      "text": "-- Mention product value clearly."
    },
    {
      "type": "remove",
      "text": "-- Use a demo when possible."
    },
    {
      "type": "add",
      "text": "+## Trigger Boundaries"
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-## Known Weaknesses"
    },
    {
      "type": "add",
      "text": "+Use this Skill for:"
    },
    {
      "type": "context",
      "text": " "
    },
    {
      "type": "remove",
      "text": "-- The description is too broad and may trigger on adjacent promotional writing tasks."
    },
    {
      "type": "remove",
      "text": "-- It does not clearly say when not to use this Skill."
    },
    {
      "type": "remove",
      "text": "-- It asks for Bilibili style but does not harden title count, cover line length, or demo-first rules."
    },
    {
      "type": "remove",
      "text": "-- It has no deterministic verifier script."
    },
    {
      "type": "add",
      "text": "+- AI product video planning."
    },
    {
      "type": "add",
      "text": "+- Bilibili titles, cover text, demo ideas, outlines, and spoken scripts."
    },
    {
      "type": "add",
      "text": "+- Creator-facing launch videos for AI tools, models, cloud services, hardware, or agent workflows."
    },
    {
      "type": "add",
      "text": "+"
    },
    {
      "type": "add",
      "text": "+Do not use this Skill for:"
    },
    {
      "type": "add",
      "text": "+"
    },
    {
      "type": "add",
      "text": "+- Press releases or official blog posts."
    },
    {
      "type": "add",
      "text": "+- Generic marketing strategy."
    },
    {
      "type": "add",
      "text": "+- Project management plans."
    },
    {
      "type": "add",
      "text": "+- Issue triage or implementation planning."
    },
    {
      "type": "add",
      "text": "+- Non-video writing tasks."
    },
    {
      "type": "add",
      "text": "+"
    },
    {
      "type": "add",
      "text": "+## Reference Loading"
    },
    {
      "type": "add",
      "text": "+"
    },
    {
      "type": "add",
      "text": "+- Titles: read `references/title-formulas.md`."
    },
    {
      "type": "add",
      "text": "+- Cover text: read `references/cover-style.md`."
    },
    {
      "type": "add",
      "text": "+- Outline and demo: read `references/outline-patterns.md` and `references/demo-design.md`."
    },
    {
      "type": "add",
      "text": "+- Script: read `references/script-style.md` and `references/checklist.md`."
    },
    {
      "type": "add",
      "text": "+- Final review: run `scripts/validate_package.py` when available."
    },
    {
      "type": "add",
      "text": "+"
    },
    {
      "type": "add",
      "text": "+## Required Checks"
    },
    {
      "type": "add",
      "text": "+"
    },
    {
      "type": "add",
      "text": "+- Title count is 8-12."
    },
    {
      "type": "add",
      "text": "+- At least four titles use different high-hook buckets."
    },
    {
      "type": "add",
      "text": "+- Cover text uses 2-3 lines with readable line length."
    },
    {
      "type": "add",
      "text": "+- The first 10 seconds sell a visible result."
    },
    {
      "type": "add",
      "text": "+- The script includes old-way vs new-way contrast."
    },
    {
      "type": "add",
      "text": "+- Unsupported extreme claims are softened."
    },
    {
      "type": "add",
      "text": "+- Product name is not the only hook."
    }
  ]
};
