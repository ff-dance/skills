# Siemens Components Cheat Sheet

给 `siemens-slides` 写 prompt 时，优先把组件当作“局部形状语言”来描述，而不是当作要拼贴的素材。

使用顺序：
1. 用 `references/layouts.md` 定整页结构
2. 用本页补局部构件
3. 需要更细来源解释时，再回 `references/components.md`

## 最高频组件

### 1. `homePlate`
- 适合：章节标识、边缘强调、侧向标签、盒子尖角附件
- 典型语句：
  - `a slender Siemens-petrol home-plate wedge as a side accent`
  - `small pointed home-plate tags attached to box edges`
  - `narrow tapered vertical markers for emphasis`
- 常见搭配：
  - `content-basic-light`
  - `process-flow-light`
  - `statement-light`

### 2. `flowChartExtract`
- 适合：流程箭头、步骤导向、阶段切换
- 典型语句：
  - `compact flowchart extract arrows between steps`
  - `embedded directional arrowheads inside process blocks`
  - `small sharp process pointers with clean geometry`
- 常见搭配：
  - `process-flow-light`
  - `process-steps-grid`
  - `roadmap-curved`

### 3. `custGeom process piece`
- 适合：复杂流程件、连续路径碎片、技术路线块
- 典型语句：
  - `custom freeform process arrows with segmented geometry`
  - `technical progression pieces with clean custom outlines`
  - `linked freeform directional modules, restrained and corporate`
- 常见搭配：
  - `process-flow-light`
  - `roadmap-curved`
  - `staircase-growth`

### 4. `ellipse node`
- 适合：节点、步骤编号底座、图标圆底、指标点
- 典型语句：
  - `small circular milestone nodes`
  - `clean ellipse icon containers`
  - `minimal round status markers`
- 常见搭配：
  - `process-flow-light`
  - `radar-arc`
  - `question-ring`

### 5. `arc ring`
- 适合：局部环形指标、半环状态、刻度环
- 典型语句：
  - `partial Siemens-petrol arcs around circular nodes`
  - `minimal radial indicator rings`
  - `thin circular status arcs with precise alignment`
- 常见搭配：
  - `radar-arc`
  - `status-overview`
  - `question-ring`

### 6. `thin connector`
- 适合：关系线、因果连接、步骤之间的严谨连线
- 典型语句：
  - `thin straight technical connectors`
  - `precise linking lines between modules`
  - `lightweight alignment dividers and relationship lines`
- 常见搭配：
  - `process-steps-grid`
  - `house-pillars`
  - `commercial-split`

### 7. `technical glyph icon`
- 适合：功能图标、业务图标、能力图标
- 典型语句：
  - `simple Siemens-style technical glyph icons`
  - `clean business pictograms with restrained line work`
  - `compact functional outline icons`
- 常见搭配：
  - `single-object-focus`
  - `status-overview`
  - `three-card-scs`

### 8. `irregular contour`
- 适合：生态轮廓、外部对象轮廓、logo-like 抽象边界
- 典型语句：
  - `abstract irregular contours for ecosystem entities`
  - `organic badge-like silhouettes used sparingly`
  - `brand-like outline shapes without explicit logos`
- 常见搭配：
  - `commercial-split`
  - `interview-summary`
  - `status-overview`

## 直接可用 Prompt 模板

### 强调标签型
`Use a clean white corporate slide with a few slender Siemens-petrol home-plate wedges as side accents, attached to key content blocks, all aligned to a strict grid.`

### 流程推进型
`Build a restrained process slide using segmented custom freeform process pieces, compact flowchart extract arrows, and thin technical connectors, with consistent spacing, no decorative clutter, and no dashed borders around text content boxes.`

### 环形节点型
`Use small circular milestone nodes with thin Siemens-petrol arc rings and minimal connector lines to create a precise status or capability overview.`

### 图标支撑型
`Add 3 to 5 compact Siemens-style technical glyph icons inside clean ellipse containers to support the main content without turning the page into an infographic poster.`

### 底部重点总结型
`Use one single full-width takeaway strip in one dominant brand color, preferably Deep Blue or Siemens Petrol, instead of multiple colored cards or segmented KPI tiles.`

## 推荐组合

### 标题页局部强化
- `homePlate + thin connector`

### 流程页
- `custGeom process piece + flowChartExtract + ellipse node`

### 状态总览页
- `ellipse node + arc ring + technical glyph icon`

### 框架页 / 结构页
- `homePlate + thin connector + technical glyph icon`

## 不推荐组合

- 不要把 `star5 / heart / diamond` 当成正式 Siemens 咨询页组件
- 不要把这批组件写成海报化的大装饰
- 不要在一个页面里同时塞太多组件家族
- 不要给正文说明区、注释区、信息说明框默认加虚线边框
- 不要把底部重点内容区做成多个颜色并排的小卡片
- 不要把本地 SVG 路径直接写进 imagegen prompt

## 一句话规则

如果拿不准，优先用：
- `homePlate` 做强调
- `flowChartExtract` 做方向
- `ellipse + arc` 做节点
- `technical glyph icon` 做小型支撑图形

补充约束：
- 编号 badge 默认使用正方形或直角矩形
- 内容 text 区域优先无边框，必要时只用细实线
- 底部重点条优先单一主色整条表达，不用多色分段
