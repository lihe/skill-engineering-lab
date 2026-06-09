#!/usr/bin/env python3
"""把 Skill Engineering Lab 的评测结果汇总成 Markdown 报告。"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


CONFIG_LABELS = {
    "without_skill": "无 Skill",
    "with_skill_v1": "使用 Skill v1",
    "with_skill_v2": "使用 Skill v2",
}


def load_benchmark(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "benchmark.json").read_text(encoding="utf-8"))


def config_results(benchmark: dict[str, Any], config: str) -> list[dict[str, Any]]:
    return [result for result in benchmark["results"] if result["config"] == config]


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def pass_rate(results: list[dict[str, Any]]) -> float:
    if not results:
        return 0.0
    return sum(1 for result in results if result["overall_pass"]) / len(results)


def trigger_recall(results: list[dict[str, Any]]) -> float:
    positives = [result for result in results if result["should_trigger"]]
    if not positives:
        return 0.0
    return sum(1 for result in positives if result["actual_triggered"]) / len(positives)


def over_trigger_rate(results: list[dict[str, Any]]) -> float:
    negatives = [result for result in results if not result["should_trigger"]]
    if not negatives:
        return 0.0
    return sum(1 for result in negatives if result["actual_triggered"]) / len(negatives)


def avg_token(results: list[dict[str, Any]]) -> float:
    return mean(result["token_estimate"] for result in results) if results else 0.0


def avg_duration(results: list[dict[str, Any]]) -> float:
    return mean(result["duration_ms"] for result in results) if results else 0.0


def failure_summary(results: list[dict[str, Any]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for result in results:
        counter.update(result["failure_patterns"])
    return counter


def top_badcases(benchmark: dict[str, Any], config: str, limit: int = 5) -> list[dict[str, Any]]:
    results = [result for result in config_results(benchmark, config) if not result["overall_pass"]]
    return sorted(results, key=lambda result: (result["score_ratio"], result["case_id"]))[:limit]


def decision(v2_results: list[dict[str, Any]], v1_results: list[dict[str, Any]]) -> str:
    v2_pass = pass_rate(v2_results)
    v1_pass = pass_rate(v1_results)
    v2_over = over_trigger_rate(v2_results)
    if v2_pass >= 0.85 and v2_over == 0:
        return "发布"
    if v2_pass > v1_pass:
        return "继续迭代"
    return "拆分或重写"


def metric_table(benchmark: dict[str, Any]) -> str:
    lines = [
        "| 配置 | 通过率 | 触发召回率 | 过度触发率 | 平均 Token | 平均耗时 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for config in benchmark["configs"]:
        results = config_results(benchmark, config)
        lines.append(
            "| {label} | {pass_rate} | {trigger} | {over} | {tokens:.0f} | {time:.0f} ms |".format(
                label=CONFIG_LABELS[config],
                pass_rate=pct(pass_rate(results)),
                trigger="不适用" if config == "without_skill" else pct(trigger_recall(results)),
                over="不适用" if config == "without_skill" else pct(over_trigger_rate(results)),
                tokens=avg_token(results),
                time=avg_duration(results),
            )
        )
    return "\n".join(lines)


def lift_table(benchmark: dict[str, Any]) -> str:
    base = config_results(benchmark, "without_skill")
    v1 = config_results(benchmark, "with_skill_v1")
    v2 = config_results(benchmark, "with_skill_v2")
    base_pass = pass_rate(base)
    v1_pass = pass_rate(v1)
    v2_pass = pass_rate(v2)
    base_tokens = avg_token(base)
    v1_tokens = avg_token(v1)
    v2_tokens = avg_token(v2)
    return "\n".join(
        [
            "| 对比 | 质量提升 | Token 变化 |",
            "| --- | ---: | ---: |",
            f"| v1 相对基线 | {pct(v1_pass - base_pass)} | {pct((v1_tokens - base_tokens) / base_tokens)} |",
            f"| v2 相对基线 | {pct(v2_pass - base_pass)} | {pct((v2_tokens - base_tokens) / base_tokens)} |",
            f"| v2 相对 v1 | {pct(v2_pass - v1_pass)} | {pct((v2_tokens - v1_tokens) / v1_tokens)} |",
        ]
    )


def badcase_table(benchmark: dict[str, Any], config: str) -> str:
    badcases = top_badcases(benchmark, config)
    if not badcases:
        return "没有失败样例。"
    lines = [
        "| 样例 | 类型 | 得分 | 失败模式 |",
        "| --- | --- | ---: | --- |",
    ]
    type_labels = {
        "core": "核心",
        "boundary": "边界",
        "extension": "扩展",
        "negative": "负向",
    }
    for result in badcases:
        lines.append(
            f"| `{result['case_id']}` | {type_labels.get(result['case_type'], result['case_type'])} | {pct(result['score_ratio'])} | {'、'.join(result['failure_patterns']) or '无'} |"
        )
    return "\n".join(lines)


def failure_pattern_table(benchmark: dict[str, Any]) -> str:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for config in benchmark["configs"]:
        grouped[config] = failure_summary(config_results(benchmark, config))
    all_patterns = sorted({pattern for counter in grouped.values() for pattern in counter})
    if not all_patterns:
        return "没有记录到失败模式。"
    lines = [
        "| 失败模式 | 无 Skill | v1 | v2 | 建议动作 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    actions = {
        "触发不匹配": "收紧或扩展 `description` 的触发边界。",
        "产出不完整": "硬化必选产出检查清单。",
        "风格较弱": "补强参考资料和示例。",
        "效率成本偏高": "把确定性检查下沉到脚本，并裁剪参考资料。",
        "泛化风险": "把改写和边界样例加入回归集。",
    }
    for pattern in all_patterns:
        lines.append(
            "| {pattern} | {base} | {v1} | {v2} | {action} |".format(
                pattern=pattern,
                base=grouped["without_skill"][pattern],
                v1=grouped["with_skill_v1"][pattern],
                v2=grouped["with_skill_v2"][pattern],
                action=actions.get(pattern, "复盘失败样例。"),
            )
        )
    return "\n".join(lines)


def summarize(run_dir: Path) -> str:
    benchmark = load_benchmark(run_dir)
    base = config_results(benchmark, "without_skill")
    v1 = config_results(benchmark, "with_skill_v1")
    v2 = config_results(benchmark, "with_skill_v2")
    final_decision = decision(v2, v1)

    return f"""# Skill Engineering Lab 评测报告

