# Footer Geometry Extracted From Advanta Template

来源模板：
- Advanta slide library template 源文件的本地工作副本
- slide size：`12192000 x 6858000 EMU`
- 比例：`16:9`

本文件记录从 PowerPoint XML 母版 / 布局中直接提取的 footer 三分区几何，用于约束 skill 中的页脚、页码和 logo 位置。普通内容页默认使用 `compact-content-page-logo` family；封面、章节页和少数特殊页型才允许切换到较大的 logo family。

## Master 占位符

来自 `ppt/slideMasters/slideMaster1.xml`：

### Page Number Placeholder

- `x = 411162 EMU`
- `y = 6310800 EMU`
- `width = 648000 EMU`
- `height = 547200 EMU`
- `x = 3.3724%`
- `y = 92.0210%`
- `width = 5.3150%`
- `height = 7.9790%`
- `x = 32.37 pt`
- `y = 496.91 pt`
- `width = 51.02 pt`
- `height = 43.09 pt`

### Footer Placeholder

- `x = 1059160 EMU`
- `y = 6310800 EMU`
- `width = 9216000 EMU`
- `height = 547200 EMU`
- `x = 8.6873%`
- `y = 92.0210%`
- `width = 75.5906%`
- `height = 7.9790%`
- `x = 83.40 pt`
- `y = 496.91 pt`
- `width = 725.67 pt`
- `height = 43.09 pt`

说明：
- 这是母版里的基础 footer 文本占位框。
- 普通内容页 layout 会把 footer 文本区右侧收窄，以给右下 logo 留出稳定品牌位。

## 普通内容页 Family

默认适用于 `slideLayout34` 到 `slideLayout60` 对应的内容页 / 图形页 family。

### Page Zone

- 继承母版页码框：
- `x = 411162 EMU`
- `y = 6310800 EMU`
- `width = 648000 EMU`
- `height = 547200 EMU`

### Footer Zone

来自内容页 layout 的 footer placeholder：

- `x = 1059160 EMU`
- `y = 6310800 EMU`
- `width = 8640003 EMU`
- `height = 547200 EMU`
- `x = 8.6873%`
- `y = 92.0210%`
- `width = 70.8662%`
- `height = 7.9790%`
- `x = 83.40 pt`
- `y = 496.91 pt`
- `width = 680.32 pt`
- `height = 43.09 pt`

### Brand Zone

来自内容页右下 `Siemens Logo` 图片：

- `x = 10635188 EMU`
- `y = 6418800 EMU`
- `width = 1152000 EMU`
- `height = 183168 EMU`
- `x = 87.2309%`
- `y = 93.5958%`
- `width = 9.4488%`
- `height = 2.6709%`
- `right_edge = 96.6797%`
- `x = 837.42 pt`
- `y = 505.42 pt`
- `width = 90.71 pt`
- `height = 14.42 pt`
- `variant = compact-content-page-logo`

布局关系：
- `page_zone.right_edge = footer_zone.x`，母版关系可视为无缝衔接。
- footer text 必须从页码右侧几乎立即开始，不得另做底部居中说明文字。
- compact logo 位于 footer band 内更低的位置，视觉上与文字带分区，但仍属于同一品牌带。

## 封面 / 章节 / 特殊页 Large Logo Family

出现在 title / chapter divider / 部分 full-bleed 特殊页中，不能混入普通内容页。

### Brand Zone

主变体：

- `x = 10274400 EMU`
- `y = 6364800 EMU`
- `width = 1512000 EMU`
- `height = 240408 EMU`
- `x = 84.2717%`
- `y = 92.8084%`
- `width = 12.4016%`
- `height = 3.5055%`
- `right_edge = 96.6732%`
- `x = 809.01 pt`
- `y = 501.17 pt`
- `width = 119.06 pt`
- `height = 18.93 pt`
- `variant = large-cover-or-divider-logo`

微调变体：

- `x = 10275188 EMU`
- `y = 6366627 EMU`
- `width = 1512000 EMU`
- `height = 240408 EMU`
- `x = 84.2781%`
- `y = 92.8350%`
- `width = 12.4016%`
- `height = 3.5055%`
- `right_edge = 96.6797%`
- `x = 809.07 pt`
- `y = 501.31 pt`
- `width = 119.06 pt`
- `height = 18.93 pt`

说明：
- 该 family 明显更宽、更高，也更靠左。
- 只适用于封面、章节分隔页和少数特殊大版式页面。

## 对 skill 的直接约束

- 普通内容页默认固定使用：
  - `page_zone = 411162 / 6310800 / 648000 / 547200`
  - `footer_zone = 1059160 / 6310800 / 8640003 / 547200`
  - `brand_zone = 10635188 / 6418800 / 1152000 / 183168`
- 普通内容页不得误用更大的封面 logo family。
- 浅色内容页右下 `SIEMENS` 品牌字标默认使用 Siemens Petrol `#009999`。
- 深色内容页右下 `SIEMENS` 品牌字标可切换为白色，但不应改动几何。
