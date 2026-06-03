# Siemens Advanta Style Guide

## 核心气质

- Deep Blue、克制、咨询级、品牌驱动、数据导向、现代企业、Teal/Petrol 点缀
- 页面应像 Siemens 企业咨询/战略汇报页，不像海报、广告、网页 hero 或 startup pitch
- 装饰度极低，强调网格、留白、层级、数据和结构

## 关键词

`corporate` `enterprise` `clean` `minimalist` `industrial` `technology` `professional` `German-design` `Swiss-grid` `widescreen` `left-aligned`

## 官方色板

- Deep Blue: `#000028`
- White: `#FFFFFF`
- Siemens Petrol: `#009999`
- Light Petrol: `#00C1B6`
- Advanta Green: `#E6E65F`
- Soft Green: `#00D7A0`
- Soft Blue: `#00BEDC`
- Deep Blue 80: `#333353`
- Deep Blue 60: `#66667E`
- Deep Blue 40: `#9999A9`
- Deep Blue 20: `#CCCCD4`
- Deep Blue 10: `#E5E5E9`
- Sand 辅助色: `#F3F3F0`, `#DFDFD9`, `#C5C5B8`, `#AAAA96`

## 色彩使用

- 深色页：背景 `#000028`，正文 White，强调只用 `#009999`、`#00C1B6` 或 `#E6E65F`
- 浅色页：背景默认 `#FFFFFF`，正文和标题默认 `#000028`
- `#F3F3F0` 仅在用户明确需要更柔和浅底时作为可选变体
- 封面标题：White + 少量 `#E6E65F` 关键词高亮，不要整句染色
- 形状和项目符号：优先 `#009999`
- 图表序列：`#009999`, `#E6E65F`, `#00C1B6`, `#00D7A0`, `#00BEDC`, `#000028`
- `#F3F3F0` 只作为 sand 辅助区块或底纹，不作为默认页面背景

## 背景模式

- `dark`：深蓝底，白字，重点词可用 Petrol / Light Petrol / Advanta Green
- `light`：默认白底，深蓝标题和正文
- `light-sand`：仅在明确需要更柔和底色时使用
- `image-overlay`：暗色图片加遮罩，保证标题和关键信息可读

## 字体观感

- 中文：接近 `PingFang SC`
- 英文、数字：接近 `Arial`
- 封面标题：超大、Bold，按内容长度接近 80pt / 60pt / 40pt 层级
- 内容页标题：接近 20pt Bold
- 正文：接近 18pt Regular
- 表格：表头接近 14pt Bold，内容接近 14pt Regular

## 版式锚点

- 画幅固定 16:9
- 左安全区约 3.4% slide width，对应 Advanta 母版 `0.45"`
- 右安全区约 3.4% slide width
- 内容页标题靠近顶部 6.9% slide height，对应 `0.52"`
- 非标题内容从约 20.7% slide height 开始，对应 `1.55"`
- 内容区底部保留品牌安全区，不要压到画面底边
- 正文默认左对齐；只有 quote / statement 可居中

## 栅格系统

- 默认使用 12-column content grid；所有主要内容块、表格、流程框、图片区、说明区都应吸附在同一套列网格上
- 页面内容区按“左安全区到右安全区”展开，列间距保持一致，不允许某一列明显漂移或脱离网格
- 标题区、主体区、辅助区、底部品牌区之间应共享统一的左对齐起点或统一列边界
- 垂直方向使用稳定节奏：标题区、主体区、说明区、底部品牌区之间保持一致的行距与区块间距
- 同一页面中的 box、card、panel、表格列、步骤块，顶部和底部应尽量落在共同水平线上
- 允许留白，但留白必须是“网格中的空列 / 空行”或有明确层级目的，不能形成无依据的大面积空白
- 如果页面视觉重心偏左或偏右，另一侧必须有明确的辅助区、图片区或结构区进行平衡，不能只剩空白
- 图片、图表、说明框要么贴齐列边界，要么全幅贴边；不要悬浮在栅格之外

## 构图原则

- 永远优先左对齐
- 宽留白，不要拥挤
- 强网格感，结构清楚
- 大标题和内容区关系明确
- 图片要么全幅，要么严格贴边，不要随意悬浮
- 留白必须可解释：要么来自列网格留白，要么来自标题区/品牌区节奏，不能是“元素没对齐后剩下来的空”

## 底部品牌区

默认应保留完整的 corporate brand zone 关系：
- 左下页码：`Page X`
- 底部页脚：`Restricted | © Siemens 20XX | YYYY-MM-DD`
- 右下品牌位：`SIEMENS`

要求：
- 页码固定在 bottom-left
- 页脚固定在底部 footer zone 贴近页码位置
- `SIEMENS` 固定在 bottom-right
- 这些元素是 corporate slide 的组成部分，不是可随意移动的装饰

如果用户没有明确要求完整页脚文案，也至少要保留清晰、稳定的底部品牌区关系，不让主体内容侵入。

## 组件规则

- 表格：清晰行列，表头可用 Deep Blue 色阶，行列线克制
- Agenda：可使用 Petrol 编号圆形或简洁编号列表
- Process：可使用箭头、三角或等宽步骤块
- Highlight box：Petrol 或 Advanta Green 文本/块，数量少，必须直角
- 阴影：默认无明显阴影；仅允许极轻微、接近官方模板默认组件阴影的效果
- Box / card / panel / table block：全部使用直角矩形，不使用 rounded corners，不使用 pill 形状
- 同类组件必须共用列宽、边界线和间距节奏，不要出现单独漂浮的模块

## 标题与正文关系

- 标题大、清晰、强识别
- 关键词可以双色强调，但不要超过标题词数的大约 30%
- 正文、列表、说明文字全部左对齐
- 避免把长段文字排成海报式居中大字

## 参考图使用规则

- `assets/reference-slides/...` 是给 agent 观察和提炼特征用的
- 不要把文件路径原样当成模型“可见参考图”
- 正确做法是先观察，然后把版式几何、大框架布局、色彩比例、留白密度、主次重心写成 prompt

## 禁止项

- 不要 emoji、贴纸、卡通化元素、多彩消费级元素混搭
- 不要居中海报式构图、startup landing page、霓虹 HUD、3D 图表、玻璃拟态
- 不要圆角卡片、圆角信息块、pill-shaped boxes
- 不要边框、相框、下划线式标题装饰
- 不要出现因为元素未对齐而形成的大面积无意义空白
- 不要让几个主要模块各自使用不同的对齐起点
- 不要节庆、Pride、Belonging、Disability、Ramadan、Diwali、Chinese New Year 等专题元素混入通用企业汇报页
