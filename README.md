# 软件开发全生命周期技能库

> 面向 coding agent 的中文 skill 工作流：先澄清、再设计、再拆解、再实施、再验证、再交付，并把过程文档与项目记忆沉淀下来。

这不是一个“提示词合集”，而是一套可复用的软件工程开发生命周期（SDLC）工作流：当你让 agent 写代码时，它应先把目标、边界与验收说清楚，再做方案决策，再拆解任务，再进入实现与验证，最后交付收尾。

本仓库参考了 `superpowers` 的阶段化思想，也参考了 `opencode_ios_client` 的文档分层方法，但核心目标不是复制某一个模板，而是建立一套可持续产出高质量设计文档、工作记录和经验沉淀的中文 skill 系统。

## 你会得到什么

- 可复用的生命周期主线：从需求澄清到交付收尾，减少“过早写代码”的失败。
- 更稳定的交付证据：用测试与验证说明“为什么算完成”，而不是口头保证。
- 项目记忆（差异化能力）：`WORKING` 记录当前事实，`lessons` 沉淀可复用经验，避免多轮对话后偏航。
- 多平台接入：同一套 skill 可用于 `Claude Code`、`Codex`、`OpenCode`。

## 它如何改变 agent 的工作方式

装上这套 skill 后，理想状态下的 agent 不应再这样工作：

- 听到需求就直接写代码
- 只记住当前对话，忘记前面已经确认过的决策
- 测一下能跑就说“完成了”

它应更接近下面这条行为链：

1. 先由 `生命周期总控` 判断当前所处阶段，而不是盲目进入实现。
2. 如果问题还不清楚，就先进入 `需求澄清`，把目标、范围、约束和验收定义清楚。
3. 如果需求已经明确，但做法还没定，就进入 `技术方案`，比较方案、写清取舍与风险。
4. 如果方案已定但任务过大，就用 `任务拆解` 把设计转成可执行、可验证的步骤。
5. 真正动手实现前，先经过 `测试先行`，再进入 `编码实施`。
6. 实现完成后，不靠口头保证，而是通过 `测试验证`、`代码评审`、`接收评审` 和必要的 `缺陷修复` 来证明结果。
7. 最后由 `交付收尾` 输出变更说明、验证证据、剩余风险与后续事项。

## 典型 Lifecycle Flow

最典型的一条主线如下：

`生命周期总控` → `需求澄清` → `技术方案` → `任务拆解` → `测试先行` → `编码实施` → `测试验证` → `代码评审` / `接收评审` → `交付收尾`

如果是缺陷场景，链路通常变成：

`生命周期总控` → `系统化调试` → `缺陷修复` → `测试验证` → `交付收尾`

## 项目记忆：WORKING 与 lessons

很多 agent 在复杂项目里失败，不是不会写代码，而是缺少稳定的上下文锚点。为此本仓库把记录机制提升为一等能力：

- `WORKING`：维护项目“现在到底是什么状态”，包括已确认结论、阻塞、实测结果与下一步。
- `lessons`：沉淀“下次仍然会遇到的问题”，包括默认做法、踩坑、复盘与反模式。

这两者共同降低重复讨论、遗忘决策、偏离目标的概率。

## 全局纪律

- `完成验证`：没有验证证据，不允许宣称完成。

## 能力地图（含架构图）

仓库整体 skill 关系、职责边界与典型链路见 [docs/能力地图.md](docs/能力地图.md)。

## 安装

安装方式因工具而不同，但 skill 内容本身是 agent-neutral 的。

### Claude Code（推荐）

```bash
claude plugin marketplace add virgil0418/software-development-lifecycle-skills-cn
claude plugin install software-development-lifecycle-skills-cn@sdlc-skills-cn-dev
```

详细说明见 `docs/README.claude.md`。

### Codex