## 摘要

评测对象：`{benchmark['skill']}`  
迭代版本：`{benchmark['iteration']}`  
样例数：{benchmark['cases']}  
结论：**{final_decision}**

这个实验室用同一组评测样例对比三种状态：

```text
without_skill -> with_skill v1 -> with_skill v2
```

重点不是生成的视频文案有多漂亮，而是让 Skill 的行为变得可观察、可评分、可改进。

## 核心指标

{metric_table(benchmark)}

## 提升幅度

{lift_table(benchmark)}

## v1 到 v2 的变化

- `description` 增加负向边界：不处理新闻稿、项目计划、issue 分诊或通用非视频写作。
- `SKILL.md` 增加清晰的产出契约：标题、封面文案、Demo 方案、大纲、口播稿和自检。
- 必检项被硬化：标题数量、封面行长、Demo 优先开场、旧方式和新方式对比。
- 新增确定性校验脚本，用于检查创意包结构和文案行长。

## v1 主要失败样例

{badcase_table(benchmark, "with_skill_v1")}

## v2 主要失败样例

{badcase_table(benchmark, "with_skill_v2")}

## 失败模式诊断

{failure_pattern_table(benchmark)}

## 已创建的治理资产

- `evals/cases.json`：12 条种子评测样例。
- `runs/{benchmark['iteration']}/benchmark.json`：基准汇总。
- `runs/{benchmark['iteration']}/*/trace.jsonl`：路由和参考资料加载轨迹。
- `runs/{benchmark['iteration']}/*/grading.json`：结构化评分结果。
- `skills/ai-video-creator-style/scripts/validate_package.py`：确定性校验器。
- `governance/versions.json`：版本假设、风险、指标和决策。
- `governance/reason_archive.json`：失败样例根因归档。
- `governance/regression_set.json`：必须保留的回归样例。

## 下一步动作

1. 从历史项目中加入 3-5 条真实产品信息作为回归样例。
2. 在相同评分接口后面，把确定性模拟器替换成真实大模型调用。
3. 如果要用于现场分享，增加一个轻量 HTML 看板。
4. 在 `governance/versions.json` 中持续记录未来 v3 的变化。
5. 持续保留负向样例，防止 Skill 过度触发。
"""


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    report = summarize(run_dir)
    (run_dir / "report.md").write_text(report, encoding="utf-8")
    (run_dir.parents[1] / "report.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
