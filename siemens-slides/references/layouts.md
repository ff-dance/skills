# Siemens Layouts

Layout taxonomy 合并 Advanta 官方母版和 EE Team 结构页。它是唯一的 layout 来源。使用前先选最接近的页面类型，再打开对应主参考图观察结构与视觉重心。

所有 layout 默认都应保留底部品牌区：
- 左下页码 `Page X`
- 底部页脚
- 右下 `SIEMENS` 字标位

浅色页面默认使用白色背景 `#FFFFFF`。仅在用户明确需要更柔和底色时，才使用 `#F3F3F0` 作为浅色变体。

所有 layout 都必须满足以下对齐规则：
- 标题区、主体区、辅助区、底部品牌区共享同一套列网格
- 主要模块必须对齐到统一列边界和统一水平线
- 不允许出现因为没有贴齐栅格而形成的大面积无意义空白
- 如果页面一侧留白更大，必须能解释为图片区、说明区、品牌区或结构节奏，而不是“元素没铺满”

## 页面类型速查

| 页面类型 | Layout | 主参考图 |
|---|---|---|
| 封面 / 主标题 | `cover-title-dark` | `advanta/Slide1.png` |
| 带图封面 | `cover-title-picture` | `advanta/Slide29.png` |
| 章节页 | `chapter-divider` | `advanta/Slide7.png` |
| 目录 / 议程 | `agenda` | `ee-team/Slide60.png` |
| 深色内容页 | `content-basic-dark` | `advanta/Slide8.png` |
| 浅色内容页 | `content-basic-light` | `advanta/Slide17.png` |
| 图文 spotlight | `content-image-spotlight` | `advanta/Slide29.png` |
| 浅色表格 | `content-table-light` | `advanta/Slide24.png` |
| 三列流程 | `process-flow-light` | `advanta/Slide44.png` |
| Steps grid | `process-steps-grid` | `advanta/Slide45.png` |
| Roadmap | `roadmap-curved` | `advanta/Slide46.png` |
| 浅色引用 | `quote-light` | `ee-team/Slide75.png` |
| 深色引用 | `quote-dark` | `advanta/Slide8.png` |
| 浅色主张 | `statement-light` | `ee-team/Slide77.png` |
| 深色主张 | `statement-dark` | `advanta/Slide7.png` |
| 单对象焦点 | `single-object-focus` | `advanta/Slide17.png` |
| 全出血大图 | `single-large-image` | `advanta/Slide29.png` |
| 深色联系页 | `contact-dark` | `advanta/Slide53.png` |
| 浅色联系页 | `contact-light` | `advanta/Slide54.png` |
| 状态表 | `status-table` | `ee-team/Slide127.png` |
| 状态总览 | `status-overview` | `ee-team/Slide193.png` |
| 问题环 | `question-ring` | `ee-team/Slide133.png` |
| 金字塔 | `pyramid-priority` | `ee-team/Slide61.png` |
| 雷达 | `radar-arc` | `ee-team/Slide62.png` |
| 漏斗 | `funnel-columns` | `ee-team/Slide63.png` |
| House | `house-pillars` | `ee-team/Slide118.png` |
| 阶梯成长 | `staircase-growth` | `ee-team/Slide144.png` |
| 访谈总结 | `interview-summary` | `ee-team/Slide150.png` |
| 商业拆分 | `commercial-split` | `ee-team/Slide169.png` |
| Sit-Com-Sol | `three-card-scs` | `advanta/Slide16.png` |

## Advanta 基础页

### `cover-title-dark`
- 结构：深蓝背景，大标题从左侧安全区开始，副标题位于标题下方，底部品牌区留空
- 风格重点：强对比、极简、正式、企业级
- 建议：关键词用 `#E6E65F`；标题不要超过 2-3 行
- 避免：正文堆叠、居中海报感、多色装饰
- 栅格要求：标题区、副标题区和品牌区左边界一致，大留白必须来自标题区与品牌区之间的结构留白

### `cover-title-picture`
- 结构：照片主导，一侧深色信息区或遮罩，标题和副标题左对齐
- 风格重点：图片必须克制、企业化、工业化
- 建议：图片要像工业、咨询、技术或真实业务场景
- 避免：生活方式广告感、图片压住页脚/logo
- 栅格要求：图片区与文字区必须形成明确双区结构，不能让文字区漂在大面积图片空白中

### `chapter-divider`
- 结构：深蓝背景，极少文本，章节标题为视觉中心或左侧强标题
- 风格重点：比封面更干净、更结构化，强调段落切换
- 建议：只放章节名和短副标题

### `content-basic-dark`
- 结构：深蓝全底，标题在顶部，内容从约 20.7% 高度开始
- 风格重点：深色 presentation 感更强，适合摘要或重点结论
- 建议：用于摘要、关键发现、深色强调页

### `content-basic-light`
- 结构：白底、Deep Blue 标题、规整正文区
- 风格重点：阅读优先，信息层级清楚，不做卡片堆叠
- 建议：用于阅读优先的普通内容页
- 栅格要求：标题区和正文区共享统一左边界，正文内容块按列宽展开，不要只有左上有内容、右下大片空白

### `content-image-spotlight`
- 结构：大图区域 + 右侧或左侧文字区，常见比例接近 7.87" + 4.09"
- 风格重点：图片与说明有清晰主次，图片侧更宽，文字侧更窄
- 建议：正文不要过密，图片裁切留出信息呼吸感
- 栅格要求：图片区和文字区必须贴齐列边界，禁止两栏均未贴边导致中间或底部出现松散空白