告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/virgil0418/software-development-lifecycle-skills-cn/refs/heads/main/.codex/INSTALL.md
```

详细说明见 `docs/README.codex.md`。

### OpenCode

告诉 OpenCode：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/virgil0418/software-development-lifecycle-skills-cn/refs/heads/main/.opencode/INSTALL.md
```

详细说明见 `docs/README.opencode.md`。

### 验证安装（建议）

- `Claude Code`：开启新会话，确认 skill 可见，并能触发 `生命周期总控` 引导。
- `Codex`：重启后确认能发现本仓库 skill；最小验证是让它先进入阶段判断再行动。
- `OpenCode`：确认 OpenCode plugin 与 skills 的软链接存在，且会话启动时预加载 `生命周期总控`。OpenCode plugin 入口见 `.opencode/plugins/software-development-lifecycle-skills-cn.js`。

### 更新

- `Claude Code`：`claude plugin update software-development-lifecycle-skills-cn`
- `Codex`：`cd ~/.codex/software-development-lifecycle-skills-cn && git pull`
- `OpenCode`：`cd ~/.config/opencode/software-development-lifecycle-skills-cn && git pull`

### 工作原理概览

| 工具 | 接入方式 | Bootstrap 方式 |
|------|----------|----------------|
| Claude Code | `.claude-plugin/` + `hooks/` | SessionStart hook 注入 `生命周期总控` |
| Codex | `.codex/INSTALL.md` + `~/.agents/skills/` | 依赖原生 skills 发现 |
| OpenCode | OpenCode plugin + skills symlink | `.opencode/plugins/software-development-lifecycle-skills-cn.js` 注入 `生命周期总控` |

## 命令入口

为兼容 `superpowers` 风格的用户习惯，仓库新增 `commands/` 目录作为命令兼容层。

- `commands/brainstorm.md`：引导转向 `生命周期总控`、`需求澄清`、`技术方案`
- `commands/write-plan.md`：引导转向 `任务拆解`
- `commands/execute-plan.md`：引导转向 `测试先行`、`编码实施`、`测试验证`

这些命令当前不承载复杂逻辑，重点是把“命令式入口”平滑映射到本仓库的中文 skill 体系。

## 设计原则（为什么这样做）

### 1. 先定义成功，再开始实现

任何 skill 都不能只告诉代理做什么，还要说明做到什么程度才算完成。

### 2. 先明确边界，再展开设计

需求不清时不要急着设计，方案未定时不要急着写代码，缺少验收口径时不要声称完成。

### 3. 先交最小闭环，再扩展范围

优先追求最小可验证结果，避免 skill 指令过大、过散、不可落地。

### 4. 优先证据，不靠口头保证

完成、修复、通过、可交付，都需要对应证据：测试结果、复现步骤、影响范围、剩余风险。

### 5. 文档不是模板，而是决策与过程的载体

高质量文档来自边界判断、方案取舍、过程留痕和经验复用，而不是章节排版本身。

## 仓库结构

```text
软件开发全生命周期技能库/
├─ README.md
├─ CONTRIBUTING.md
├─ .claude-plugin/        # Claude Code plugin 配置
│  ├─ plugin.json
│  └─ marketplace.json
├─ .opencode/
│  ├─ INSTALL.md
│  └─ plugins/            # OpenCode plugin 注入层
├─ commands/              # superpowers 风格命令兼容入口
├─ hooks/                 # Claude Code SessionStart hook
│  ├─ hooks.json
│  ├─ run-hook.cmd
│  └─ session-start
├─ templates/
│  ├─ 需求说明模板.md
│  ├─ 技术方案模板.md
│  ├─ 任务清单模板.md
│  ├─ 测试验证模板.md
│  ├─ 代码评审模板.md
│  ├─ 交付总结模板.md
│  ├─ WORKING模板.md
│  └─ lessons模板.md
├─ examples/
├─ scripts/
├─ tests/
└─ skills/
   ├─ 生命周期总控/
   ├─ 需求澄清/
   ├─ 技术方案/
   ├─ 任务拆解/
   ├─ 测试先行/
   ├─ 编码实施/
   ├─ 测试验证/
   ├─ 代码评审/          # 发起评审
   ├─ 接收评审/          # 接收评审反馈
   ├─ 系统化调试/
   ├─ 缺陷修复/
   ├─ 交付收尾/
   ├─ 完成验证/          # 全局纪律
   ├─ WORKING/
   ├─ lessons/
   └─ 技能编写/
```

