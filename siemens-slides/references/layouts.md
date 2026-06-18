# Siemens Layouts

Layout taxonomy 合并 Advanta 官方母版和 EE Team 结构页。它是一个 layout 参考语汇库，不是唯一答案，也不是固定模板目录。内容页应先判断这页在回答什么问题，再选择论证模式，最后把模式映射到最合适的 layout；必要时允许在品牌边界内做 hybrid 组合。

所有 layout 默认都应保留底部品牌区：
- 左下页码 `Page X`
- 底部页脚
- 右下 `SIEMENS` 字标位

所有 layout 默认也应保留固定 footer band：
- footer band 从约 `y = 92%` slide height 开始到底边
- takeaway strip、正文、主图形不得侵入 footer band
- 普通内容页默认使用 Advanta 内容页 footer family：
  - 页码区约 `x=411162 / y=6310800 / width=648000 / height=547200 EMU`
  - 页码区约 `x=3.37% / y=92.02% / width=5.31%`
  - 页脚区约 `x=1059160 / y=6310800 / width=8640003 / height=547200 EMU`
  - 页脚区约 `x=8.69% / y=92.02% / width=70.87%`
  - 品牌区约 `x=10635188 / y=6418800 / width=1152000 / height=183168 EMU`
  - 品牌区约 `x=87.23% / y=93.60% / width=9.45% / right_edge=96.68%`
- 页脚区是左锚定文字带，不是底部居中文案区；footer text 必须从页码右侧几乎直接开始。
- 页码区右边界与页脚区左边界在母版里几乎重合，应按无缝衔接处理。

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

## 论证模式到 Layout 的映射

| 论证模式 | 推荐 Layout | 备注 |
|---|---|---|
| `① Sit-Com-Sol` | `three-card-scs`, `process-flow-light` | 首选三栏递进 |
| `③ 成熟度评估` | `status-overview`, `radar-arc` | 适合状态分层与能力差距 |
| `⑤ 结构化总览` | `content-basic-light`, `commercial-split`, `house-pillars` | 按关键维度并列或分层 |
| `⑥ 对比分析` | `commercial-split`, `content-table-light` | 适合左右对照和推荐方案 |
| `⑧ 数据驱动洞察` | `single-object-focus`, `content-basic-light` | 让 hero evidence 成为主角 |
| `⑩ 愿景 vs 现状 + 差距` | `commercial-split`, `staircase-growth` | 适合现状到目标的桥接 |
| `⑪ 技术架构蓝图` | `house-pillars`, `content-basic-light` | 适合分层结构，不适合堆太多系统框 |
| `⑭ 战略路线图` | `roadmap-curved`, `staircase-growth` | 路线感优先 |
| `⑯ 组织与治理` | `house-pillars`, `status-table` | 用层级或 RACI 结构承载 |
| `⑰ 端到端数据流` | `process-flow-light`, `process-steps-grid` | 强调流向和节点关系 |
| `⑱ 业务流程泳道图` | `process-steps-grid`, `process-flow-light` | 当前 skill 里用轻量泳道表达 |
| `⑲ 能力建设路径` | `staircase-growth`, `house-pillars` | 从当前到目标的建设节奏 |
| `㉑ 标杆对比` | `content-table-light`, `commercial-split` | 适合表格和差距总结 |
| `㉓ 速赢清单` | `commercial-split`, `content-basic-light` | 适合行动清单和优先项 |

## 每个 Layout 最擅长表达的逻辑关系

- `three-card-scs`：最适合递进式三段论，不适合堆积平行事实。
- `commercial-split`：最适合对比、归纳、现状 vs 目标，不适合同时塞 3 种逻辑。
- `content-table-light`：最适合标准化对比与标杆评估，不适合海报式大数字页。
- `single-object-focus`：最适合单一证据主导，不适合多线程论证。
- `roadmap-curved`：最适合阶段推进，不适合细粒度项目甘特。
- `process-flow-light`：最适合线性流转，不适合复杂矩阵关系。
- `process-steps-grid`：最适合步骤与轻量泳道，不适合复杂架构图。
- `status-overview`：最适合成熟度总览和状态盘点，不适合长篇细节说明。
- `house-pillars`：最适合分层架构与治理框架，不适合纯数据比较。
- `staircase-growth`：最适合能力成长路径，不适合一次性静态对照。

## Advanta 基础页

### `cover-title-dark`
- 结构：深蓝背景，大标题从左侧安全区开始，副标题位于标题下方，底部品牌区留空
- 风格重点：强对比、极简、正式、企业级
- 建议：关键词用 `#E6E65F`；标题不要超过 2-3 行
- 避免：正文堆叠、居中海报感、多色装饰
- 栅格要求：标题区、副标题区和品牌区左边界一致，大留白必须来自标题区与品牌区之间的结构留白
- 擅长逻辑：封面、主标题、章节切换
- 易错点：把它做成营销海报或堆满正文

