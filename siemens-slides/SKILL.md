---
name: siemens-slides
description: Generate Siemens-style slides, ppt images, and presentation slide images as raster output. Use this skill when the user asks for 西门子风格的 slides / ppt / ppt 图片 / presentation slides / slide images, especially Siemens Advanta-style corporate pages such as covers, image spotlight pages, agendas, tables, process flows, roadmaps, radar pages, funnel pages, house pages, status overviews, interview summaries, quote/statement pages, and contact pages.
---

# Siemens Slides

生成西门子 / Siemens Advanta 风格的 slide 图片。这个 skill 只保留两层规范：
- `references/style-guide.md`：system-level style
- `references/layouts.md`：layout

## 何时使用

使用本 skill：
- 用户要求生成“西门子风格的 slides / ppt / ppt 图片”
- 用户要求生成 “Siemens-style presentation slides / slide images”
- 用户要企业汇报页、方案页、咨询框架页、结构化图文页、联系页等 raster slide image

不要使用本 skill：
- 用户要可编辑 `.pptx` 文件
- 用户要普通海报、网页 UI、插画或非演示文稿图片
- 用户要直接编辑 SVG / HTML / PPT 原生资产

## 使用顺序

1. 先读 `references/style-guide.md`，锁定品牌气质、色板、字体观感、组件规则和禁忌项。
2. 再读 `references/layouts.md`，选择最接近页面类型的 layout 和主参考图。
3. 如果用户任务明显依赖局部构件语言、箭头、节点、图标、标签或流程件，先读 `references/components-cheatsheet.md`，需要更细来源解释时再读 `references/components.md`。
4. 打开主参考 slide，自行观察并提炼版式特征；不要把本地路径当作模型可见输入。
5. 必须使用 `$imagegen` 直接生成最终图片，prompt 中优先写清楚：
   - 页面类型与 layout
   - 大框架布局
   - 栅格系统与对齐关系
   - 官方色板
   - 字体观感
   - Siemens Advanta 企业咨询风格
   - 直角矩形和禁忌项

## 快速工作流

1. 先判断用户要的是哪类页面：封面、章节页、目录页、普通内容页、图文页、流程页、表格页、结构框架页、引言页、主张页还是联系页。
2. 到 `references/layouts.md` 中选择最接近的 layout；如果拿不准，优先选择信息结构更清楚的 layout，而不是更花的 layout。
3. 从主参考图中提炼 3 件事写进 prompt：
   - 标题区位置
   - 主体区结构
   - 栅格对齐与底部品牌区关系
4. 如果用户要直接出图，不要只停留在给 prompt；继续调用 `$imagegen` 完成图片生成。
5. 出图后优先检查：
   - 是否仍像 corporate presentation page，而不是海报
   - 大框架布局是否稳定
   - 主要元素是否对齐到同一栅格体系
   - 底部品牌区是否完整、清楚、没有被主体内容压住

## 核心硬规则

- 产物是图片格式 slide。
- 最终 slide 图片必须由 `$imagegen` 生成；不要使用 Python、PIL/Pillow、matplotlib、Plotly、SVG/HTML/canvas 截图或脚本绘图来生成最终图片。
- Python 只能用于文件整理、尺寸检查、元数据读取或非图像生成的辅助验证；不能作为 slide 渲染/绘图引擎。
- 即使需要参考本地品牌资产或参考 slide，也应由 agent 观察后把版式、色彩、文字和构图要求写入 `$imagegen` prompt，而不是用脚本拼贴或复刻图片。
- 默认输出 `16:9`、`4K`，目标 `3840x2160`。
- 浅色页默认白底 `#FFFFFF`，浅色页正文默认 `#000028`。
- 官方主色：Deep Blue `#000028`、Siemens Petrol `#009999`、Light Petrol `#00C1B6`、Advanta Green `#E6E65F`、White `#FFFFFF`。
- 字体观感：中文接近 `PingFang SC`，英文和数字接近 `Arial`。
- Box、card、信息块、表格块必须使用直角矩形，不使用圆角。
- 编号 badge 默认使用正方形或直角矩形，不使用 trapezoid、wedge 或 home-plate。
- 内容 text 区域、说明框、注释框默认不用虚线边框；优先无边框，必要时只用极细实线。
- 底部重点内容区、总结条、takeaway strip 默认使用单一主色背景，不做多色并排卡片。
- 不允许出现无依据的大面积空白；留白必须服务于栅格、层级和阅读节奏。
- 本地文件路径只是 agent 的检索线索，不是 `$imagegen` 能直接“看见”的参考图输入。
- 默认中文优先，除非用户明确要求英文。
- 底部品牌区应保持干净，避免重要文字或主体图形压到底边。
- 视觉目标始终是 Siemens corporate presentation page，不是 poster，不是 startup landing page，不是 marketing hero banner。

## 资源导航

- 风格与色板：`references/style-guide.md`
- 布局说明与选型建议：`references/layouts.md`
- 组件速查表：`references/components-cheatsheet.md`
- 组件词典与 raw PPT 归类：`references/components.md`
- 正式组件参考资产：`assets/reference-components/shape-assets/`
- 品牌与示例图资产：`assets/branding/`、`assets/reference-slides/`
