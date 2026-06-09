"""Deterministic provider used for stable demos and regression tests."""

from __future__ import annotations

import time
from typing import Any

from .base import ProviderResult, SkillContext
from .routing import should_trigger


def estimate_tokens(config: str, triggered: bool, should_trigger_case: bool) -> int:
    if config == "without_skill":
        return 760 if should_trigger_case else 520
    if config == "with_skill_v1":
        return 1250 if triggered else 820
    return 1010 if triggered else 560


def estimate_duration_ms(config: str, triggered: bool) -> int:
    if config == "without_skill":
        return 480
    if config == "with_skill_v1":
        return 930 if triggered else 520
    return 650 if triggered else 500


def titles(product: str, config: str) -> list[str]:
    if config == "without_skill":
        return [
            f"{product} 产品介绍",
            f"{product} 功能解析",
            "AI 工具如何提升效率",
        ]
    if config == "with_skill_v1":
        return [
            f"{product} 深度测评：AI 工作流效率提升",
            "AI 正在改变视频创作方式",
            "这款 AI 工具功能很全面",
            "从功能到场景，一次讲清楚",
            "普通人也能用 AI 做复杂任务",
            "AI 工具的新机会来了",
            "一次看懂 AI 产品的核心价值",
            "这个工具适合哪些真实场景？",
        ]
    return [
        "别再手搓流程了，AI 已经能自己跑评测",
        "我用 AI 做了一个 Skill 评测台，结果有点意外",
        "这不是写提示词，而是在造一个能力闭环",
        "一个 Skill 到底有没有用？这次直接跑给你看",
        "AI Agent 的隐藏用法：把经验变成可回归资产",
        "以前靠感觉改 Skill，现在直接看失败样例",
        "这才是我想要的 Skill 工程化流程",
        "把同一个任务跑三遍，差距一下就出来了",
        "不是更长的提示词，而是可治理的能力包",
        "Skill 评测能有多直观？我实测后有点意外",
    ]


def cover_texts(config: str) -> list[str]:
    if config == "without_skill":
        return []
    if config == "with_skill_v1":
        return [
            "AI视频创作工具全面提升效率 / 一站式完成创意策划脚本封面",
            "智能内容生产解决方案 / 帮你快速完成视频策划",
            "让AI帮你做内容营销 / 从标题到脚本一次完成",
            "AI产品视频创作 / 效率提升明显",
            "AI工具全流程提效 / 内容团队都能使用",
            "从产品亮点出发 / 做一条完整视频",
        ]
    return [
        "别再凭感觉改 / 让评测说话",
        "Skill闭环 / 当场跑出来",
        "不是长提示词 / 是能力资产",
        "同题跑三遍 / 差距看得见",
        "失败归因 / 下一版就改",
        "标题封面脚本 / 一次全验收",
        "触发对不对 / 轨迹里见",
        "AI真能干活 / 流程自己跑",
    ]


def generic_non_video_output(case: dict[str, Any], config: str) -> str:
    if case["id"] == "negative-project-plan":
        return f"""# 项目计划：{case['brief']['product']}

## 里程碑
1. 澄清项目需求。
2. 创建 issue 流转规则。
3. 定义可交给 Agent 执行的状态标准。

## 状态流转
needs-triage -> ready-for-agent -> in-progress -> review -> done
"""
    return f"""# 官方新闻稿草稿：{case['brief']['product']}

## 摘要
{case['brief']['product']} 面向企业用户发布一项新的 AI 产品更新。

## 正文
这版草稿保持官方发布口吻，不生成创作者视频脚本。
"""


