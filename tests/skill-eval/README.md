# Skill 评估（维护者用）

本目录用于支持“评估过程中的测评”，以比较同一 skill 在不同版本/不同提示/不同输出下的质量差异。

原则：

- 评估框架不属于 skill 执行流程的一部分，不应入侵 `skills/` 的分流与步骤。
- 评估应可复现：同一 case 的输出与评分应可存档、可回看、可对比。
- 评估先以人工 rubric 为主，脚本只做汇总与契约扫描，避免过度自动判优劣。

当前工具（统一入口 `scripts/skill_eval.py`）：

- 全量校验：`PYTHONPATH=scripts python scripts/skill_eval.py check [--json]`
- 输出契约校验：`PYTHONPATH=scripts python scripts/skill_eval.py output --skill 测试验证 --file <output.md> [--json]`
- 两份输出对比：`PYTHONPATH=scripts python scripts/skill_eval.py compare --skill 测试验证 --a <a.md> --b <b.md> [--json]`

