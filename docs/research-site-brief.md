# Skill Engineering Lab 研究站点 Brief

## 核心命题

AI Agent Skill 不应被当成长 Prompt，而应被建设成可触发、可评测、可回归、可治理的工程资产。

## 目标受众

- AI Agent 工程师
- Agent 产品经理
- 正在搭建内部自动化能力库的团队
- 需要在简历或作品集中展示 Agent 工程化能力的个人开发者

## 站点要让读者理解什么

1. Skill 的价值不在“写得多”，而在稳定触发和稳定净增益。
2. Skill 评测要用对照实验，而不是只展示单次输出。
3. 失败样例必须进入治理资产，否则 Skill 会变成上下文税。
4. 本项目已经用一个可复现实验演示了完整闭环。

## 叙事结构

1. Hero：提出命题和项目结果。
2. Evidence：引用官方文档和 eval 体系，说明为什么 `description`、渐进披露、评测资产重要。
3. System：展示本项目的运行链路。
4. Benchmark：展示 without_skill / v1 / v2 的量化结果。
5. Governance：展示版本记录、失败归因和回归集。
6. Handoff：引导读者打开 Dashboard、方法论文章和 GitHub 项目。

## 视觉资产

- 生命周期 SVG：Skill 从编写、评测、归因到治理。
- 三态对照图：without_skill / v1 / v2。
- 失败模式条形图：展示 v2 如何收敛失败。
- 证据卡片：官方 Skill 文档、OpenAI Evals、项目评测结果。

## 交互设计

- 点击切换三种配置，查看通过率、触发召回、过度触发和 Token。
- 展开证据卡，查看对应来源和对项目的启发。
- 样例矩阵展示每个 case 在三种配置下的结果。

## 引用来源

- Anthropic Claude Docs：Agent Skills
- Claude Code Docs：Extend Claude with skills
- OpenAI API Reference：Evals
- OpenAI Cookbook：Getting Started with OpenAI Evals
- 本项目：`runs/iteration-001/benchmark.json`
