# 中文软件开发全生命周期技能库：OpenCode 安装说明

本仓库对 OpenCode 的接入方式参考了 `superpowers`，但 bootstrap 内容改为注入 `生命周期总控`。

## 快速安装

告诉 OpenCode：

```text
Clone https://github.com/virgil0418/software-development-lifecycle-skills-cn to ~/.config/opencode/software-development-lifecycle-skills-cn, then symlink ~/.config/opencode/software-development-lifecycle-skills-cn/.opencode/plugins/software-development-lifecycle-skills-cn.js to ~/.config/opencode/plugins/software-development-lifecycle-skills-cn.js, then symlink its skills directory to ~/.config/opencode/skills/software-development-lifecycle-skills-cn, then restart OpenCode.
```

## 手动安装

### macOS / Linux

```bash
if [ -d ~/.config/opencode/software-development-lifecycle-skills-cn ]; then
  cd ~/.config/opencode/software-development-lifecycle-skills-cn && git pull
else
  git clone https://github.com/virgil0418/software-development-lifecycle-skills-cn.git ~/.config/opencode/software-development-lifecycle-skills-cn
fi

mkdir -p ~/.config/opencode/plugins ~/.config/opencode/skills
rm -f ~/.config/opencode/plugins/software-development-lifecycle-skills-cn.js
rm -rf ~/.config/opencode/skills/software-development-lifecycle-skills-cn

ln -s ~/.config/opencode/software-development-lifecycle-skills-cn/.opencode/plugins/software-development-lifecycle-skills-cn.js ~/.config/opencode/plugins/software-development-lifecycle-skills-cn.js
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

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\plugins"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\opencode\skills"
Remove-Item "$env:USERPROFILE\.config\opencode\plugins\software-development-lifecycle-skills-cn.js" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.config\opencode\skills\software-development-lifecycle-skills-cn" -Recurse -Force -ErrorAction SilentlyContinue

New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\plugins\software-development-lifecycle-skills-cn.js" -Target "$env:USERPROFILE\.config\opencode\software-development-lifecycle-skills-cn\.opencode\plugins\software-development-lifecycle-skills-cn.js"
cmd /c mklink /J "$env:USERPROFILE\.config\opencode\skills\software-development-lifecycle-skills-cn" "$env:USERPROFILE\.config\opencode\software-development-lifecycle-skills-cn\skills"
```

## 验证

```bash
ls -l ~/.config/opencode/plugins/software-development-lifecycle-skills-cn.js
ls -l ~/.config/opencode/skills/software-development-lifecycle-skills-cn
```

两者都应指向本仓库，且 OpenCode 新会话启动后会预加载 `生命周期总控`。

## 更新

```bash
cd ~/.config/opencode/software-development-lifecycle-skills-cn && git pull
```

## 工作原理

OpenCode 通过两条路径发现本仓库：

1. `~/.config/opencode/plugins/software-development-lifecycle-skills-cn.js`  
   指向 `.opencode/plugins/software-development-lifecycle-skills-cn.js`，用于把 `生命周期总控` 注入系统上下文
2. `~/.config/opencode/skills/software-development-lifecycle-skills-cn`  
   指向仓库下 `skills/`，用于让原生 `skill` 工具发现其他 skill

所以本仓库的 skill 内容依然平台中立，平台差异主要体现在安装与 bootstrap 方式。