### `cover-title-picture`
- 结构：照片主导，一侧深色信息区或遮罩，标题和副标题左对齐
- 风格重点：图片必须克制、企业化、工业化
- 建议：图片要像工业、咨询、技术或真实业务场景
- 避免：生活方式广告感、图片压住页脚/logo
- 栅格要求：图片区与文字区必须形成明确双区结构，不能让文字区漂在大面积图片空白中
- 擅长逻辑：带场景氛围的封面或引导页
- 易错点：图片主导过强，内容像广告封面

### `chapter-divider`
- 结构：深蓝背景，极少文本，章节标题为视觉中心或左侧强标题
- 风格重点：比封面更干净、更结构化，强调段落切换
- 建议：只放章节名和短副标题
- 擅长逻辑：章节切换、故事节奏停顿
- 易错点：把它当普通内容页使用

### `content-basic-dark`
- 结构：深蓝全底，标题在顶部，内容从约 20.7% 高度开始
- 风格重点：深色 presentation 感更强，适合摘要或重点结论
- 建议：用于摘要、关键发现、深色强调页
- 擅长逻辑：重点结论、管理层摘要、statement-like 内容
- 易错点：正文过多导致阅读负担重

### `content-basic-light`
- 结构：白底、Deep Blue 标题、规整正文区
- 风格重点：阅读优先，信息层级清楚，不做卡片堆叠
- 建议：用于阅读优先的普通内容页
- 栅格要求：标题区和正文区共享统一左边界，正文内容块按列宽展开，不要只有左上有内容、右下大片空白
- 擅长逻辑：结构化总览、结论页、轻量数据洞察
- 易错点：没有 hero evidence，只剩普通文档排版

### `content-image-spotlight`
- 结构：大图区域 + 右侧或左侧文字区，常见比例接近 7.87" + 4.09"
- 风格重点：图片与说明有清晰主次，图片侧更宽，文字侧更窄
- 建议：正文不要过密，图片裁切留出信息呼吸感
- 栅格要求：图片区和文字区必须贴齐列边界，禁止两栏均未贴边导致中间或底部出现松散空白
- 擅长逻辑：图文证据、场景展示、before/after
- 易错点：文字区信息过多，图片退化成装饰

### `content-table-light`
- 结构：白底表格，表头 Deep Blue 色阶，行列清楚
- 风格重点：清晰、规整、阅读优先，绝不做卡片化表格
- 建议：表格标题、表头、数据区层级清晰
- 栅格要求：表格宽度应与标题区或内容区主列宽对齐，不要做成中间一小块、四周大面积空白
- 擅长逻辑：对比分析、标杆对比、评估表
- 易错点：做成表格堆字而没有推荐结论

### `process-flow-light`
- 结构：三列等宽流程，列宽接近 3.94"，列间距克制
- 风格重点：强调顺序或阶段关系，而不是复杂信息图
- 建议：适合 3 步流程、阶段说明、从左到右推进
- 栅格要求：三列必须等宽等距并落在统一水平线上，箭头和说明块也要对齐到列中心
- 擅长逻辑：线性流程、数据流、三段递进
- 易错点：硬塞过多节点导致失去顺序清晰度

### `process-steps-grid`
- 结构：横向步骤条或矩阵式步骤块，带箭头/三角方向
- 风格重点：适合阶段推进、步骤说明、简洁里程碑
- 建议：4 或 5 个阶段最稳定
- 栅格要求：步骤块宽度、间距、基线一致，不允许某一步单独偏移造成空白断裂
- 擅长逻辑：阶段推进、轻量泳道、标准步骤
- 易错点：把它当复杂系统架构图来用

### `roadmap-curved`
- 结构：曲线路径、里程碑节点、短说明
- 风格重点：路径感清楚，节点不宜过多，整体保持克制
- 建议：节点不宜过多，保持底部品牌区清爽
- 栅格要求：虽然路径可弯曲，但节点说明框仍需吸附到隐含列网格，不要东一块西一块漂浮
- 擅长逻辑：路线图、阶段性演进、里程碑规划
- 易错点：节点过多，变成复杂甘特

### `single-object-focus`
- 结构：标题 + 全宽单一对象或核心图示 + 可选高亮框
- 风格重点：单一焦点最重要，页面只服务一个对象或主题
- 建议：用于一个模型、一张图、一组大数字或核心判断
- 栅格要求：主体对象与高亮框必须和标题区共用对齐轴，不能只把对象缩成页面中央小块留下四周空白
- 擅长逻辑：数据驱动洞察、hero number、单一证据
- 易错点：把多个并列结论塞进同一页面

