# Siemens Slides ↔ SkillOpt Mapping

本仓库不 vendor Microsoft SkillOpt 源码，只提供可直接映射到 SkillOpt 的 seed skill、split 数据和 gate 资产。

## 对应关系

- Seed skill：`SKILL.md`
- Target rollout 输入：`evals/skillopt/train|val|test/items.json`
- Task schema：`evals/skillopt/schema.md`
- Hard gate：`scripts/skillopt_spec_lint.py`
- Judge rubric：`evals/skillopt/rubric.md`
- Smoke regression：`evals/skillopt/smoke/prompts.json`

## 推荐训练对象

优先优化 `slide_spec`，而不是直接优化最终图片：

- 训练期：生成 `slide_spec`，过 linter，再过 judge
- 部署期：由 `slide_spec` 继续生成最终 slide 图片
- 回归期：只用少量 held-out prompt 检查最终图片没有品牌或结构倒退

## 建议 loop

1. 用当前 `SKILL.md` 作为 seed skill
2. 对 `train/items.json` 做 rollout，要求产出 `slide_spec`
3. 跑 `scripts/skillopt_spec_lint.py`
4. 对通过 linter 的结果按 `rubric.md` 打分
5. 在 `val/items.json` 上做 acceptance gate
6. 接受的新 best 再用 `smoke/prompts.json` 做最终图片小样回归

## 为什么不把图片放进主 gate

- 图像质量评估噪声大
- footer、品牌色、中文标题可读性更适合先在 `slide_spec` 层做硬约束
- 用少量 smoke render 更能控制成本和误判
