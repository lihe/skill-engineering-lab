const data = window.SKILL_DASHBOARD_DATA;
const skillDiff = window.SKILL_DIFF_DATA;

const typeLabels = {
  all: "全部",
  core: "核心",
  boundary: "边界",
  extension: "扩展",
  negative: "负向",
};

const configLabels = {
  without_skill: "无 Skill",
  with_skill_v1: "Skill v1",
  with_skill_v2: "Skill v2",
};

const state = {
  caseFilter: "all",
  selectedCaseId: data.caseMatrix[0]?.caseId,
};

const fmtPct = (value) => (value === null || value === undefined ? "不适用" : `${value.toFixed(1)}%`);
const fmtNum = (value) => Math.round(value).toLocaleString("zh-CN");
const clamp = (value, min = 0, max = 100) => Math.max(min, Math.min(max, value));

function el(tag, className, html) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
}

function renderRunMeta() {
  const container = document.getElementById("runMeta");
  const items = [
    data.skill,
    data.iteration,
    `${data.provider || "mock"} / ${data.model || "deterministic-v1"}`,
    `${data.cases} 条样例`,
    `生成于 ${new Date(data.generatedAt).toLocaleString("zh-CN", { hour12: false })}`,
  ];
  container.replaceChildren(...items.map((item) => el("span", "pill", item)));
}

function renderHeadlineMetrics() {
  const v2 = data.metrics.find((item) => item.config === "with_skill_v2");
  const metrics = [
    {
      title: "v2 相对基线质量提升",
      value: `+${data.headline.passLiftV2VsBase.toFixed(1)}%`,
      desc: "用对照实验衡量 Skill 是否真正带来净增益。",
    },
    {
      title: "v2 触发召回率",
      value: fmtPct(v2.triggerRecall),
      desc: "正向视频创作任务全部触发目标 Skill。",
    },
    {
      title: "过度触发下降",
      value: `-${data.headline.overTriggerDrop.toFixed(1)}%`,
      desc: "通过负向边界控制新闻稿、项目计划等相邻任务串扰。",
    },
    {
      title: "v2 相对 v1 Token 变化",
      value: `${data.headline.tokenDeltaV2VsV1.toFixed(1)}%`,
      desc: "在质量提升的同时，压缩无效上下文消耗。",
    },
  ];
  document.getElementById("headlineMetrics").replaceChildren(
    ...metrics.map((item) =>
      el(
        "article",
        "metric-card",
        `<h3>${item.title}</h3><strong>${item.value}</strong><p>${item.desc}</p>`,
      ),
    ),
  );
}

function renderMetricTable() {
  const rows = data.metrics
    .map((item) => {
      const badge =
        item.config === "with_skill_v2"
          ? '<span class="status-good">发布</span>'
          : item.config === "with_skill_v1"
            ? '<span class="status-warn">迭代</span>'
            : '<span class="status-muted">基线</span>';
      return `<tr>
        <td><b>${item.label}</b></td>
        <td>${fmtPct(item.passRate)}</td>
        <td>${fmtPct(item.triggerRecall)}</td>
        <td>${fmtPct(item.overTriggerRate)}</td>
        <td>${fmtNum(item.avgTokens)}</td>
        <td>${fmtNum(item.avgDurationMs)} ms</td>
        <td>${badge}</td>
      </tr>`;
    })
    .join("");
  document.getElementById("metricTable").innerHTML = `
    <thead>
      <tr>
        <th>配置</th>
        <th>通过率</th>
        <th>触发召回率</th>
        <th>过度触发率</th>
        <th>平均 Token</th>
        <th>平均耗时</th>
        <th>决策</th>
      </tr>
    </thead>
    <tbody>${rows}</tbody>
  `;
}

function renderLiftStack() {
  const v1 = data.metrics.find((item) => item.config === "with_skill_v1");
  const v2 = data.metrics.find((item) => item.config === "with_skill_v2");
  const rows = [
    { label: "v1 通过率", value: v1.passRate, color: "amber" },
    { label: "v2 通过率", value: v2.passRate, color: "green" },
    { label: "v1 过度触发", value: v1.overTriggerRate, color: "red" },
    { label: "v2 过度触发", value: v2.overTriggerRate, color: "green" },
  ];
  document.getElementById("liftStack").replaceChildren(
    ...rows.map((row) =>
      el(
        "div",
        "lift-item",
        `<b>${row.label}</b>
        <div class="bar-track"><div class="bar ${row.color}" style="width:${clamp(row.value)}%"></div></div>
        <div class="bar-caption"><span>当前值</span><span>${fmtPct(row.value)}</span></div>`,
      ),
    ),
  );
}

