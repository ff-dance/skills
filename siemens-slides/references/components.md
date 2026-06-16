# Siemens Components

面向 `siemens-slides` 的组件词典。它不是给模型直接读取本地 SVG 文件用的“素材库”，而是给 agent 提炼 prompt 时使用的“形状语义词典”。

使用原则：
- 先用 `references/layouts.md` 选页面结构，再用本词典补“局部构件语言”。
- 默认把这里的组件理解成 prompt 里的描述词，而不是直接拼贴本地资产。
- 优先使用来源明确、在 raw PPT 中反复出现的组件，而不是偶发装饰。
- 如果一个组件明显只是训练页示意形状，不要强行带进正式企业页面。

## 用法

- 需要页面边缘强调、章节指示、侧向标签时：优先看 `01_Basics` 和 `02_Boxes`
- 需要阶段推进、步骤连接、流程导向时：优先看 `03_Processes`
- 需要环形指标、图标容器、圆形节点时：优先看 `09_SiemensIcons`
- 需要行业/通用图标轮廓时：优先看 `sie-general-icons-*` 和 `sie-market-icons-*`
- 需要竞争者/NGO 这类 logo-like 轮廓时：只把它们当“轮廓密度参考”，不要直接把名字带进 prompt

## 按 Raw PPT 归类

### `01_Basics.pptx`

用途定位：
- 基础几何语言、页面局部强调、评分/指标小构件、连接线

主要组件家族：
- `homePlate`
  - 语义：细长楔形、竖向强调片、尖头标签
  - prompt 用语：`slender Siemens-petrol home-plate wedge`, `vertical tapered marker`, `narrow pointed side accent`
  - 示例：
    - [slide014_id1177603_homePlate_AutoShape_3.svg](../assets/reference-components/shape-assets/01_Basics/slide014_id1177603_homePlate_AutoShape_3.svg)
    - [slide015_id1179650_homePlate_AutoShape_2.svg](../assets/reference-components/shape-assets/01_Basics/slide015_id1179650_homePlate_AutoShape_2.svg)
- `custGeom`
  - 语义：自由曲线小构件、液位/胶囊/小型说明图形
  - prompt 用语：`small freeform technical glyph`, `capsule-like process marker`, `simple custom outline accent`
  - 示例：
    - [slide060_id40_custGeom_reservoir.svg](../assets/reference-components/shape-assets/01_Basics/slide060_id40_custGeom_reservoir.svg)
    - [slide060_id56_custGeom_foreground.svg](../assets/reference-components/shape-assets/01_Basics/slide060_id56_custGeom_foreground.svg)
- `connector` / `line`
  - 语义：关系连接、时间轴、分隔细线
  - prompt 用语：`thin straight connector`, `light technical divider`, `precise alignment line`
  - 示例：
    - [slide022_id21_connector_Gerade_Verbindung_55.svg](../assets/reference-components/shape-assets/01_Basics/slide022_id21_connector_Gerade_Verbindung_55.svg)
    - [slide048_id18_line_Line_24.svg](../assets/reference-components/shape-assets/01_Basics/slide048_id18_line_Line_24.svg)
- `arc + ellipse`
  - 语义：小型环状指标、刻度环、状态环
  - prompt 用语：`circular indicator ring`, `partial arc around a circle`, `minimal radial status marker`
  - 示例：
    - [slide069_id45_arc_arc.svg](../assets/reference-components/shape-assets/01_Basics/slide069_id45_arc_arc.svg)
    - [slide069_id46_ellipse_circle.svg](../assets/reference-components/shape-assets/01_Basics/slide069_id46_ellipse_circle.svg)

使用建议：
- `01_Basics` 最适合补“局部部件感”，不适合作为整页结构参考。
- `star5 / heart / diamond` 这类训练形状不建议进入正式 Siemens 咨询页，除非用户明确要图标化练习页。

### `02_Boxes.pptx` / `02_BoxesDark.pptx`

用途定位：
- 盒状说明块的尖角附件、流程导向箭头、端点标签

主要组件家族：
- `homePlate`
  - 语义：横向/纵向尖头标签、附着在 box 边缘的突出块
  - prompt 用语：`petrol home-plate tag attached to a box edge`, `sharp side pointer`, `small directional tab`
  - 示例：
    - [slide043_id17_homePlate_AutoShape_3.svg](../assets/reference-components/shape-assets/02_Boxes/slide043_id17_homePlate_AutoShape_3.svg)
    - [slide064_id17_homePlate_AutoShape_3.svg](../assets/reference-components/shape-assets/02_Boxes/slide064_id17_homePlate_AutoShape_3.svg)
- `flowChartExtract`
  - 语义：抽取式箭头、插入式方向构件、内外双层导向箭头
  - prompt 用语：`flowchart extract arrow`, `compact directional arrowhead`, `embedded process pointer`
  - 示例：
    - [slide026_id12_flowChartExtract_OuterArrow.svg](../assets/reference-components/shape-assets/02_Boxes/slide026_id12_flowChartExtract_OuterArrow.svg)
    - [slide026_id15_flowChartExtract_InnerArrow.svg](../assets/reference-components/shape-assets/02_Boxes/slide026_id15_flowChartExtract_InnerArrow.svg)
- `connector`
  - 语义：盒与盒之间的直线连接
  - prompt 用语：`strict straight connector`, `precise linking line between blocks`
  - 示例：
    - [slide067_id10_connector_Straight_Connector_9.svg](../assets/reference-components/shape-assets/02_Boxes/slide067_id10_connector_Straight_Connector_9.svg)

