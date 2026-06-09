const configs = [
  {
    id: "without_skill",
    label: "无 Skill",
    passRate: 16.7,
    triggerRecall: null,
    overTrigger: null,
    tokens: 720,
    duration: 480,
    note: "基线输出泛化严重，缺少完整视频创意包结构。",
  },
  {
    id: "with_skill_v1",
    label: "Skill v1",
    passRate: 75.0,
    triggerRecall: 80.0,
    overTrigger: 50.0,
    tokens: 1142,
    duration: 828,
    note: "质量明显提升，但触发边界过宽，负向样例误触发。",
  },
  {
    id: "with_skill_v2",
    label: "Skill v2",
    passRate: 100.0,
    triggerRecall: 100.0,
    overTrigger: 0.0,
    tokens: 935,
    duration: 625,
    note: "通过收紧 description、硬化契约和脚本校验，形成可发布版本。",
  },
];

const evidence = [
  {
    title: "Skill 由 description 触发",
    body: "Claude 文档强调 description 会帮助模型判断何时加载 Skill；这解释了为什么本项目优先修正 v1 的触发边界。",
    source: "Anthropic Claude Docs",
    href: "https://docs.claude.com/en/docs/claude-code/skills",
  },
  {
    title: "支持文件用于渐进披露",
    body: "Claude Code 文档建议把详细参考、示例和脚本拆到 Skill 目录中，避免 SKILL.md 膨胀成上下文税。",
    source: "Claude Code Docs",
    href: "https://code.claude.com/docs/en/skills",
  },
  {
    title: "Eval 需要数据源与评分器",
    body: "OpenAI Evals 将评测定义为测试条件、数据源和评分器的组合；本项目以 cases、grader 和 benchmark 对应这些概念。",
    source: "OpenAI API Reference",
    href: "https://platform.openai.com/docs/api-reference/evals",
  },
  {
    title: "评测是 LLM 应用验证过程",
    body: "OpenAI Cookbook 将 evaluation 视为验证和测试应用输出的过程；本项目进一步把 Agent Skill 的触发和治理纳入评测。",
    source: "OpenAI Cookbook",
    href: "https://cookbook.openai.com/examples/evaluation/getting_started_with_openai_evals",
  },
];

const cases = [
  ["core-skill-eval-lab", 50, 70, 100],
  ["core-agent-coding", 50, 70, 100],
  ["core-mcp-db", 50, 70, 100],
  ["core-ai-image", 50, 70, 100],
  ["core-cloud-inference", 50, 70, 100],
  ["core-meeting-agent", 50, 70, 100],
  ["boundary-sparse-brief", 25, 20, 100],
  ["boundary-complex-brief", 50, 70, 100],
  ["extension-title-pool", 25, 70, 100],
  ["extension-cover-only", 25, 20, 100],
  ["negative-press-release", 100, 50, 100],
  ["negative-project-plan", 100, 100, 100],
];

const formatPct = (value) => (value === null ? "不适用" : `${value.toFixed(1)}%`);

function renderTabs() {
  const tabRoot = document.getElementById("configTabs");
  tabRoot.innerHTML = configs
    .map((config, index) => `<button class="tab-button ${index === 2 ? "active" : ""}" data-config="${config.id}">${config.label}</button>`)
    .join("");
  tabRoot.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    document.querySelectorAll(".tab-button").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    renderMetrics(button.dataset.config);
  });
}

function renderMetrics(configId = "with_skill_v2") {
  const config = configs.find((item) => item.id === configId);
  const cards = [
    ["通过率", formatPct(config.passRate), "最终产物是否通过结构、风格与泛化检查。"],
    ["触发召回率", formatPct(config.triggerRecall), "正向任务是否能稳定进入目标 Skill。"],
    ["过度触发率", formatPct(config.overTrigger), "负向任务是否被错误路由到视频创作 Skill。"],
    ["平均 Token", String(config.tokens), config.note],
  ];
  document.getElementById("metricPanels").innerHTML = cards
    .map(([title, value, body]) => `<article class="metric-card"><span>${title}</span><strong>${value}</strong><p>${body}</p></article>`)
    .join("");
}

function renderEvidence() {
  document.getElementById("evidenceGrid").innerHTML = evidence
    .map(
      (item) => `<article class="evidence-card">
        <h3>${item.title}</h3>
        <p>${item.body}</p>
        <a href="${item.href}">${item.source}</a>
      </article>`,
    )
    .join("");
}

function renderCases() {
  document.getElementById("caseGrid").innerHTML = cases
    .map(
      ([id, base, v1, v2]) => `<article class="case-card">
        <h3>${id}</h3>
        ${caseRow("无", base)}
        ${caseRow("v1", v1)}
        ${caseRow("v2", v2)}
      </article>`,
    )
    .join("");
}

function caseRow(label, score) {
  const tone = score >= 90 ? "good" : score >= 60 ? "warn" : "";
  return `<div class="case-row"><span>${label}</span><span class="score-pill ${tone}">${score}%</span></div>`;
}

renderTabs();
renderMetrics();
renderEvidence();
renderCases();
