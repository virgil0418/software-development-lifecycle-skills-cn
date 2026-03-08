# 中文软件开发全生命周期技能库：OpenCode 安装说明

本仓库对 OpenCode 的接入方式参考了 `superpowers` 的 OpenCode 安装结构。

## 快速安装

告诉 OpenCode：

```text
Clone https://github.com/virgil0418/software-development-lifecycle-skills-cn to ~/.config/opencode/software-development-lifecycle-skills-cn, then symlink its skills directory to ~/.config/opencode/skills/software-development-lifecycle-skills-cn, then restart OpenCode.
```

## 手动安装

### macOS / Linux

```bash
if [ -d ~/.config/opencode/software-development-lifecycle-skills-cn ]; then
  cd ~/.config/opencode/software-development-lifecycle-skills-cn && git pull
else
  git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git ~/.config/opencode/software-development-lifecycle-skills-cn
fi

mkdir -p ~/.config/opencode/skills
rm -rf ~/.config/opencode/skills/software-development-lifecycle-skills-cn
ln -s ~/.config/opencode/software-development-lifecycle-skills-cn/skills ~/.config/opencode/skills/software-development-lifecycle-skills-cn
```

### Windows

```powershell
if (Test-Path "$env:USERPROFILE\.config\opencode\software-development-lifecycle-skills-cn") {
  Set-Location "$env:USERPROFILE\.config\opencode\software-development-lifecycle-skills-cn"
  git pull
} else {
  git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git "$env:USERPROFILE\.config\opencode\software-development-lifecycle-skills-cn"
}

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\skills"
if (Test-Path "$env:USERPROFILE\.config\opencode\skills\software-development-lifecycle-skills-cn") {
  Remove-Item -Recurse -Force "$env:USERPROFILE\.config\opencode\skills\software-development-lifecycle-skills-cn"
}
cmd /c mklink /J "$env:USERPROFILE\.config\opencode\skills\software-development-lifecycle-skills-cn" "$env:USERPROFILE\.config\opencode\software-development-lifecycle-skills-cn\skills"
```

## 工作原理

OpenCode 侧重点也是把本仓库 `skills/` 暴露到它自己的 skills 目录中。

所以本仓库的 skill 内容本身依然是平台中立的，差异主要在安装方式。

