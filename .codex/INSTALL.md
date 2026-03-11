# 为 Codex 安装中文软件开发全生命周期技能库

通过 Codex 的本地技能发现机制安装本仓库。

## 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git ~/.codex/software-development-lifecycle-skills-cn
```

2. 暴露 skills 目录：

```bash
mkdir -p ~/.agents/skills
ln -s ~/.codex/software-development-lifecycle-skills-cn/skills ~/.agents/skills/software-development-lifecycle-skills-cn
```

3. 重启 Codex。

## Windows PowerShell

```powershell
git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git "$env:USERPROFILE\.codex\software-development-lifecycle-skills-cn"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\software-development-lifecycle-skills-cn" "$env:USERPROFILE\.codex\software-development-lifecycle-skills-cn\skills"
```

## 验证

```bash
ls ~/.agents/skills/software-development-lifecycle-skills-cn
```

确认能看到指向本仓库 `skills/` 的链接或目录映射。

## 更新

```bash
cd ~/.codex/software-development-lifecycle-skills-cn && git pull
```