function renderPatternChart() {
  const max = Math.max(
    1,
    ...data.failurePatterns.flatMap((item) => [item.withoutSkill, item.skillV1, item.skillV2]),
  );
  document.getElementById("patternChart").replaceChildren(
    ...data.failurePatterns.map((item) =>
      el(
        "div",
        "pattern-row",
        `<div class="pattern-label">${item.pattern}</div>
        <div class="pattern-bars">
          ${miniBar("无 Skill", item.withoutSkill, max, "red")}
          ${miniBar("v1", item.skillV1, max, "amber")}
          ${miniBar("v2", item.skillV2, max, "green")}
        </div>`,
      ),
    ),
  );
}

function miniBar(label, value, max, color) {
  const width = (value / max) * 100;
  return `<div class="mini-bar">
    <span>${label}</span>
    <div class="bar-track"><div class="bar ${color}" style="width:${width}%"></div></div>
    <span>${value}</span>
  </div>`;
}

function renderCaseTypes() {
  document.getElementById("caseTypes").replaceChildren(
    ...data.caseTypes.map((item) =>
      el(
        "div",
        "case-type-item",
        `<div><strong>${item.label}场景</strong><span>${item.type}</span></div><b>${item.count}</b>`,
      ),
    ),
  );
}

function renderBadcases() {
  const list = skillDiff?.badcaseFixMap || data.reasonArchive.slice(0, 4);
  document.getElementById("badcaseList").replaceChildren(
    ...list.map((item) =>
      el(
        "div",
        "badcase-item",
        `<strong>${item.caseId || item.case_id}</strong>
        <p>${item.failurePattern || item.failure_pattern}：${item.rootCause || item.root_cause}</p>
        <p><b>修复动作</b>：${item.fix || item.suggested_action}</p>`,
      ),
    ),
  );
}

function renderGovernance() {
  const latest = data.versions[data.versions.length - 1];
  const items = [
    ["版本决策", `${latest.version}：${latest.decision}`],
    ["Provider", `${data.provider || "mock"} / ${data.model || "deterministic-v1"}`],
    ["回归样例", `${data.regressionSet.must_keep_cases.length} 条必须保留`],
    ["失败归因", `${data.reasonArchive.length} 条根因归档`],
    ["下一步风险", latest.known_risks.join("；")],
  ];
  document.getElementById("governanceList").replaceChildren(
    ...items.map(([title, body]) =>
      el("div", "governance-item", `<strong>${title}</strong><p>${body}</p>`),
    ),
  );
}

function renderCaseFilters() {
  const container = document.getElementById("caseFilters");
  if (!container) return;
  const filters = ["all", ...data.caseTypes.map((item) => item.type)];
  container.replaceChildren(
    ...filters.map((filter) => {
      const button = el("button", `filter-button ${state.caseFilter === filter ? "active" : ""}`, typeLabels[filter]);
      button.type = "button";
      button.addEventListener("click", () => {
        state.caseFilter = filter;
        const first = filteredCases()[0];
        state.selectedCaseId = first?.caseId;
        renderCaseFilters();
        renderCaseMatrix();
        renderCaseDetail();
      });
      return button;
    }),
  );
}

function filteredCases() {
  if (state.caseFilter === "all") return data.caseMatrix;
  return data.caseMatrix.filter((item) => item.caseType === state.caseFilter);
}

