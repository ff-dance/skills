---
name: siemens-slides
description: 生成西门子 Advanta 风格的中文咨询汇报页图片。适用于中文业务汇报、一页结论页、结构化论证页、战略分析页、路线图页、成熟度页、对比推荐页等场景。
---

# Siemens Slides

生成西门子 Advanta 风格的中文咨询页图片。核心原则只有一句：

**模板只是品牌来源，不是布局来源。**

## 何时使用

使用本 skill：
- 用户要中文西门子风格的 slide / ppt 图片
- 用户要中文高管汇报页、咨询式一页页、战略分析页、路线图、成熟度、对比推荐页
- 用户要最终交付的是图片，而不是可编辑 `.pptx`

不要使用本 skill：
- 用户要可编辑 `.pptx`
- 用户要网页 UI、海报、插画、营销长图
- 用户要直接编辑 SVG / HTML / PPT 原生资产

## 中文单语约束

- 默认所有 `page_question`、`Action Title`、`supporting_points`、`takeaway`、`slide_spec` 都使用中文。
- 不为英文标题、英文页脚、双语兼容单独优化。
- 内部可使用 layout id、pattern id、组件 id 作为路由语言，但最终页面文案默认保持中文。

## P0 硬规则

以下任一项不成立，就不应直接交付：

- 只有一个 `page_question`
- 标题是结论句式 `Action Title`，不是主题标签
- 至少有一个 `key_evidence` 和一个 `l2_hero_choice`
- 页面可归属到一个明确的 `reasoning_pattern`
- 页面有清晰的 L5 takeaway / 收束区
- 使用普通内容页 footer family，不漂移、不侵入
- 色彩只使用允许的品牌 token 和语义色

## 默认工作流

### Plan

1. 先读 `references/content-brief.md`，把原始输入压成结构化 `slide_spec`。
2. 再读 `references/reasoning-patterns.md`，确定 `reasoning_pattern`。
3. 只在 pattern 明确后，再读 `references/layouts.md` 选择 `preferred_layout`。
4. 遇到箭头、节点、icon、mini-process 等局部结构需求时，先读 `references/components-cheatsheet.md`，再按需补读 `references/components.md`。
5. 品牌、色彩、footer 几何、logo family 一律以 `references/style-guide.md` 为准。

## `reasoning_pattern` canonical 规则

- `reasoning_pattern` 必须使用官方模式库中的 canonical 名称，不要自造同义模式名。
- 不要输出自由命名，例如：
  - `闭环机制`
  - `优先级排序`
  - `对比推荐型`
  - `因果链路论证`
  - `投资收益路径三段式论证`
- 这些情况应回到 canonical 模式，例如：
  - 系统 / 数据 / 异常回传闭环：`⑰ 端到端数据流`
  - 多类问题并存、问“真正先抓什么”：默认优先 `② 根因分析`
  - 已提供影响/难度/排序标准并要排先后：可用 `④ 问题优先级矩阵`
  - AI 识别出传统经验没看见的真实约束或隐藏根因：优先 `⑨ AI驱动根因发现`
  - 蓝图页在强调分层骨架、核心平台层、结构优先：优先 `⑪ 技术架构蓝图`
  - 问“90天内先做哪几件、先批哪3个动作、哪些动作能快速见效”：优先 `㉓ 速赢清单`
  - 方案二选一并要明确推荐：`⑥ 对比分析`
  - 管理层风险提醒页、要突出 Top 风险与受控风险：优先 `㉒ 风险全景图`
  - 投资 / 收益 / 路径的董事会单页摘要：默认优先 `⑤ 结构化总览`

## 高频误判纠正