## 能力分层（参考）

本仓库现在包含四层能力：

### 生命周期主线

- 生命周期总控
- 需求澄清
- 技术方案
- 任务拆解
- 测试先行
- 编码实施
- 测试验证
- 代码评审（发起评审）
- 接收评审（接收反馈）
- 系统化调试
- 缺陷修复
- 交付收尾

### 执行纪律

- `完成验证`：全局门控纪律，没有验证证据就不许宣称完成
- 强制依赖链：关键 skill 之间的 REQUIRED 级别前置条件

### 文档决策增强

- `需求澄清` 负责问题定义、边界和非目标
- `技术方案` 负责技术决策、取舍和风险
- `任务拆解` 负责把设计决策转成执行计划

### 横向文档机制

- `WORKING`：维护项目当前动态工作文档
- `lessons`：沉淀可复用的经验、反模式与默认做法

### 元能力

- `技能编写`：用 TDD 方法编写和加固 skill

## 使用方式（快速选择）

### 方式一：按阶段使用生命周期 skill

- 目标不清时，用 `需求澄清`
- 方案未定时，用 `技术方案`
- 任务过大时，用 `任务拆解`
- 新增功能、修 bug、改行为并准备进入实现时，用 `测试先行`
- 开始落代码时，用 `编码实施`
- 需要证明结果时，用 `测试验证`
- 需要质量把关时，用 `代码评审`
- 收到评审反馈需要处理时，用 `接收评审`
- 出现 bug 且根因未明时，用 `系统化调试`
- 根因已明确、需要进入修复时，用 `缺陷修复`
- 准备结束时，用 `交付收尾`

### 方式二：默认从 `生命周期总控` 开始

先触发 `生命周期总控`，再由它判断当前阶段与是否需要补充 `WORKING` / `lessons`。

### 方式三：单独使用项目记忆机制

以下情况即使不在正式生命周期阶段，也适合触发：

- 出现新决策、新阻塞、新实测结论时，更新 `WORKING`
- 形成可迁移经验、失败教训、模式性 review 结论时，沉淀 `lessons`

## 仓库校验

统一入口：`scripts/skill_eval.py`，需要 `PYTHONPATH=scripts`。

### 全量校验（结构 + 场景 + 契约）

```bash
PYTHONPATH=scripts python scripts/skill_eval.py check
```

加 `--json` 可追加 JSON 摘要输出。

### 校验 agent 产出是否满足输出契约

```bash
PYTHONPATH=scripts python scripts/skill_eval.py output --skill 测试验证 --file path/to/output.md
```

### 对比两份 agent 产出

```bash
PYTHONPATH=scripts python scripts/skill_eval.py compare --skill 测试验证 --a a.md --b b.md
```

契约定义位于 `tests/contracts.json`，包含 `skill_text`（校验仓库内 skill 定义）和 `skill_output`（校验 agent 实际产出）两类规则。

## 当前状态

当前版本已经包含：

- 多工具安装入口
- OpenCode plugin 注入层
- `commands/` 命令兼容层
- 16 个中文 skill（含 `完成验证` 纪律 skill 和 `接收评审` skill）
- 8 个模板
- 3 个场景示例
- 统一评估工具（`skill_eval.py` + `skill_eval_core.py`）
- 18 条契约测试规则
- 强制依赖链（REQUIRED 级别前置条件）

当前仓库已经从"生命周期 skill 库"升级为"生命周期 + 执行纪律 + 文档机制 + 经验沉淀 + 强制依赖 + 统一评估"的完整工作流仓库。
