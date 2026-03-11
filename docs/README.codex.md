# 中文软件开发全生命周期技能库：Codex 安装说明

本仓库对 Codex 的接入方式参考了 `superpowers`：

- 仓库正常克隆到本地
- 通过 `~/.agents/skills/` 暴露 `skills/` 目录
- 由 Codex 在启动时发现并按需触发 skill

## 快速安装

告诉 Codex：

```text
Fetch and follow instructions from https://raw.githubusercontent.com/virgil0418/software-development-lifecycle-skills-cn/refs/heads/main/.codex/INSTALL.md
```

## 手动安装

### macOS / Linux

```bash
git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git ~/.codex/software-development-lifecycle-skills-cn
mkdir -p ~/.agents/skills
ln -s ~/.codex/software-development-lifecycle-skills-cn/skills ~/.agents/skills/software-development-lifecycle-skills-cn
```

### Windows

```powershell
git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git "$env:USERPROFILE\.codex\software-development-lifecycle-skills-cn"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\software-development-lifecycle-skills-cn" "$env:USERPROFILE\.codex\software-development-lifecycle-skills-cn\skills"
```

## 验证

```bash
ls -la ~/.agents/skills/software-development-lifecycle-skills-cn
```

确认它指向仓库下的 `skills/`，然后重启 Codex，新会话应能发现 `生命周期总控` 与其余 skill。

## 更新

```bash
cd ~/.codex/software-development-lifecycle-skills-cn && git pull
```

## 工作原理

Codex 会扫描本地 skills 目录，并按 `SKILL.md` 的 frontmatter 判断何时触发 skill。

因此，这个仓库不是“Codex 专用内容”，只是当前提供了对 Codex 友好的安装入口。