function renderCaseMatrix() {
  const labels = {
    without_skill: "无",
    with_skill_v1: "v1",
    with_skill_v2: "v2",
  };
  const cases = filteredCases();
  document.getElementById("caseMatrix").replaceChildren(
    ...cases.map((item) => {
      const configHtml = Object.entries(labels)
        .map(([config, label]) => {
          const result = item.configs[config];
          const status = result.pass ? "status-good" : "status-warn";
          return `<div class="case-result">
            <b>${label}</b>
            <span class="${status}">${fmtPct(result.score)}</span>
          </div>`;
        })
        .join("");
      const card = el(
        "button",
        `case-card ${item.caseId === state.selectedCaseId ? "active" : ""}`,
        `<div class="case-card-header">
          <h3>${item.caseId}</h3>
          <span class="pill">${typeLabels[item.caseType] || item.caseType}</span>
        </div>
        <div class="case-results">${configHtml}</div>`,
      );
      card.type = "button";
      card.addEventListener("click", () => {
        state.selectedCaseId = item.caseId;
        renderCaseMatrix();
        renderCaseDetail();
      });
      return card;
    }),
  );
}

function renderCaseDetail() {
  const container = document.getElementById("caseDetail");
  if (!container) return;
  const selected = data.caseMatrix.find((item) => item.caseId === state.selectedCaseId) || filteredCases()[0];
  if (!selected) {
    container.innerHTML = "<p>当前筛选下没有样例。</p>";
    return;
  }

  const rows = Object.entries(configLabels)
    .map(([config, label]) => {
      const result = selected.configs[config];
      const status = result.pass ? "通过" : "待修复";
      const patterns = result.failurePatterns.length ? result.failurePatterns.join("、") : "无";
      return `<div class="detail-row">
        <b>${label}</b>
        <span>${status} · ${fmtPct(result.score)} · ${fmtNum(result.tokens)} token</span>
        <p>${patterns}</p>
      </div>`;
    })
    .join("");

  container.innerHTML = `
    <p class="eyebrow">Selected Case</p>
    <h3>${selected.caseId}</h3>
    <div class="detail-meta">
      <span>${typeLabels[selected.caseType] || selected.caseType}</span>
      <span>${selected.shouldTrigger ? "应触发" : "不应触发"}</span>
    </div>
    ${rows}
  `;
}

function renderSkillDiff() {
  if (!skillDiff) return;

  const summary = document.getElementById("skillDiffSummary");
  const diffBlock = document.getElementById("skillDiffBlock");
  summary.replaceChildren(
    el(
      "div",
      "diff-card",
      `<strong>Description 收紧</strong>
      <p>${skillDiff.description.impact}</p>
      <small>v1：${skillDiff.description.from}</small>
      <small>v2：${skillDiff.description.to}</small>`,
    ),
    el(
      "div",
      "diff-card",
      `<strong>指标变化</strong>
      <p>通过率 +${skillDiff.metricDelta.passRate.toFixed(1)}%，过度触发 ${skillDiff.metricDelta.overTriggerRate.toFixed(1)}%，平均 Token ${skillDiff.metricDelta.avgTokens}。</p>`,
    ),
    el(
      "div",
      "diff-card",
      `<strong>改动面</strong>
      <p>${skillDiff.changedParts.join("、")}</p>
      <small>${skillDiff.hypothesis}</small>`,
    ),
  );

  diffBlock.innerHTML = skillDiff.skillMdDiff
    .map((line) => `<span class="diff-line ${line.type}">${escapeHtml(line.text)}</span>`)
    .join("");
}

function renderRegressionList() {
  const container = document.getElementById("regressionList");
  if (!container) return;
  const regression = skillDiff?.regressionSet || data.regressionSet;
  const reason = regression.reason;
  container.replaceChildren(
    el("div", "governance-item", `<strong>保护原因</strong><p>${reason}</p>`),
    ...regression.must_keep_cases.map((caseId) =>
      el("div", "governance-item compact", `<strong>${caseId}</strong><p>必须保留在每轮回归测试中。</p>`),
    ),
  );
}

function setupTabs() {
  const buttons = [...document.querySelectorAll(".tab-button")];
  const panels = [...document.querySelectorAll(".view-panel")];
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.viewTarget;
      buttons.forEach((item) => item.classList.toggle("active", item === button));
      panels.forEach((panel) => panel.classList.toggle("active", panel.id === target));
    });
  });
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function render() {
  setupTabs();
  renderRunMeta();
  renderHeadlineMetrics();
  renderMetricTable();
  renderLiftStack();
  renderPatternChart();
  renderCaseTypes();
  renderCaseFilters();
  renderBadcases();
  renderGovernance();
  renderCaseMatrix();
  renderCaseDetail();
  renderSkillDiff();
  renderRegressionList();
}

render();