- 当页面主题是“数据如何在系统之间流动、如何形成异常回传闭环”，不要写成抽象“闭环机制”，应直接使用 `⑰ 端到端数据流`。
- 当原始纪要里同时有插单、主数据、缺件、报工、接口、执行纪律等多类问题，且问题是在问“先抓什么”，不要直接写成泛化“优先级排序”，应先判断是不是 `② 根因分析`；只有在题目明确提供排序维度时才转 `④ 问题优先级矩阵`。
- 当题目强调“AI 看到了传统经验没看见的真实瓶颈 / 隐藏根因 / 关键约束”，即使页面里带有“传统判断 vs AI发现”的对照，也不要退回 `⑥ 对比分析`；这种对照只是证据呈现方式，pattern 应优先使用 `⑨ AI驱动根因发现`。
- 当题目是“整理一页蓝图页 / 架构页 / 全景蓝图页”，且原始材料强调的是真正需要 `分层骨架`、`核心平台层`、`结构优先`、`不要接口清单`，不要退成泛化 `⑤ 结构化总览`；应优先使用 `⑪ 技术架构蓝图`。
- 当题目是在提醒管理层“先盯住哪些风险”，并要求有 Top 风险、次级风险、受控风险提示时，不要直接退成 `④ 问题优先级矩阵`；只有题目明确给出排序维度或二维打分轴时，才使用矩阵。默认优先 `㉒ 风险全景图`。
- 当题目强调 `90天内见效`、`只先批3件事`、`短期快速见效` 这类速赢筛选时，不要退回 `⑤ 结构化总览`，应优先使用 `㉓ 速赢清单`。
- 当页面只是董事会摘要或管理层一页总览，不要发明新的 pattern 名称，优先从 `⑤ 结构化总览`、`⑩ 愿景 vs 现状 + 差距`、`⑬ ROI` 中选择。

### Do

1. 先产出中文 `slide_spec`，再把它转成最终出图 prompt。
2. layout 只能是论证模式的视觉承载结果，不能先挑模板再塞内容。
3. 最终图片必须直接通过 `$imagegen` 生成，不用脚本绘图替代。

## `slide_spec` 输出契约

生成前先写一个严格合法的中文 `slide_spec`，字段必须满足：

- `page_question`：字符串，只回答一个问题
- `action_title`：字符串，中文结论句
- `reasoning_pattern`：字符串，只选一个模式
- `key_evidence`：字符串数组，至少 1 条
- `l2_hero_choice`：字符串，不能写成对象
- `supporting_points`：字符串数组，默认 3 到 5 条
- `preferred_layout`：字符串，不能写成对象
- `component_strategy`：字符串，不能写成对象
- `footer_spec` 必须包含：
  - `page_number = "Page X"`，必须保留这个占位符，不要替换成具体页码
  - `footer_text`
  - `brand_mark = "SIEMENS"`
  - `footer_family = "advanta-content-footer"`
  - `logo_family = "compact-content-page-logo"`
  - `text_alignment = "left"`
- `color_strategy` 必须包含：
  - `page_mode = "light"`
  - `body_text = "Deep Blue"`
  - `hero_accent`
  - `connector_support = "Light Petrol"`
  - `positive_accent = "Advanta Green"`
  - `risk_accent = "Risk Orange"`
- `overflow_recommendation` 只能是：
  - `single-page`
  - `suggest-split`
  - `compressed-single-page`
  - `multi-page-orchestration`
- `degrade_mode` 只能是：
  - `none`
  - `brief-only`
  - `image-plus-brief`

不要把这些字段改写成自由结构，也不要自造同义字段，例如：

- 不要把 `l2_hero_choice` 写成对象
- 不要把 `preferred_layout` 写成对象
- 不要把 `component_strategy` 写成对象
- 不要把 `hero_accent` 改写成 `hero_primary`
- 不要把 `overflow_recommendation` 写成 `normal-single-page`

### Check

1. 用 `references/quality-checklist.md` 做自检。
2. 如果要做 SkillOpt-style 门禁，先跑 `scripts/skillopt_spec_lint.py` 做 P0 结构检查，再用 `evals/skillopt/rubric.md` 做 judge 评分。
3. 对最终图片只做 smoke check，不把图像评分放进主训练 gate。

### Act

1. 第一次失败：重写 prompt 并重试一次。
2. 第二次仍失败：降级为 `image-plus-brief`，交付最佳近似图 + 结构化 `slide_spec`。
3. 重复失败应沉淀为新的 `must_avoid`、fallback 或 gating 规则，而不是继续堆长 prompt。
