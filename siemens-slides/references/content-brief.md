# Siemens Slide Spec

`siemens-slides` 在中文场景下默认先产出 `slide_spec`，再把它转成最终出图 prompt。这个 spec 既是生成前规格单，也是 SkillOpt 主训练对象。

## `slide_spec` 模板

```yaml
page_question: "这页只回答一个决策问题"
action_title: "完整结论句，不以分析/介绍/概况/说明收尾"
reasoning_pattern: "从 reasoning-patterns.md 中选择一个"
key_evidence:
  - "至少一个 L2 级证据锚点"
l2_hero_choice: "这页最重要的视觉证据"
supporting_points:
  - "3-5 个 L3 级支撑论据"
preferred_layout: "从 layouts.md 中选择一个最匹配的 layout"
component_strategy: "哪个主要内容区承担 icon / 节点 / mini-process / 关系线"
footer_spec:
  page_number: "Page X"
  footer_text: "Restricted | © Siemens {current_year} | {current_date_yyyy_mm_dd}"
  brand_mark: "SIEMENS"
  footer_family: "advanta-content-footer"
  logo_family: "compact-content-page-logo"
  text_alignment: "left"
color_strategy:
  page_mode: "light"
  body_text: "Deep Blue"
  hero_accent: "Siemens Petrol"
  connector_support: "Light Petrol"
  positive_accent: "Advanta Green"
  risk_accent: "Risk Orange"
overflow_recommendation: "single-page / suggest-split / compressed-single-page / multi-page-orchestration"
degrade_mode: "none / brief-only / image-plus-brief"
known_issues:
  - "当前已知偏差，可为空"
validation_result: "pending / pass / pass_with_warning / fail_retry / fail_degraded"
```

## 填写规则

- `page_question` 必须是单一问题，不能为空，不能拆成多条。
- `action_title` 必须是中文结论句，不是主题词。
- `reasoning_pattern` 只能选一个。
- `key_evidence` 至少 1 条；没有证据时先补证据，不先补装饰。
- `supporting_points` 默认 3 到 5 条；超出 5 条通常意味着应该拆页。
- `preferred_layout` 只能在 `reasoning_pattern` 确定后再选。
- `component_strategy` 要明确页面生命力由哪个区域承接，避免全页退化成文字墙。
- `slide_spec` 当前不单列 `takeaway` 字段，但最终页面规划必须保留一个明确的 L5 收束区或 takeaway strip。
- `footer_spec.footer_family` 普通内容页默认固定为 `advanta-content-footer`。
- `footer_spec.logo_family` 普通内容页默认固定为 `compact-content-page-logo`。
- `color_strategy.hero_accent` 默认只允许一个主强调色。
- `overflow_recommendation` 不是装饰字段；多问题输入默认先尝试 `suggest-split`。
- `validation_result` 在出图前必须是 `pending`。

## 输入压缩提示

原始输入可来自：

- `A` 主题词 / 一句话
- `B` 结构化内容
- `C` 原始材料（会议纪要、邮件、报告摘录）
- `D` 改版请求
- `E` 多页套件

压缩顺序固定为：

1. 先识别输入类型
2. 再写单一 `page_question`
3. 再定 `reasoning_pattern`
4. 再选 `preferred_layout`
5. 最后补 `component_strategy`、`footer_spec`、`color_strategy`

`slide_task` 与 `slide_spec` 的完整字段契约、允许值和样例见 `evals/skillopt/schema.md`。
