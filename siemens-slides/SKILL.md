---
name: siemens-slides
description: Generate Siemens-style slides, ppt images, and presentation slide images as raster output. Use this skill when the user asks for 西门子风格的 slides / ppt / ppt 图片 / presentation slides / slide images, especially Siemens Advanta-style corporate pages, consulting-style one-page report slides, executive summary slides, structured argument slides, strategy analysis pages, roadmaps, maturity pages, comparison/recommendation pages, and other Siemens corporate raster slide images.
---

# Siemens Slides

生成西门子 / Siemens Advanta 风格的 slide 图片。核心原则只有一句：

**模板只是品牌来源，不是布局来源。**

也就是：
- 模板只提供品牌边界：字体、色板、页边距、footer 几何、企业气质。
- 页面结构来自这页要回答的决策问题，以及对应的论证模式。
- layout 只是论证模式的视觉承载结果，不是起点，更不是要复刻的模板形状。
- 在品牌边界和论证结构稳定的前提下，允许模型自主创造局部节奏、组件组合和版面张力。

## 何时使用

使用本 skill：
- 用户要求生成“西门子风格的 slides / ppt / ppt 图片”
- 用户要求生成 “Siemens-style presentation slides / slide images”
- 用户要咨询式一页汇报页、结构化论证页、管理层汇报页、战略分析页、路线图页、成熟度页、对比推荐页等 raster slide image

不要使用本 skill：
- 用户要可编辑 `.pptx` 文件
- 用户要普通海报、网页 UI、插画或非演示文稿图片
- 用户要直接编辑 SVG / HTML / PPT 原生资产

## 设计宪法

每次出图都必须满足这 5 条：
- `Action Title`：标题必须是完整论断句，不是主题标签。
- `One Message Per Page`：每页只回答一个决策问题。
- `Evidence-Backed`：每个结论都要有至少一个视觉证据锚点。
- `Ghost Deck`：不靠讲解也能读懂主要结论。
- `Restraint`：克制、留白、企业化，不做海报或信息图杂耍。

## P0 / P1 / P2 优先级

### P0 红线

不满足就不应直接交付：
- 不是行动标题
- 没有单一 `page_question`
- 没有 L2 hero evidence
- 没有 L5 takeaway
- footer 三分区跑位
- 页面无法归属到一个 `reasoning_pattern`

### P1 主干

影响质量和稳定性，应优先修：
- layout 与模式不匹配
- 页面 ghost-read 不顺
- 纯文字墙
- 色彩语义不清
- 生动感缺失

### P2 扩展

影响先进性和可维护性：
- pattern log
- fallback 映射表
- 引擎能力边界说明
- 多页编排策略完善

## PDCA 工作流

### Plan

负责“决定这页该讲什么、为什么、怎么讲”：
1. 先读 `references/style-guide.md`，只锁定品牌边界，不从模板借 layout。
2. 判断输入类型：
   - `A` 主题词 / 一句话
   - `B` 结构化内容
   - `C` 原始材料
   - `D` 改版请求
   - `E` 多页套件
3. 判断默认受众：默认以 L1/L2 中高层为主，兼顾 L3 下钻。
4. 用 `references/content-brief.md` 填出生成前规格单。
5. 写 `page_question`：明确这页到底在回答什么决策问题。
6. 读 `references/reasoning-patterns.md`，按决策问题选择最合适的 `reasoning_pattern`。
7. 写 `Action Title`，并定义至少一个 `key_evidence` 和一个 `l2_hero_choice`。
8. 判断输入是否内容超载：
   - 如果天然包含多个页面问题，先建议拆页。
   - 如果用户坚持单页，明确标记为压缩模式，再选择压缩策略。
9. 选择 `preferred_layout`：layout 必须是论证模式的结果。
10. 选择 `component_strategy`：决定哪个主要内容区承担 icon、节点、mini-process、关系线或局部结构变化。

### Do

负责“把 plan 变成稳定 prompt 和出图动作”：
1. 按 L1-L5 信息层级组装 prompt。
2. 注入品牌 token、语义色、footer 几何、组件语义。
3. 明确模式与 layout 的关系：layout 只是视觉承载，不是结构来源。
4. 固定 footer 文案和 footer 三分区几何；位置关系默认参考 Advanta 母版，不得自由漂移。
5. 用 `$imagegen` 直接生成最终图片。

