# Siemens Components

面向 `siemens-slides` 的组件语义词典，用来帮助 agent 组织局部构件语言。

使用原则：
- 先用 `references/layouts.md` 确定整页结构方向，再用本词典补“局部构件语言”；必要时允许在相邻 layout 之间做 hybrid 组合。
- 默认把这里的组件理解成 prompt 里的抽象描述词。
- 优先用能表达逻辑关系的组件语义，不要为了装饰而堆组件。

## 怎么用

- 页面需要强调、标签、章节标识时：优先选 `homePlate` 一类的“边缘强调语义”。
- 页面需要推进、阶段、路线、流程时：优先选 `flow arrow`、`process piece`、`connector`。
- 页面需要节点、里程碑、状态点时：优先选 `ellipse node`、`arc ring`。
- 页面需要少量支撑图标时：优先选 `technical glyph icon`。
- 页面需要生态对象或外部实体边界时：优先选 `irregular contour`，但只作为抽象轮廓语义。

## 核心组件语义

### `homePlate`
- 语义：细长楔形、竖向强调片、侧向标签、附着在 box 边缘的尖头小附件
- 适合：章节标识、边缘强调、关键内容标记
- prompt 用语：
  - `slender Siemens-petrol side accent`
  - `narrow pointed label attachment`
  - `sharp edge marker attached to a content block`

### `flow arrow`
- 语义：方向推进、步骤迁移、阶段切换、下一步引导
- 适合：路线图、步骤图、流程页、实施节奏页
- prompt 用语：
  - `compact directional arrows between steps`
  - `clean process pointers guiding the reading flow`
  - `restrained forward arrows for stage transitions`

### `process piece`
- 语义：连续流程件、分段推进模块、技术路径碎片、阶段拼接块
- 适合：端到端流程、工艺链、能力建设路径、成熟度路径
- prompt 用语：
  - `segmented process modules with clean geometry`
  - `linked directional process pieces`
  - `technical progression blocks with restrained outlines`

### `thin connector`
- 语义：严谨连接、因果关系、模块对齐、阅读路径控制
- 适合：关系图、架构图、流程连接、结构分解
- prompt 用语：
  - `thin straight technical connectors`
  - `precise linking lines between modules`
  - `lightweight relationship lines with strict alignment`

### `ellipse node`
- 语义：节点、里程碑、编号底座、图标圆底、指标点
- 适合：步骤编号、状态节点、能力点、流程起止点
- prompt 用语：
  - `small circular milestone nodes`
  - `minimal round status markers`
  - `clean ellipse containers for icons or numbers`

### `arc ring`
- 语义：环形指标、局部刻度、半环状态、状态承托
- 适合：状态总览、成熟度点、能力环、雷达式局部结构
- prompt 用语：
  - `thin circular status arcs`
  - `partial rings around key nodes`
  - `minimal radial indicator rings`

### `technical glyph icon`
- 语义：简洁业务图标、技术功能 pictogram、支持性小图形
- 适合：状态页、三卡片页、能力页、总结页的小型视觉支撑
- prompt 用语：
  - `simple Siemens-style technical glyph icons`
  - `clean business pictograms with restrained line work`
  - `compact functional outline icons`

### `irregular contour`
- 语义：生态实体边界、抽象外部对象轮廓、logo-like 包络
- 适合：生态图谱、伙伴版图、外部对象对比
- prompt 用语：
  - `abstract irregular contours for ecosystem entities`
  - `organic badge-like silhouettes used sparingly`
  - `brand-like outline shapes without explicit logos`

## 逻辑关系到组件的映射

### 讲“为什么”
- 优先：`thin connector` + 因果箭头语义
- 用法：把问题、原因、影响、方案串成有方向的推理链

### 讲“怎么走”
- 优先：`flow arrow` + `ellipse node` + `process piece`
- 用法：表达阶段推进、实施顺序、路径切换

### 讲“系统如何协同”
- 优先：`thin connector` + 双向连接语义 + `ellipse node`
- 用法：表达模块互动、系统接口、数据来回流动

### 讲“当前状态如何被看见”
- 优先：`arc ring` + `ellipse node` + `technical glyph icon`
- 用法：表达状态总览、成熟度、能力面板

### 讲“谁和谁构成生态”
- 优先：`irregular contour` + `thin connector`
- 用法：表达生态对象边界与外部关系网络

## 对常见页面任务的建议

### 强调边缘 / 章节标识
- 推荐：`homePlate`

### 流程推进 / 方向引导
- 推荐：`flow arrow` + `thin connector` + `process piece`

### 节点 / 指标 / 环形状态
- 推荐：`ellipse node` + `arc ring`

### 图标支撑
- 推荐：`technical glyph icon`

### 生态 / 品牌墙 / 外部对象轮廓
- 推荐：`irregular contour`

## 约束

- 不要把任何本地 SVG 路径或文件名写进 prompt。
- 不要根据单个轮廓细节做一比一复刻。
- 不要在一个页面里同时堆太多组件家族。
- 不要把组件做成海报化大装饰。
- 不要为了所谓“稳”而把所有内容区都做成同构文字盒子。
- 不要给正文说明区、注释区、信息说明框默认加虚线边框。
- 不要把底部重点内容区做成多色拼接卡片带；优先单一主色整条表达。
- `star5 / heart / diamond` 这类练习形状不应进入正式 Siemens 咨询页。

## 一句话规则

如果拿不准，优先用：
- `homePlate` 做强调
- `flow arrow` 做方向
- `ellipse node + arc ring` 做节点
- `technical glyph icon` 做小型支撑图形

前提是：它们只作为语义提示。
