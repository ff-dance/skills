# Siemens Slide Quality Checklist

用这个清单做 `siemens-slides` 的质量门禁。目标不是机械打分，而是明确什么算咨询级页面，什么必须判定为失败。

## Layer 1: Prompt-Level Validation

### P0

- `Action Title` 是否成立，而不是主题标签。
- `page_question` 是否唯一。
- `reasoning_pattern` 是否明确。
- `key_evidence` 是否存在。
- 是否存在清晰的 L2 hero choice。
- 是否存在清晰的 L5 takeaway 计划。

### P1

- `preferred_layout` 是否是论证模式的结果，而不是起点。
- 是否写明 footer 文案和三分区几何。
- 是否写明主强调色、风险色和 `component_strategy`。
- 如果输入超载，是否已写明拆页建议或压缩策略。

### P2

- 是否写明 `known_limitations`。
- 是否写明 `degrade_mode`。
- 是否为多页场景预留 `storyline_mode`。

## Layer 2: Visual-Level Validation

### P0

- 标题是否为行动标题，而不是主题标签。
- 页面是否仍只有一个主要决策问题。
- 页面是否存在清晰的 L2 hero evidence。
- 页面是否存在清晰的 L5 takeaway。
- 页面是否 evidence-backed，而不是纯文字说明页。
- 页面是否仍可明确归属到一个 `reasoning_pattern`。
- 页面是否避免把内部方法词直接暴露成版面文案，除非用户明确要求。

### P1

- 页面是否仍像 Siemens corporate consulting presentation page。
- 页面是否可以 ghost-read：只看标题、核心证据、结论收束就能理解。
- 主模块是否吸附到同一栅格。
- 是否存在无依据的大面积空白。
- 页面是否“生动但克制”，而不是死板文字墙，也不是海报化信息图。
- 页面是否至少有一个主要内容区带有局部结构变化，例如 mini-process、icon-assisted summary、节点链或细连接关系。
- 页面是否在统一网格内保留了适度的非同构节奏，而不是所有模块完全同形同构。

### P2

- 页面是否至少使用了 3 到 5 个克制的 icon / 节点 / 流程件来提供节奏，除非该模式明确不需要这么多。
- 颜色是否整体符合 Siemens 企业观感，而不仅仅是 hex 接近。

## Footer / Brand Zone

### P0

- footer 三分区是否完整：
  - 左下 `Page X`
  - 左锚定 footer text
  - 右下 `SIEMENS`
- footer 三分区是否未被主体内容侵入。

### P1

- footer 三分区位置是否符合母版关系：
  - 页码区约 `x=3.37% / y=92.02% / width=5.31%`
  - 页脚区约 `x=8.69% / y=92.02% / width=70.87%`
  - 品牌区约 `x=87.23% / y=93.60% / width=9.45% / right_edge=96.68%`
- 页码与页脚文字带是否在同一基线上近乎贴齐，而不是彼此分离过远。
- 页码区右边界与页脚文字带左边界是否近乎无缝衔接，而不是被拉出明显空隙。
- 页脚文字带是否从页码右侧直接开始并保持左对齐，而不是被排成视觉居中的底部说明文字。
- takeaway strip、正文或主图形是否侵入 footer band。
- 浅色内容页中，右下 `SIEMENS` 是否既使用 Siemens Petrol `#009999`，又保持 compact 内容页 logo 几何，而不是近似青绿或过大的 logo family。

## 色彩 / 语义

### P0

- 颜色是否超出品牌 token 和语义色范围。
- 是否出现无语义的多主色并列。

### P1

- 标题和正文是否仍以 Deep Blue 为主。
- hero 区是否只有一个主强调色。
- Orange 是否只出现在受控风险提示中。
- takeaway strip 是否符合当前页面的语义色策略。
- 默认功能 icon / 业务 icon / 能力 icon 是否优先使用 Deep Blue，而不是随意 teal 化。
- 流程 / 连接 icon 是否只在对应语义中使用 Light Petrol。
- 风险 icon 是否只在风险语义中使用 Orange。

## Escalation Rules

- Prompt-Level `P0 fail`：禁止出图，必须先修正 prompt。
- Visual-Level `P0 fail`：不允许直接交付，必须触发 retry 或降级。
- `P1 fail`：优先触发 retry；如无法修复，可带偏差说明交付。
- `P2 fail`：允许交付，但必须记录在 `known_issues` 中。

## Degrade Rules

满足以下任一条件时进入降级交付：
- 第二次生成后仍存在 Visual `P0 fail`
- 中文长标题、复杂图表或高密度结构超出当前引擎稳定能力
- 页面核心逻辑成立，但视觉精度始终无法达标

降级交付物：
- 最佳近似图片
- 结构化 slide brief，至少包含：
  - `Action Title`
  - `reasoning_pattern`
  - `preferred_layout`
  - L1-L5 层级文本
  - `component_strategy`
  - 已知偏差说明

## 一票否决项

- 标题以 `分析`、`介绍`、`概况`、`说明` 收尾。
- 页面同时回答两个以上问题。
- 没有任何证据锚点。
- 没有 L2 hero evidence。
- 没有 L5 takeaway。
- footer 三分区缺项、跑位或被主体内容侵入。
- 页码与页脚文字带间距明显过大，或页脚文字带被排成页面中部居中文本，破坏 Advanta footer 关系。
- 浅色页中的 `SIEMENS` 品牌字标不是 Siemens Petrol 主色。
- 颜色超出品牌 token 和语义色范围，或出现无语义的多主色并列。
- 页面无法明确归属到一个 reasoning pattern。
- 画面像广告海报、startup landing page 或营销 infographic。
- 页面退化成纯文字说明页。