### Check

负责“双层验证”：
1. Layer 1：Prompt-Level 自检
2. Layer 2：Visual-Level 回看
3. 检查项按 P0 / P1 / P2 分级
4. 明确哪些 fail 会阻断、哪些 fail 允许降级

### Act

负责“修正、降级、积累”：
1. 首次失败：重写 prompt 并重生一次。
2. 二次仍失败：进入降级交付。
3. 记录 `input_type`、`reasoning_pattern`、`preferred_layout`、`retry_count`、`known_issues` 等 pattern log 字段。
4. 把失败模式沉淀成后续 `don't` 或 fallback 规则。

## 引擎能力边界与降级策略

### 已知能力边界

- 中文长句渲染不稳定，尤其在标题或高密度正文里。
- 精确几何是近似而非像素级，不应把局部坐标复刻当成可交付标准。
- 多层级密集文字仍然是弱项，越长越容易牺牲层级清晰度。
- 复杂图表不可靠，优先用 hero number、结构化色块或流程证据替代。
- 颜色接近但不保证完全精确，必须用 token + 语义双重约束。

### Retry / Degrade

1. 第一次生成：按完整规格出图。
2. 第一次 retry：简化最复杂的视觉区，例如合并组件、减少文字层级、弱化次要结构。
3. 第二次 retry：进入降级模式。
4. 降级交付：
   - 最佳近似图片
   - 结构化 slide brief，包含：
     - `Action Title`
     - 完整层级文本
     - `reasoning_pattern`
     - `preferred_layout`
     - `component_strategy`
     - 品牌参数速查
     - 已知偏差

## 内容页默认规则

- 内容页默认追求 `Action Title`，而不是主题标题。
- 每页只回答一个问题；如果同一页要回答两个问题，优先拆页。
- layout 只能是论证模式的结果，不能是内容组织的起点。
- 每页至少要有一个证据锚点，例如：
  - 大数字
  - 对比关系
  - 图表式信息块
  - 优先级结构
  - before / after
  - 流程证据
- 内容页不应退化成纯文字排版；至少要有一个主要内容区承担结构化视觉证据。
- 默认保留底部 takeaway strip，或至少保留明确的 L5 结论收束区。
- 高密度单页压缩时优先考虑 `⑤ 结构化总览`，必要时可借用 MECE 的分组纪律，但不要把 `MECE` 当成页面显性语言。

## 多页编排（P2 预留）

当用户要求生成 ≥ 2 页的汇报时，先建立 `storyline_mode`，再逐页执行 PDCA：
- `情境—冲突—方案`
- `现状—目标—路径`
- `总—分—总`
- `并列论证`

当前只定义接口和流程，不把多页 orchestration 作为本轮主阻塞项。

## Fallback 映射表（P2 预留）

当 `reasoning-patterns.md` 或 `layouts.md` 不可用时，可使用以下精简 fallback：

| Reasoning Pattern | Preferred Layout | 主内容区策略 |
|---|---|---|
| `① Sit-Com-Sol` | 双 / 三栏递进结构 | 因果递进 + 轻量图标容器 |
| `⑤ 结构化总览` | 等分并列结构 | 等权内容区 + icon 头部 |
| `⑥ 对比分析` | 左右双栏或对照表 | 并列对照 + 推荐高亮 |
| `⑭ 战略路线图` | 水平路径或阶段台阶 | 阶段节点 + 顺序箭头 |
| `⑰ 端到端数据流` | 线性流程带 | 节点链 + 流向箭头 |

这张映射表只作为降级 fallback，不替代完整模式库。

## 反馈循环（P2 预留）

每次交付后预留以下记录字段：
- `input_type`
- `reasoning_pattern`
- `preferred_layout`
- `retry_count`
- `degraded`
- `known_issues`
- `user_feedback`

当前不要求持久化，但应把这些字段当成可观测性契约固定下来。

## Do