### `content-table-light`
- 结构：白底表格，表头 Deep Blue 色阶，行列清楚
- 风格重点：清晰、规整、阅读优先，绝不做卡片化表格
- 建议：表格标题、表头、数据区层级清晰
- 栅格要求：表格宽度应与标题区或内容区主列宽对齐，不要做成中间一小块、四周大面积空白

### `process-flow-light`
- 结构：三列等宽流程，列宽接近 3.94"，列间距克制
- 风格重点：强调顺序或阶段关系，而不是复杂信息图
- 建议：适合 3 步流程、阶段说明、从左到右推进
- 栅格要求：三列必须等宽等距并落在统一水平线上，箭头和说明块也要对齐到列中心

### `process-steps-grid`
- 结构：横向步骤条或矩阵式步骤块，带箭头/三角方向
- 风格重点：适合阶段推进、步骤说明、简洁里程碑
- 建议：4 或 5 个阶段最稳定
- 栅格要求：步骤块宽度、间距、基线一致，不允许某一步单独偏移造成空白断裂

### `roadmap-curved`
- 结构：曲线路径、里程碑节点、短说明
- 风格重点：路径感清楚，节点不宜过多，整体保持克制
- 建议：节点不宜过多，保持底部品牌区清爽
- 栅格要求：虽然路径可弯曲，但节点说明框仍需吸附到隐含列网格，不要东一块西一块漂浮

### `single-object-focus`
- 结构：标题 + 全宽单一对象或核心图示 + 可选高亮框
- 风格重点：单一焦点最重要，页面只服务一个对象或主题
- 建议：用于一个模型、一张图、一组大数字或核心判断
- 栅格要求：主体对象与高亮框必须和标题区共用对齐轴，不能只把对象缩成页面中央小块留下四周空白

### `single-large-image`
- 结构：图片全出血，标题叠加或靠近图上安全区，底部品牌区留空
- 风格重点：像 presentation slide，不像广告海报
- 建议：图片上叠加文字时使用深色遮罩保证可读
- 栅格要求：标题与说明区必须贴齐安全区边界，不能悬浮在图中央导致大片无结构空白

### `quote-light` / `quote-dark`
- 结构：一句引言 + 作者/来源；light 为白底，dark 为 Deep Blue 底
- 风格重点：安静、干净、可信，重点在一句话本身
- 建议：可居中，文字必须短

### `statement-light` / `statement-dark`
- 结构：一句强主张占据主视觉；light 为白底，dark 为 Deep Blue 底
- 风格重点：比 quote 更强、更直接，但仍保持企业语气和理性
- 建议：只强调少量关键词

### `contact-dark` / `contact-light`
- 结构：标题 + 联系人信息块 + 底部品牌区留空
- 风格重点：整洁、可信、像标准 corporate ending slide
- 建议：信息左对齐，联系方式层级清楚
- 栅格要求：信息块应按统一列宽和统一行距排布，不要在页面中部孤立放置一小块联系信息

## EE Team 结构页

### `status-table`
- 结构：深色框架页，清晰行列，状态灯或行动列
- 建议：优先把状态、行动和责任拆成清楚行列，不要做成卡片墙

### `status-overview`
- 结构：行级状态块、关键方面区、状态色点
- 建议：适合总览，不适合堆很多细节文本

### `question-ring`
- 结构：中心问题 + 环状外圈 + 左右问题条
- 建议：中心问题必须足够短，外围问题数控制在可读范围内

### `pyramid-priority`
- 结构：塔形或 1-2-3 层级结构
- 建议：适合优先级或成熟度分层，不要塞长段说明

### `radar-arc`
- 结构：半圆扇区 + 中心品牌元素
- 建议：适合维度分布和能力地图，不适合长表格式信息

### `funnel-columns`
- 结构：漏斗或阶段收缩逻辑
- 建议：突出阶段收敛关系，不要做成营销漏斗海报

### `house-pillars`
- 结构：屋顶 + 多支柱 + 底座
- 建议：适合框架型解决方案、能力架构或治理模型

### `staircase-growth`
- 结构：台阶、阶段卡、前进式增长
- 建议：适合成长路线、成熟度路径、阶段提升说明

### `interview-summary`
- 结构：人物侧栏 + 主题条 + insight 列
- 建议：人物信息做辅助，核心洞察才是主内容

### `commercial-split`
- 结构：左侧条目 + 右侧总结框或大数值
- 建议：适合商业拆分、价值归纳、左右对照

### `three-card-scs`
- 结构：Situation / Complication / Solution 三个直角信息块或三列
- 建议：每块控制在一个标题加少量要点，保持节奏清楚

## 选择规则

- 如果用户明确指定页型，优先服从页型。
- 如果用户没有指定页型，根据内容结构自动选：
  - 1 个主标题 + 副标题：`cover-title-dark`；需要照片氛围时改用 `cover-title-picture`
  - 章节切换：`chapter-divider`
  - 目录 / 章节清单：`agenda`
  - 1 个核心主题：`single-object-focus` 或 `content-basic-light`
  - 图文组合 / 图解说明：`content-image-spotlight`
  - 3 个步骤 / 3 个模块：`process-flow-light`
  - 一张大图主导：`single-large-image`
  - 一句话引用：`quote-light` 或 `quote-dark`
  - 一句强主张：`statement-light` 或 `statement-dark`
  - 联系方式 / 发布信息：`contact-dark` 或 `contact-light`
- 当两个 layout 都能适配时，优先选择信息结构更清楚的那个，而不是视觉更花的那个。
