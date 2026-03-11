# 贡献指南

## 目标

本仓库欢迎继续扩展软件开发全生命周期相关的中文 skills，但新增内容必须保持以下原则：

- 一个 skill 只负责一个明确阶段或动作
- 说明何时触发，比解释概念更重要
- 输出骨架必须清晰，避免抽象空话
- 能复用模板就不重复造结构
- 能用脚本校验的地方尽量校验

## 新增 skill 的最小要求

新增 skill 目录至少包含：

- `SKILL.md`

`SKILL.md` 至少包含：

- YAML frontmatter
- skill 名称
- 触发场景说明
- 明确流程
- 输出要求
- 工作约束

## 编写风格

- 全部使用中文
- 尽量使用祈使句
- 先写动作，再写解释
- 优先给结构，不堆砌长篇概念介绍
- 一切围绕“另一个 Codex 如何更稳定执行”来写

## 修改前建议

修改技能前，优先先看：

- `README.md`
- `templates/`
- `examples/`
- `docs/能力地图.md`

## 提交前检查

运行：

```bash
PYTHONPATH=scripts python scripts/skill_eval.py check
```

确认结构校验、场景校验、契约校验全部通过后再提交。