- 先问“这页在证明什么”，再问“它应该长成什么样”。
- 先选 `reasoning_pattern`，再选 `preferred_layout`。
- 把标题写成“量化证据 + 因果判断 + 行动指向”。
- 让 L1-L5 信息层级清晰可读。
- 把局部 icon、节点、mini-process、关系线当作论证节奏工具，而不是装饰。
- 让页面在统一网格下保留局部变化，避免所有主要内容区完全同构。
- 允许模型在一个主内容区里做克制但明显的结构创新，例如非完全对称分栏、嵌入式 mini-process、局部关系链或视觉主次反转。
- 把 footer 当成品牌组成部分，而不是随意漂浮的说明文字。
- 浅色内容页中，右下 `SIEMENS` 品牌字标使用 Siemens Petrol `#009999`。

## Don't

- 不要“先挑 layout 再塞内容”。
- 不要把模板坐标、现成母版形状或本地文件路径当作可直接复刻的布局来源。
- 不要把内部方法词直接写进页面文案里，例如 `MECE`、`reasoning pattern`、`layout type`。
- 不要写主题型标题，例如以“分析 / 介绍 / 概况 / 说明”收尾。
- 不要生成纯文字说明页。
- 不要为了“生动”而海报化、信息图化、营销化。
- 不要让 hero 区出现无语义的多主色并列。
- 不要让 takeaway、正文或主图形侵入 footer band。
- 不要把浅色页右下 `SIEMENS` 做成非 Siemens Petrol 的近似色。

## Prompt 编写重点

prompt 中优先写清楚：
- `page_question`
- `reasoning_pattern`
- `Action Title`
- `key_evidence`
- 是否建议拆页，或是否属于压缩模式
- `preferred_layout` 与大框架布局
- L1-L5 信息层级
- 官方色板、语义色、主强调色与风险色边界
- icon / glyph / 节点的颜色语义与允许范围
- `component_strategy`
- footer 三分区位置关系、footer 文案、takeaway 与 footer band 的边界
- 页脚文字带必须从页码右侧直接开始并保持左锚定，绝不能做成视觉居中的底部说明文字
- 右下 `SIEMENS` 品牌字标的颜色要求
- 允许的创意空间：哪些区域可以通过 icon、关系线、节奏断点或非同构内容块增强页面生命力
- Siemens Advanta corporate consulting 风格
- 直角矩形、禁忌项和 Ghost Deck 可读性目标

## 核心硬规则

- 产物是图片格式 slide。
- 最终 slide 图片必须由 `$imagegen` 生成；不要使用 Python、PIL/Pillow、matplotlib、Plotly、SVG/HTML/canvas 截图或脚本绘图来生成最终图片。
- Python 只能用于文件整理、尺寸检查、元数据读取或非图像生成的辅助验证；不能作为 slide 渲染/绘图引擎。
- 默认输出 `16:9`、`4K`，目标 `3840x2160`。
- 浅色页默认白底 `#FFFFFF`，标题与正文默认 Deep Blue `#000028`。
- 浅色页默认功能 icon、业务 icon、能力 icon 优先使用 Deep Blue `#000028`；流程 / 连接 icon 才可使用 Light Petrol `#00C1B6`；风险 icon 才可使用 Risk Orange `#E37200`。
- footer 三分区几何固定参考 `references/style-guide.md` 与 `references/layouts.md` 中归纳的 Advanta 母版关系，不得自由改动。
- footer 中的文字带默认必须左对齐、左锚定，并从页码右侧几乎贴齐开始；不得将整段 footer text 排成页面底部中央的独立文案。
- 普通内容页默认必须使用 Advanta 内容页 footer family，包括 compact `SIEMENS` logo 几何；不要混入封面或特殊版式的更大 logo family。
- 浅色页右下 `SIEMENS` 品牌字标默认必须使用 Siemens Petrol `#009999`；深色页可改为 White `#FFFFFF`。
- 所有模式都必须避免 dead text-wall，不得退化成纯文字说明页。
- 视觉目标始终是 Siemens corporate presentation page，不是 poster，不是 startup landing page，不是 marketing hero banner。

## 资源导航

- 风格、品牌系统与信息层级：`references/style-guide.md`
- 论证模式体系：`references/reasoning-patterns.md`
- 布局说明、模式映射与选型建议：`references/layouts.md`
- 质量门禁：`references/quality-checklist.md`
- 生成前规格单：`references/content-brief.md`
- 组件速查表：`references/components-cheatsheet.md`
- 组件语义词典：`references/components.md`
- 品牌与示例图资产：`assets/branding/`、`assets/reference-slides/`