def positive_output(case: dict[str, Any], config: str, triggered: bool) -> str:
    product = case["brief"]["product"]
    visible = case["brief"]["visible_result"]
    viewer = case["brief"]["viewer"]

    if not triggered:
        return f"""# 通用 AI 产品内容方案

## 标题建议
1. {product} 产品介绍
2. {product} 如何提升效率
3. AI 工具的新机会

## 内容大纲
1. 产品背景
2. 核心功能
3. 应用场景

## 备注
这是一版通用内容方案，没有加载视频风格 Skill。
"""

    if config == "with_skill_v1":
        return f"""# AI 产品视频创意包 v1

## 标题候选
{chr(10).join(f"{idx + 1}. {title}" for idx, title in enumerate(titles(product, config)))}

## 封面文案
{chr(10).join(f"{idx + 1}. {text}" for idx, text in enumerate(cover_texts(config)))}

## Demo 方案
展示 {product} 的主要功能，并说明它能帮助 {viewer} 提升效率。

## 三段式大纲
1. 产品背景：介绍 {product} 的能力和定位。
2. 功能展示：列出核心功能和使用场景。
3. 总结价值：说明它适合哪些用户。

## 口播稿
今天给大家介绍一个 AI 产品，叫 {product}。它可以帮助 {viewer} 提升效率，完成更复杂的任务。我们会先看它的核心功能，再看几个实际场景。整体来说，它能把原来需要人工处理的流程变得更自动化。最后，如果你也在做类似工作，可以关注一下这个方向。
"""

    return f"""# AI 视频创意包 v2

## 标题候选
{chr(10).join(f"{idx + 1}. {title}" for idx, title in enumerate(titles(product, config)))}

## 封面文案
{chr(10).join(f"{idx + 1}. {text}" for idx, text in enumerate(cover_texts(config)))}

## Demo 方案
开场直接展示可见结果：{visible}。随后把同一个产品信息分别跑过 without_skill、with_skill v1、with_skill v2，让观众看到标题、封面、脚本和失败样例归因的差异。

## 三段式大纲
1. 第一部分｜结果先上屏：先给观众看 {visible}，再解释这不是普通视频策划，而是 Skill 工程化闭环。
2. 第二部分｜三轮对照实测：without_skill 泛、v1 有框架但有失败样例、v2 通过 description 和 checklist 收紧后更稳。
3. 第三部分｜价值总结：不是把提示词写长，而是把经验变成可触发、可评测、可治理的能力资产。

## 口播稿
第一部分｜产品引出
你现在看到的这份报告，不是我手动整理的，而是同一批样例跑了三遍之后自动生成的结果。第一遍没有 Skill，输出很泛；第二遍用了 v1，结构好了，但封面太长、标题不够 B 站；第三遍 v2 加了触发边界和检查脚本，失败样例直接少了一截。这次我用的是 {product}，它要展示的不是一个更会写文案的 AI，而是一套 Skill 从编写、评测到治理的闭环。

第二部分｜亮点 + 实测展示
首先，我们给它一个真实产品信息：{visible}。without_skill 会直接写成产品介绍，标题像发布会，大纲也偏功能列表。接下来切到 v1，可以看到它已经知道要写标题、封面、大纲和口播，但问题也很明显：封面文案过长，标题没有足够的创作者实测感，负向样例里甚至会把新闻稿误判成视频任务。重点是，这些问题不是靠感觉改，而是都被评分器拆成触发、产出、风格、效率和泛化。最后再到 v2，我们改 description，明确不处理新闻稿和项目计划；改 checklist，要求标题数量、封面行长和 Demo 优先；再加一个脚本验证输出结构。这样，整个 Skill 的修正路径就清楚了。

第三部分｜价值总结 + 行动号召
真正关键的是，Skill 不是长提示词，而是一个能被持续验证的能力包。以前你可能是凭感觉改，现在你可以看轨迹、看失败样例、看质量提升。别再只问这个 Skill 会不会跑了，先问它有没有稳定带来净增益。如果你也在做 Agent 工作流，建议先从 12 条样例开始，把你的 Skill 跑起来。

## 自检清单
- 标题数量：10 个。
- 封面文案：8 个，包含 2-3 行短句。
- Demo：首屏展示可见结果。
- 结构：三段式大纲和三段式口播一致。
- 风格：包含旧方式 vs 新方式、实测感、不是 X 而是 Y。
"""


def generate_output(case: dict[str, Any], config: str, triggered: bool) -> str:
    if not case["should_trigger"] and not triggered:
        return generic_non_video_output(case, config)
    if not case["should_trigger"] and triggered:
        return positive_output(case, "with_skill_v1", True)
    return positive_output(case, config, triggered)


class MockProvider:
    """Provider that simulates model output deterministically."""

    name = "mock"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or "deterministic-v1"

    def generate(
        self,
        *,
        case: dict[str, Any],
        config: str,
        skill_context: SkillContext,
    ) -> ProviderResult:
        triggered = should_trigger(config, case)
        token_estimate = estimate_tokens(config, triggered, case["should_trigger"])
        duration_ms = estimate_duration_ms(config, triggered)

        start = time.perf_counter()
        output_text = generate_output(case, config, triggered)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        trace_events: list[dict[str, Any]] = [
            {
                "event": "provider_generate",
                "provider": self.name,
                "model": self.model,
                "simulated": True,
                "routing_policy": config,
            }
        ]
        if triggered:
            trace_events.append(
                {
                    "event": "reference_loaded",
                    "files": ["title-formulas.md", "cover-style.md", "checklist.md"],
                }
            )

        return ProviderResult(
            output_text=output_text,
            actual_triggered=triggered,
            token_estimate=token_estimate,
            duration_ms=duration_ms + elapsed_ms,
            simulated=True,
            provider=self.name,
            model=self.model,
            trace_events=trace_events,
        )
