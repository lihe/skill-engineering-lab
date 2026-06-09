# Skill Engineering Lab 评测报告

## 摘要

评测对象：`ai-video-creator-style`  
迭代版本：`iteration-001`  
Provider：`mock` / `deterministic-v1`  
样例数：12  
结论：**发布**

这个实验室用同一组评测样例对比三种状态：

```text
without_skill -> with_skill v1 -> with_skill v2
```

重点不是生成的视频文案有多漂亮，而是让 Skill 的行为变得可观察、可评分、可改进。

## 核心指标

| 配置 | 通过率 | 触发召回率 | 过度触发率 | 平均 Token | 平均耗时 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 无 Skill | 16.7% | 不适用 | 不适用 | 720 | 480 ms |
| 使用 Skill v1 | 75.0% | 80.0% | 50.0% | 1142 | 828 ms |
| 使用 Skill v2 | 100.0% | 100.0% | 0.0% | 935 | 625 ms |

## 提升幅度

| 对比 | 质量提升 | Token 变化 |
| --- | ---: | ---: |
| v1 相对基线 | 58.3% | 58.7% |
| v2 相对基线 | 83.3% | 29.9% |
| v2 相对 v1 | 25.0% | -18.2% |

## v1 到 v2 的变化

- `description` 增加负向边界：不处理新闻稿、项目计划、issue 分诊或通用非视频写作。
- `SKILL.md` 增加清晰的产出契约：标题、封面文案、Demo 方案、大纲、口播稿和自检。
- 必检项被硬化：标题数量、封面行长、Demo 优先开场、旧方式和新方式对比。
- 新增确定性校验脚本，用于检查创意包结构和文案行长。

## v1 主要失败样例

| 样例 | 类型 | 得分 | 失败模式 |
| --- | --- | ---: | --- |
| `boundary-sparse-brief` | 边界 | 20.0% | 触发不匹配、产出不完整、风格较弱、泛化风险 |
| `extension-cover-only` | 扩展 | 20.0% | 触发不匹配、产出不完整、风格较弱、泛化风险 |
| `negative-press-release` | 负向 | 50.0% | 触发不匹配、产出不完整、效率成本偏高 |

## v2 主要失败样例

没有失败样例。

## 失败模式诊断

| 失败模式 | 无 Skill | v1 | v2 | 建议动作 |
| --- | ---: | ---: | ---: | --- |
| 产出不完整 | 10 | 3 | 0 | 硬化必选产出检查清单。 |
| 效率成本偏高 | 0 | 9 | 0 | 把确定性检查下沉到脚本，并裁剪参考资料。 |
| 泛化风险 | 4 | 2 | 0 | 把改写和边界样例加入回归集。 |
| 触发不匹配 | 0 | 3 | 0 | 收紧或扩展 `description` 的触发边界。 |
| 风格较弱 | 10 | 10 | 0 | 补强参考资料和示例。 |

## 已创建的治理资产

- `evals/cases.json`：12 条种子评测样例。
- `runs/iteration-001/benchmark.json`：基准汇总。
- `runs/iteration-001/*/trace.jsonl`：路由和参考资料加载轨迹。
- `runs/iteration-001/*/provider.json`：Provider、模型和真实 usage 信息。
- `runs/iteration-001/*/grading.json`：结构化评分结果。
- `providers/`：统一 mock、OpenAI、Anthropic 的模型运行适配层。
- `skills/ai-video-creator-style/scripts/validate_package.py`：确定性校验器。
- `governance/versions.json`：版本假设、风险、指标和决策。
- `governance/reason_archive.json`：失败样例根因归档。
- `governance/regression_set.json`：必须保留的回归样例。

## 下一步动作

1. 从历史项目中加入 3-5 条真实产品信息作为回归样例。
2. 将 OpenAI / Anthropic provider 接入稳定回归环境，补齐密钥管理和费用上限。
3. 引入 LLM Judge 作为风格评价补充，但保留确定性检查作为主验收。
4. 在 `governance/versions.json` 中持续记录未来 v3 的变化。
5. 持续保留负向样例，防止 Skill 过度触发。
