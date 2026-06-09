# Skill Engineering Lab

这个实验室用于展示一个 Skill 如何完成工程化闭环：

```text
without_skill -> with_skill_v1 -> with_skill_v2
```

示例主题是“AI 视频创作风格 Skill”：输入一个 AI 产品信息，生成适合 B 站的标题、封面文案、Demo 方案、大纲和口播稿。

这个实验室采用确定性模拟，不直接调用大模型接口。它会模拟三种 Agent 状态，并用规则评分器生成稳定、可复现的评测结果，方便汇报分享。

## 运行

```bash
python3 scripts/run_eval.py --skill ai-video-creator-style --cases evals/cases.json
python3 scripts/summarize_report.py runs/iteration-001
```

报告会写入：

```text
runs/iteration-001/report.md
report.md
```

## 展示内容

- Skill 是否在该触发时触发、在不该触发时保持沉默。
- 引入 Skill 后，输出质量是否提升。
- Token 和耗时成本是否发生变化。
- 失败样例如何反推 `description`、`SKILL.md`、参考资料或脚本的迭代。
- 一个 Skill 如何沉淀为带有样例、轨迹、评分和报告的团队资产。

## 目录结构

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
