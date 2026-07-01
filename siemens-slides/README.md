# Siemens Slides

中文 Siemens Advanta 风格咨询页 skill，以及一套可重复执行的 SkillOpt 训练、回写、验证闭环。

## 目录

- [SKILL.md](./SKILL.md)
  当前仓库内的主 skill 定义，也是回写后的最终产物。
- [evals/skillopt](./evals/skillopt)
  中文 train / val / test 数据集、schema、rubric、smoke prompts。
- [tooling/skillopt-overlay](./tooling/skillopt-overlay)
  需要安装到本地 SkillOpt checkout 的最小补丁层。
- [scripts/install_skillopt_overlay.sh](./scripts/install_skillopt_overlay.sh)
  把 overlay 安装回本机 SkillOpt checkout。
- [scripts/run_skillopt_upgrade_cycle.sh](./scripts/run_skillopt_upgrade_cycle.sh)
  闭环脚本：同步、评估、训练、回写、验证。
- [Makefile](./Makefile)
  一键入口。

## 安全约定

- 不要把 gateway `key`、`base url`、本机绝对路径写进 git。
- 本地配置放在 `.env.skillopt.local`。
- 模板文件是 [.env.skillopt.local.example](./.env.skillopt.local.example)。
- `.gitignore` 已忽略 `.env.skillopt.local`、`skillopt.local.env` 等本地敏感文件。

初始化本地配置：

```bash
cp .env.skillopt.local.example .env.skillopt.local
```

然后填入你自己的：

```bash
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_AUTH_MODE=openai_compatible
```

## 前置条件

- 本机已有 SkillOpt checkout；如果不设置 `SKILLOPT_ROOT`，脚本会优先尝试 `../SkillOpt`
- 本机可用 Python；默认使用 `python3`，也可用 `PYTHON_BIN` 覆盖
- `.env.skillopt.local` 已配置好 Siemens gateway 访问参数

## 常用命令

查看所有入口：

```bash
make skillopt-help
```

安装 repo 内 overlay 到本机 SkillOpt：

```bash
make skillopt-install
```

只做轻量 smoke，不训练：

```bash
make skillopt-smoke
```

做更稳的重复验证，不训练：

```bash
make skillopt-verify
```

跑完整升级闭环：

```bash
make skillopt-upgrade
```

`skillopt-upgrade` 默认会做：

1. 安装 repo overlay 到本地 SkillOpt checkout
2. 把仓库 [SKILL.md](./SKILL.md) 同步到 SkillOpt seed
3. 跑 `valid_seen / valid_unseen` precheck
4. 跑 1 轮 SkillOpt 训练
5. 如果生成了更优 `best_skill.md`，回写到仓库 `SKILL.md`
6. 再对回写后的 repo skill 做 verify
7. 在 `tmp/skillopt-runs/<run_name>/` 下保存结果

## 常用环境变量

这些变量可以临时覆盖默认行为：

- `MODEL`
  默认 `gpt-5.4`
- `RUN_NAME`
  结果目录名
- `RUN_TRAIN`
  `0` 只验证，`1` 启动训练
- `PRECHECK_REPEATS`
  precheck 重复次数
- `VERIFY_REPEATS`
  verify 重复次数
- `SELECTION_REPEATS`
  train.py 内 selection gate 重复次数
- `TEST_REPEATS`
  train.py 内 test eval 重复次数
- `TRAIN_NUM_EPOCHS`
  训练 epoch 数
- `FAILURE_ONLY`
  是否只针对失败样本反思
- `INSTALL_OVERLAY`
  是否自动先安装 overlay

例子：

```bash
RUN_NAME=full-v1 \
MODEL=gpt-5.4 \
PRECHECK_REPEATS=3 \
VERIFY_REPEATS=3 \
SELECTION_REPEATS=3 \
TEST_REPEATS=1 \
make skillopt-upgrade
```

## 输出结果怎么看

每次升级闭环都会产出：

- `tmp/skillopt-runs/<run_name>/summary.md`
  本轮摘要
- `tmp/skillopt-runs/<run_name>/precheck/.../aggregate_summary.json`
  precheck 聚合结果
- `tmp/skillopt-runs/<run_name>/verify/.../aggregate_summary.json`
  verify 聚合结果
- `tmp/skillopt-runs/<run_name>/train/train.log`
  训练日志
- `tmp/skillopt-runs/<run_name>/best_skill_selected.md`
  本轮选中的 best skill 快照

通常重点看：

- `verify valid_seen hard_mean`
- `verify valid_unseen hard_mean`
- 训练日志里是否出现 `skip_no_patches`
- 是否真的生成并接受了新的 patch

## 说明

- 这个 repo 不 vendor Microsoft SkillOpt 全量源码，只保存我们需要的 overlay。
- 真正的训练对象是 `slide_spec` 文本规划层，不是最终图片。
- 最终图片仍只做 smoke check，不作为主 gate。