### `single-large-image`
- 结构：图片全出血，标题叠加或靠近图上安全区，底部品牌区留空
- 风格重点：像 presentation slide，不像广告海报
- 建议：图片上叠加文字时使用深色遮罩保证可读
- 栅格要求：标题与说明区必须贴齐安全区边界，不能悬浮在图中央导致大片无结构空白
- 擅长逻辑：场景引导、现场感、封面过渡
- 易错点：做成广告式视觉页

### `quote-light` / `quote-dark`
- 结构：一句引言 + 作者/来源；light 为白底，dark 为 Deep Blue 底
- 风格重点：安静、干净、可信，重点在一句话本身
- 建议：可居中，文字必须短
- 擅长逻辑：引用、观点引导、态度声明
- 易错点：引用过长，变成大段正文

### `statement-light` / `statement-dark`
- 结构：一句强主张占据主视觉；light 为白底，dark 为 Deep Blue 底
- 风格重点：比 quote 更强、更直接，但仍保持企业语气和理性
- 建议：只强调少量关键词
- 擅长逻辑：主张页、总括页、章节结论
- 易错点：做成海报式 slogan

### `contact-dark` / `contact-light`
- 结构：标题 + 联系人信息块 + 底部品牌区留空
- 风格重点：整洁、可信、像标准 corporate ending slide
- 建议：信息左对齐，联系方式层级清楚
- 栅格要求：信息块应按统一列宽和统一行距排布，不要在页面中部孤立放置一小块联系信息
- 擅长逻辑：结束页、联系人页、发布页
- 易错点：把它误用为普通内容页

## EE Team 结构页

### `status-table`
- 结构：深色框架页，清晰行列，状态灯或行动列
- 建议：优先把状态、行动和责任拆成清楚行列，不要做成卡片墙
- 擅长逻辑：状态盘点、责任分配、治理视图
- 易错点：信息太密，缺少主判断

### `status-overview`
- 结构：行级状态块、关键方面区、状态色点
- 建议：适合总览，不适合堆很多细节文本
- 擅长逻辑：成熟度总览、状态快照、差距概览
- 易错点：没有清晰的层级，像状态墙

### `question-ring`
- 结构：中心问题 + 环状外圈 + 左右问题条
- 建议：中心问题必须足够短，外围问题数控制在可读范围内
- 擅长逻辑：问题框定、诊断起点、议题拆分
- 易错点：外围问题过多，页面转不动

### `pyramid-priority`
- 结构：塔形或 1-2-3 层级结构
- 建议：适合优先级或成熟度分层，不要塞长段说明
- 擅长逻辑：优先级、层级、成熟度分层
- 易错点：每层文本太长，失去塔形表达力

### `radar-arc`
- 结构：半圆扇区 + 中心品牌元素
- 建议：适合维度分布和能力地图，不适合长表格式信息
- 擅长逻辑：成熟度评估、能力分布
- 易错点：维度过多，视觉噪音很高

### `funnel-columns`
- 结构：漏斗或阶段收缩逻辑
- 建议：突出阶段收敛关系，不要做成营销漏斗海报
- 擅长逻辑：收敛、筛选、漏斗式决策
- 易错点：强营销感，偏离 corporate 语气

### `house-pillars`
- 结构：屋顶 + 多支柱 + 底座
- 建议：适合框架型解决方案、能力架构或治理模型
- 擅长逻辑：架构蓝图、治理框架、能力分层
- 易错点：支柱太多，读不出主次

### `staircase-growth`
- 结构：台阶、阶段卡、前进式增长
- 建议：适合成长路线、成熟度路径、阶段提升说明
- 擅长逻辑：能力建设路径、愿景差距、阶段提升
- 易错点：同时表达太多并列维度

### `interview-summary`
- 结构：人物侧栏 + 主题条 + insight 列
- 建议：人物信息做辅助，核心洞察才是主内容
- 擅长逻辑：访谈洞察、声音摘录、研究总结
- 易错点：人物信息喧宾夺主

### `commercial-split`
- 结构：左侧条目 + 右侧总结框或大数值
- 建议：适合商业拆分、价值归纳、左右对照
- 擅长逻辑：对比分析、现状 vs 目标、速赢清单、推荐结论
- 易错点：左右两侧没有明确主次或推荐方向

### `three-card-scs`
- 结构：Situation / Complication / Solution 三个直角信息块或三列
- 建议：每块控制在一个标题加少量要点，保持节奏清楚
- 擅长逻辑：Sit-Com-Sol、三段递进、因果收束
- 易错点：每栏塞过多要点，失去节奏

## 选择规则

- 如果用户明确指定页型，优先服从页型。
- 如果用户没有指定页型，优先按论证模式选，再按以下内容结构映射：
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
- 当两个 layout 都能适配时，优先选择更能表达论证关系的那个，而不是视觉更花的那个。
- 当现成 layout 都不够贴合时，可以在统一网格、footer band 和品牌用色不被破坏的前提下，混合相邻 layout 的优点生成新的结构化变体。
