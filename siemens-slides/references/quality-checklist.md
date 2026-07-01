# Siemens Slide Quality Checklist

这个清单服务两件事：

- 日常出图时做自检
- SkillOpt-style 优化时做中文双层门禁

主训练对象是 `slide_spec`，不是最终图片。最终图片只做 smoke check。

## Layer 1: P0 Linter

先用确定性规则检查 `slide_spec`，任一项失败即 reject：

- 必须存在且只存在一个 `page_question`
- 必须存在 `action_title`
- 必须存在 `reasoning_pattern`
- 必须存在至少一个 `key_evidence`
- 必须存在 `l2_hero_choice`
- 必须存在 `overflow_recommendation`
- `action_title` 不能以 `分析`、`介绍`、`概况`、`说明` 收尾
- `footer_spec.footer_family` 必须是 `advanta-content-footer`
- `footer_spec.logo_family` 必须是 `compact-content-page-logo`
- `footer_spec.text_alignment` 必须是 `left`
- `footer_spec.brand_mark` 必须是 `SIEMENS`
- `color_strategy.body_text` 必须是 `Deep Blue`
- `color_strategy.hero_accent` 必须在允许的品牌 token 中
- `color_strategy.risk_accent` 必须是 `Risk Orange`

说明：
- L5 takeaway 当前不作为 `slide_spec` 的单独字段出现，但仍必须在最终页面规划和 smoke check 中成立。

默认脚本入口：

```bash
python3 scripts/skillopt_spec_lint.py path/to/slide_spec.json
```

## Layer 2: LLM Judge

P0 通过后，再按 `evals/skillopt/rubric.md` 评分。重点看：

- 中文 `Action Title` 是否像结论句，而不是主题标签
- `reasoning_pattern` 与 `preferred_layout` 是否匹配
- 页面是否 evidence-backed，而不是纯文字说明页
- 页面是否 ghost-readable
- 页面是否仍像 Siemens corporate consulting page
- `overflow_recommendation` 是否合理处理了多问题输入

门禁策略：

- 只有 `val` split 的中文总分严格提升，候选 skill 才能被接受
- judge 分数不能覆盖 P0 fail

## Layer 3: Smoke Check

最终图片不进入主 gate，只做小规模 held-out 回归。至少检查：

- 中文标题没有退化成主题标签
- 页面仍只有一个主要决策问题
- 仍存在清晰的 L2 hero evidence
- 仍存在 L5 takeaway
- footer 三分区没有跑位、侵入或居中漂浮
- 浅色页右下 `SIEMENS` 仍为 Siemens Petrol `#009999`
- 页面没有退化成海报、营销图或纯文字说明页

smoke prompt 集见 `evals/skillopt/smoke/prompts.json`。

## 一票否决项

- 标题以 `分析`、`介绍`、`概况`、`说明` 收尾
- 页面同时回答多个问题但 `overflow_recommendation` 仍写 `single-page`
- 没有任何 `key_evidence`
- 没有 `l2_hero_choice`
- 没有 L5 takeaway
- footer family 或 logo family 错误
- 页脚文字带被做成底部居中文案
- 颜色超出品牌 token 和语义色边界
- 页面无法明确归属到一个 reasoning pattern
- 页面退化成纯文字说明页
