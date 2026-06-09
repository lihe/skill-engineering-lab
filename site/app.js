const configs = [
  {
    id: "without_skill",
    label: "无 Skill",
    passRate: 16.7,
    triggerRecall: null,
    overTrigger: null,
    tokens: 720,
    duration: 480,
    note: "没有路由、契约和参考资产，输出容易退化成通用内容建议。",
  },
  {
    id: "with_skill_v1",
    label: "Skill v1",
    passRate: 75.0,
    triggerRecall: 80.0,
    overTrigger: 50.0,
    tokens: 1142,
    duration: 828,
    note: "质量明显提升，但 description 边界过宽，负向样例出现误触发。",
  },
  {
    id: "with_skill_v2",
    label: "Skill v2",
    passRate: 100.0,
    triggerRecall: 100.0,
    overTrigger: 0.0,
    tokens: 935,
    duration: 625,
    note: "收紧触发边界、硬化输出契约，并加入确定性脚本校验。",
  },
];

const lifecycle = [
  ["01", "Write", "把用户意图拆成路由入口、任务契约、参考资料和脚本。", "SKILL.md"],
  ["02", "Run", "同一批样例分别跑无 Skill、v1、v2，保留输出与轨迹。", "run_eval.py"],
  ["03", "Grade", "用触发、产出、风格、效率和泛化拆解质量，而不是只看观感。", "grade_output.py"],
  ["04", "Govern", "把 badcase 归因成下一轮动作，并固化为回归集。", "governance/"],
];

const evidence = [
  {
    title: "description 决定触发",
    body: "Claude 文档强调 description 会帮助模型判断何时加载 Skill；本项目把 v1 的漏触发和误触发都回收到 description 边界。",
    source: "Anthropic Claude Docs",
    href: "https://docs.claude.com/en/docs/claude-code/skills",
  },
  {
    title: "参考资料渐进加载",
    body: "Claude Code 文档建议把详细参考、示例和脚本拆到 Skill 目录，避免 SKILL.md 变成上下文税。",
    source: "Claude Code Docs",
    href: "https://code.claude.com/docs/en/skills",
  },
  {
    title: "Eval = 数据源 + 评分器",
    body: "OpenAI Evals 将评测组织为数据源、测试条件和评分器；本项目以 cases、configs、grader 对应这三个部件。",
    source: "OpenAI API Reference",
    href: "https://platform.openai.com/docs/api-reference/evals",
  },
  {
    title: "验证应用输出",
    body: "OpenAI Cookbook 把 evaluation 视为验证 LLM 应用输出的过程；本项目进一步把 Skill 触发治理纳入验证。",
    source: "OpenAI Cookbook",
    href: "https://cookbook.openai.com/examples/evaluation/getting_started_with_openai_evals",
  },
];

const badcases = [
  {
    tag: "漏触发",
    title: "稀疏 brief 没进入 Skill",
    body: "v1 依赖显式的视频/产品措辞。v2 扩展 description，覆盖创作者风格、B 站标题、封面、Demo、大纲、口播等表达。",
  },
  {
    tag: "漏触发",
    title: "只要封面文案时被忽略",
    body: "v1 把完整创意包当成唯一入口。v2 将封面文案、缩略图文案、标题封面搭配列为直接触发条件。",
  },
  {
    tag: "过度触发",
    title: "新闻稿写作误触发",
    body: "v1 把 AI 产品宣传内容写得过宽。v2 增加新闻稿、官方文章、项目计划、非视频内容的负向边界。",
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
    .map(
      (config, index) =>
        `<button class="tab-button ${index === 2 ? "active" : ""}" role="tab" aria-selected="${index === 2}" data-config="${config.id}">${config.label}</button>`,
    )
    .join("");
  tabRoot.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    document.querySelectorAll(".tab-button").forEach((item) => {
      item.classList.remove("active");
      item.setAttribute("aria-selected", "false");
    });
    button.classList.add("active");
    button.setAttribute("aria-selected", "true");
    renderMetrics(button.dataset.config);
  });
}

function renderMetrics(configId = "with_skill_v2") {
  const config = configs.find((item) => item.id === configId);
  const cards = [
    ["通过率", formatPct(config.passRate), "最终产物是否通过结构、风格与泛化检查。"],
    ["触发召回", formatPct(config.triggerRecall), "正向任务是否能稳定进入目标 Skill。"],
    ["过度触发", formatPct(config.overTrigger), "负向任务是否被错误路由到视频创作 Skill。"],
    ["平均 Token", String(config.tokens), config.note],
  ];
  document.getElementById("metricPanels").innerHTML = cards
    .map(([title, value, body]) => `<article class="metric-card"><span>${title}</span><strong>${value}</strong><p>${body}</p></article>`)
    .join("");
}

function renderDeltaChart() {
  document.getElementById("deltaChart").innerHTML = configs
    .map(
      (config) => `<div class="delta-bar ${config.id === "with_skill_v2" ? "best" : ""}">
        <span>${config.label}</span>
        <div class="delta-track"><div class="delta-fill" style="--value: ${config.passRate}%"></div></div>
        <b>${config.passRate.toFixed(1)}%</b>
      </div>`,
    )
    .join("");
}

function renderLifecycle() {
  document.getElementById("lifecycle").innerHTML = lifecycle
    .map(
      ([index, title, body, artifact]) => `<article class="lifecycle-step">
        <span class="step-index">${index}</span>
        <h3>${title}</h3>
        <p>${body}</p>
        <code>${artifact}</code>
      </article>`,
    )
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

function renderBadcases() {
  document.getElementById("badcaseList").innerHTML = badcases
    .map(
      (item) => `<article class="badcase-card">
        <span class="badcase-tag">${item.tag}</span>
        <h3>${item.title}</h3>
        <p>${item.body}</p>
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
renderDeltaChart();
renderLifecycle();
renderEvidence();
renderBadcases();
renderCases();
