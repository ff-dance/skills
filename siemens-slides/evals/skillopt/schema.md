# Siemens Slides SkillOpt Schema

本目录只服务中文场景。SkillOpt 主训练对象是 `slide_spec`，不是最终图片。

## `slide_task`

每个任务项固定包含以下字段：

```json
{
  "id": "train-001",
  "user_request": "用户的直接请求",
  "source_material": "原始材料，可为空字符串",
  "input_type": "A | B | C | D | E",
  "expected_page_question": "目标单一决策问题",
  "expected_reasoning_pattern": "目标 reasoning pattern",
  "must_include": ["必须出现的关键信号"],
  "must_avoid": ["必须避免的错误"],
  "expected_overflow_recommendation": "single-page | suggest-split | compressed-single-page | multi-page-orchestration"
}
```

字段约束：

- `user_request` 永远用中文
- `source_material` 用中文摘要或原始记录，不再构造英文材料
- `input_type`
  - `A` 主题词 / 一句话
  - `B` 结构化内容
  - `C` 原始材料
  - `D` 改版请求
  - `E` 多页套件
- `must_include` 用于 judge 查验
- `must_avoid` 用于失败模式回放

## `slide_spec`

候选 skill 在 rollout 后应输出如下结构：

```json
{
  "page_question": "这页只回答一个决策问题",
  "action_title": "中文结论句",
  "reasoning_pattern": "⑤ 结构化总览",
  "key_evidence": ["至少一个 L2 级证据锚点"],
  "l2_hero_choice": "最重要的视觉证据",
  "supporting_points": ["3-5 个 L3 级支撑论据"],
  "preferred_layout": "content-basic-light",
  "component_strategy": "哪个主要内容区承担局部结构节奏",
  "footer_spec": {
    "page_number": "Page X",
    "footer_text": "Restricted | © Siemens 2026 | 2026-06-18",
    "brand_mark": "SIEMENS",
    "footer_family": "advanta-content-footer",
    "logo_family": "compact-content-page-logo",
    "text_alignment": "left"
  },
  "color_strategy": {
    "page_mode": "light",
    "body_text": "Deep Blue",
    "hero_accent": "Siemens Petrol",
    "connector_support": "Light Petrol",
    "positive_accent": "Advanta Green",
    "risk_accent": "Risk Orange"
  },
  "overflow_recommendation": "single-page",
  "degrade_mode": "none",
  "known_issues": [],
  "validation_result": "pending"
}
```

## Canonical 值

- `footer_spec.footer_family = advanta-content-footer`
- `footer_spec.logo_family = compact-content-page-logo`
- `footer_spec.text_alignment = left`
- `footer_spec.brand_mark = SIEMENS`
- `color_strategy.body_text = Deep Blue`
- `color_strategy.risk_accent = Risk Orange`

## Split 使用方式

- `train/`：rollout + reflect 的主要样本
- `val/`：selection split，也是 acceptance gate 的主依据
- `test/`：held-out 回归，不参与候选接受
- `smoke/prompts.json`：最终图片小样回归，不参与主 gate
