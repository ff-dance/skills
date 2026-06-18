# Siemens Content Brief

当用户给的是会议纪要、草稿、DOCX 摘录或零散要点时，先压成一个生成前规格单，再进入论证模式和 layout 选择。

```yaml
input_type: "A / B / C / D / E"
audience_level: "L1 / L2 / L3"
storyline_mode: "single-page / 情境-冲突-方案 / 现状-目标-路径 / 总-分-总 / 并列论证"
page_question: "这页在回答什么决策问题"
action_title_draft: "先写成结论句"
reasoning_pattern: "从 reasoning-patterns.md 里选择"
key_evidence:
  - "至少一个 L2 级证据锚点"
l2_hero_choice: "这页最重要的视觉证据是什么"
supporting_points:
  - "3-5 个 L3 级支撑论据"
preferred_layout: "从 layouts.md 里选择"
component_strategy: "哪个主要内容区承担 icon / 节点 / mini-process / 关系线"
footer_spec:
  page_number: "Page X"
  footer_text: "Restricted | © Siemens {current_year} | {current_date_yyyy_mm_dd}"
  brand_mark: "SIEMENS"
footer_geometry:
  slide_size:
    width_emu: 12192000
    height_emu: 6858000
  page_zone:
    x_emu: 411162
    y_emu: 6310800
    width_emu: 648000
    height_emu: 547200
    x_pct: 3.37
    y_pct: 92.02
    width_pct: 5.31
  footer_zone:
    x_emu: 1059160
    y_emu: 6310800
    width_emu: 8640003
    height_emu: 547200
    x_pct: 8.69
    y_pct: 92.02
    width_pct: 70.87
    gap_from_page_zone_emu: 0
    text_alignment: "left"
    optical_rule: "begin almost flush to page number, never visually centered on slide"
  brand_zone:
    x_emu: 10635188
    y_emu: 6418800
    width_emu: 1152000
    height_emu: 183168
    x_pct: 87.23
    y_pct: 93.60
    width_pct: 9.45
    right_edge_pct: 96.68
    variant: "compact-content-page-logo"
dark_mode: "false / true"
overflow_recommendation: "single-page / suggest-split / compressed-single-page / multi-page-orchestration"
known_limitations:
  - "当前引擎风险点"
degrade_mode: "none / brief-only / image-plus-brief"
retry_count: 0
known_issues:
  - "当前已知偏差"
validation_result: "pending / pass / pass_with_warning / fail_retry / fail_degraded"
language: "zh / en"
```

## 输入类型定义

- `A`：主题词 / 一句话
- `B`：结构化内容
- `C`：原始材料（会议纪要、邮件、报告摘录）
- `D`：改版请求
- `E`：多页套件

## 使用规则

- `input_type` 先于 `page_question`。
- 如果 `page_question` 写不清楚，不要急着选 layout。
- 如果 `reasoning_pattern` 还没定，不允许写 `preferred_layout`。
- 如果 `key_evidence` 为空，优先补证据而不是补装饰。
- `l2_hero_choice` 必须能被清楚指出；不能只有“很多点都重要”。
- `supporting_points` 控制在 3 到 5 个，优先结构化分组与层级节奏，但不强制所有页面都做等分并列块。
- 如果输入同时覆盖多个独立页面问题，先把 `overflow_recommendation` 设为 `suggest-split`。
- 如果用户坚持单页，改为 `compressed-single-page`，并明确压缩策略与牺牲点。
- 如果用户要求多页，改为 `multi-page-orchestration`，并先定 `storyline_mode`。
- `component_strategy` 用来决定哪里承担页面生命力，避免全页退化成文字墙。
- `known_limitations` 用来记录当前引擎边界。
- `degrade_mode` 用来声明失败后的降级交付策略。
- `footer_spec` 只定义文案；`footer_geometry` 固定定义三分区位置关系。
- `footer_geometry.footer_zone` 默认是左锚定文字带，不是底部居中文案区。
- 普通内容页默认使用 compact `SIEMENS` logo 几何；除非明确是封面或特殊页型，否则不要切回更大的 logo family。
- `validation_result` 在出图前必须是 `pending`，出图回看后改为最终状态。
