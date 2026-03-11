# 中文软件开发全生命周期技能库：Claude Code 安装说明

本仓库通过 Claude Code 的 plugin 系统接入。安装后：

- 所有 16 个 skill 自动注册到 Claude Code 的 `Skill` 工具
- SessionStart hook 自动注入「生命周期总控」引导上下文
- 每次会话启动时，Claude Code 会自动了解可用的 skill 体系

## 方式一：从 GitHub 仓库安装（推荐）

```bash
claude plugin marketplace add virgil0418/software-development-lifecycle-skills-cn
claude plugin install software-development-lifecycle-skills-cn@sdlc-skills-cn-dev
```

## 方式二：从本地路径安装

如果你已经克隆了仓库：

```bash
git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git
claude plugin marketplace add /path/to/software-development-lifecycle-skills-cn
claude plugin install software-development-lifecycle-skills-cn@sdlc-skills-cn-dev
```

## 方式三：单次会话加载（不持久安装）

```bash
claude --plugin-dir /path/to/software-development-lifecycle-skills-cn
```

这种方式只在当前会话生效，不会写入全局配置。适合试用或调试。

## 验证

启动新的 Claude Code 会话后，检查：

- 本仓库 skill 是否出现在 `Skill` 工具可见列表中
- 新会话是否已经具备 `生命周期总控` 的引导上下文

如果要做最小验证，可直接让 Claude Code 处理一个模糊需求，看它是否先进入阶段判断，而不是直接写代码。

## 更新

```bash
claude plugin update software-development-lifecycle-skills-cn
```

## 卸载

```bash
claude plugin uninstall software-development-lifecycle-skills-cn
claude plugin marketplace remove sdlc-skills-cn-dev
```

## 工作原理

Claude Code plugin 系统通过以下机制工作：

1. `.claude-plugin/plugin.json` — 声明 plugin 元信息
2. `.claude-plugin/marketplace.json` — 声明 marketplace 元信息，供 `marketplace add` 使用
3. `skills/` — 所有 skill 自动注册，可通过 `Skill` 工具按名调用
4. `hooks/hooks.json` — 声明 SessionStart hook
5. `hooks/session-start` — 在每次会话启动时将「生命周期总控」skill 内容注入上下文

### SessionStart hook 做了什么

每次 Claude Code 会话启动（包括 resume、clear、compact）时，hook 会：

1. 读取 `skills/生命周期总控/SKILL.md` 的完整内容
2. 将其包装为 `<EXTREMELY_IMPORTANT>` 上下文注入到会话中
3. 这让 Claude Code 在每次对话开始时就知道如何使用生命周期 skill 体系

## 与其他安装方式的关系

本仓库的 skill 内容是平台中立的。不同 coding agent 使用不同安装方式：

| 工具 | 安装方式 | 详细说明 |
|------|----------|----------|
| Claude Code | plugin 系统 | 本文档 |
| Codex | symlink 到 `~/.agents/skills/` | `docs/README.codex.md` |
| OpenCode | OpenCode plugin + skills symlink | `docs/README.opencode.md` |