使用建议：
- 当页面主体是多个直角信息块时，这组组件最适合补“方向感”和“边缘强调”。
- 深色版 `02_BoxesDark` 主要影响颜色搭配，不改变组件语义。

### `03_Processes.pptx` / `03_ProcessesDark.pptx`

用途定位：
- 流程箭头、阶段过渡、链式推进、连续工艺感

主要组件家族：
- `custGeom`
  - 语义：大量自由路径流程件，适合抽象成阶段箭头、推进模块、连续路径碎片
  - prompt 用语：`custom freeform process arrow`, `segmented directional flow piece`, `technical progression marker`
  - 示例：
    - [slide010_id1180675_custGeom_Freeform_3.svg](../assets/reference-components/shape-assets/03_Processes/slide010_id1180675_custGeom_Freeform_3.svg)
    - [slide018_id1182779_custGeom_Freeform_59.svg](../assets/reference-components/shape-assets/03_Processes/slide018_id1182779_custGeom_Freeform_59.svg)
- `flowChartExtract`
  - 语义：流程中局部的箭头嘴、转向端头
  - prompt 用语：`small extract arrow in a process lane`, `lightweight process pointer`
- `ellipse`
  - 语义：流程节点、起止圆、阶段编号容器
  - prompt 用语：`small process node circle`, `minimal circular milestone`

使用建议：
- 这组更适合做“过程感”而不是孤立图标。
- 如果用户要路线图、步骤图、工艺链、成熟度路径，这组组件描述最有用。
- 深色版 `03_ProcessesDark` 可以作为深底流程页的局部构件语气参考。

### `05_Tables.pptx` / `05_TablesDark.pptx`

用途定位：
- 几乎没有独立 shape asset

结论：
- 这两组更像结构模板，不适合进入组件词典。
- 后续做表格页时应主要参考 `layouts.md` 的 `content-table-light`，不要从这里找局部图形。

### `06_Competitors.pptx` / `06_NGOs.pptx` / `06_Logos_alt.pptx`

用途定位：
- 轮廓型符号、logo-like 外形、组织或品牌图形的抽象包络

主要组件家族：
- `custGeom`
  - 语义：不规则轮廓、符号边界、徽记状外轮廓
  - prompt 用语：`irregular brand-like contour`, `organic symbol outline`, `abstract badge silhouette`

使用建议：
- 可参考它们的“轮廓复杂度”和“边界密度”，但不建议把具体 logo 形状写进通用 Siemens 页面 prompt。
- 更适合用户明确要“logo wall / ecosystem / partner landscape”时，作为局部视觉节奏参考。

### `09_SiemensIcons.pptx` / `09_SiemensIcons_negative.pptx`

用途定位：
- 图标容器、图标底座、环形承托、节点式说明图形

主要组件家族：
- `custGeom`
  - 语义：图标主轮廓、功能类符号、业务语义 glyph
  - prompt 用语：`simple Siemens-style line icon`, `compact technical glyph`, `functional outline icon`
- `ellipse`
  - 语义：图标圆底、节点背景、环形底座
  - prompt 用语：`icon circle container`, `clean round node background`, `circular badge base`
  - 示例：
    - [slide002_id5_ellipse_Oval_5.svg](../assets/reference-components/shape-assets/09_SiemensIcons/slide002_id5_ellipse_Oval_5.svg)
    - [slide041_id5_ellipse_Oval_5.svg](../assets/reference-components/shape-assets/09_SiemensIcons/slide041_id5_ellipse_Oval_5.svg)

使用建议：
- 当页面需要 3-6 个小型支持图形时，这组最适合作为“图标语气来源”。
- `negative` 版本主要提供深底使用时的反相思路，不改变组件家族本身。

### `sie-general-icons-*` / `sie-market-icons-*`

用途定位：
- 通用业务图标、行业图标

主要组件家族：
- `custGeom`
  - 语义：标准化线性图标或面状图标
  - prompt 用语：`clean Siemens business icon`, `simple market icon silhouette`, `compact corporate pictogram`

使用建议：
- 这些 deck 最适合“图标选择”，不适合推导页面结构。
- 带 `_text` 的 deck 已被我们过滤掉，不纳入形状组件词典。
- 如果页面只是需要少量配套图标，这组是最稳的参考来源。

## 组件到页面任务的映射

### 强调边缘 / 章节标识
- 首选来源：`01_Basics`, `02_Boxes`
- 推荐组件：`homePlate`

### 流程推进 / 方向引导
- 首选来源：`02_Boxes`, `03_Processes`
- 推荐组件：`flowChartExtract`, `connector`, `custGeom`

### 节点 / 指标 / 环形状态
- 首选来源：`01_Basics`, `09_SiemensIcons`
- 推荐组件：`ellipse`, `arc`

### 图标支撑
- 首选来源：`09_SiemensIcons`, `sie-general-icons-*`, `sie-market-icons-*`
- 推荐组件：`custGeom` 图标轮廓

### 生态 / 品牌墙 / 外部对象轮廓
- 首选来源：`06_Competitors`, `06_NGOs`, `06_Logos_alt`
- 推荐组件：`custGeom` 不规则轮廓

## 对 `siemens-slides` 的实际帮助

这份词典最适合帮助 agent 在 prompt 里说清楚：
- 需要什么局部形状语言
- 这些形状更像标签、箭头、节点、图标还是环形指标
- 应该从哪组 raw deck 借语气

它不用于：
- 直接把本地 SVG 路径喂给 image model
- 在最终 slide 中脚本拼贴这些 SVG
- 替代 `layouts.md` 的整页结构选择
