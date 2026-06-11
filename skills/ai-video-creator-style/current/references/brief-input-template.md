# Brief Input Template

Use this reference when a client brief is messy, incomplete, or spread across chat messages. The goal is to normalize every brief into the same fields before writing titles, outline, demo, or script.

## When To Read

Read this file when:

- The user asks to create a product brief template.
- A client brief is long, scattered, or unclear.
- The brief needs to be converted into fixed fields before creative work.
- There are possible brand, legal, privacy, claim, platform, or CTA restrictions.

## Minimum Usable Brief

If time is tight, collect at least these fields:

1. Product name.
2. One-sentence product positioning.
3. Target audience.
4. Core scene or user pain.
5. The visible result the video should show.
6. 1 core capability that must be demonstrated.
7. Red lines or forbidden claims.
8. Platform, duration, CTA, and required tags.

If any of these are missing, either ask a short clarification or mark a reasonable assumption before writing.

## Client-Facing Template

Ask the client to fill this out. Empty fields are acceptable, but red lines and required claims should be explicit.

```markdown
# 视频合作 Brief

## 1. 产品基础信息

- 产品名称：
- 产品官网 / 下载地址：
- 产品类型：
- 一句话产品定位：
- 当前阶段：已上线 / 内测 / 新版本发布 / 活动推广 / 其他
- 竞品或对标对象：

## 2. 内容目标

- 这条视频最希望观众记住什么？
- 希望观众看完后做什么？下载 / 预约 / 试用 / 关注 / 报名 / 私信 / 其他
- 是否有必须出现的口径或 slogan？
- 是否有不能出现的表达？

## 3. 目标观众

- 主要观众是谁？
- 他们现在最大的痛点是什么？
- 他们为什么会关心这个产品？
- 更适合的账号方向：AI 工具 / Agent 实测 / AI Coding / 一人公司 / 内容创作 / 办公自动化 / 其他

## 4. 核心场景

- 本期视频想围绕哪个真实场景展开？
- 旧方法通常怎么做？麻烦在哪里？
- 用产品后，最直观的结果是什么？
- 开头 10 秒最好能看到什么结果？

## 5. 必露能力

请按优先级填写，最多 4 个。

1. 核心必露能力：
   - 想证明什么：
   - 最好怎么展示：
2. 次要能力：
   - 想证明什么：
   - 最好怎么展示：
3. 可选能力：
   - 想证明什么：
   - 最好怎么展示：
4. 可选能力：
   - 想证明什么：
   - 最好怎么展示：

## 6. Demo 与素材

- 是否已有推荐 Demo？
- 是否可以录屏真实产品界面？
- 是否提供测试账号、素材、数据、样例文件？
- 是否有必须展示的页面、按钮、结果或流程？
- 是否有不能展示的页面、数据或用户信息？

## 7. 平台与发布要求

- 分发平台：
- 视频时长要求：
- 产品露出要求：
- 标题是否必须出现产品名：
- 必带话题 / 标签：
- 封面是否有要求：
- 发布时间或交付时间：

## 8. CTA 与转化

- 下载 / 访问 / 报名入口：
- 评论区或私信引导口径：
- 是否有优惠、活动、邀请码、报名截止时间：

## 9. 内容红线

- 不能提到的竞品：
- 不能出现的功能或场景：
- 不能使用的绝对化表达：
- 隐私、支付、金融、医疗、法律等敏感限制：
- 需要额外免责声明的内容：

## 10. 可引用事实

请只填写确定可公开使用的信息。

- 官方数据：
- 用户案例：
- 版本信息：
- 获奖 / 排名 / 合作方：
- 其他可公开背书：
```

## Internal Normalized Brief

After reading a messy brief, convert it into this structure before creative work.

```markdown
## Brief 归一化

### 产品定位
- 产品名称：
- 产品类型：
- 一句话定位：
- 当前阶段：

### 内容目标
- 核心传播目标：
- 观众看完后的行动：
- 主要平台：
- 视频时长：

### 目标观众
- 核心人群：
- 他们的痛点：
- 他们会被什么结果吸引：

### 核心场景
- 真实使用场景：
- 旧方法：
- 新方法：
- 开头可见结果：

### Demo 方向
- Demo 一句话：
- 开场结果：
- 主要流程：
- 迭代 / 加限制：
- 最终结果：

### 必露能力
- 核心必露能力：
- 次要能力：
- 可选能力：

### 口径与禁区
- 必须出现：
- 禁止出现：
- 需要弱化或避免的表达：
- 需要免责声明：

### 发布与转化
- 标题是否带产品名：
- 必带话题：
- CTA：
- 官网 / 下载地址：

### 素材与权限
- 可用素材：
- 需要录屏：
- 测试账号 / 数据：
- 不能展示：

### 待确认问题
- [只列会影响事实准确性、合规或 Demo 可行性的问题]

### 生成假设
- [如果没有向客户追问，写清楚本次创作基于哪些假设]
```

## Extraction Rules

- Prefer scene and result over feature lists.
- Convert every product feature into "what can be shown on screen".
- Separate required facts from creative assumptions.
- Do not invent official claims, numbers, rankings, security promises, or legal conclusions.
- If the title must not include the product name, mark it explicitly.
- If the brief requires brand exposure, keep product name out of the title by default but ensure natural script exposure.
- If red lines involve privacy, finance, payment, medical, legal, or minors, keep them in `口径与禁区` and avoid risky demos.
- If the brief asks for many abilities, choose 1 core capability and 2-3 supporting capabilities; put the rest in optional notes.
- If there is no visible demo, redesign the scene before writing the script.

## Clarifying Questions

Ask at most 3 questions before writing, only when the missing information affects:

- Factual accuracy.
- Legal, privacy, or platform compliance.
- Whether the demo can actually be shown.
- Required brand exposure, CTA, or delivery format.

Otherwise, proceed with assumptions and label them.
