# 为 OpenCode 安装中文软件开发全生命周期技能库

通过 OpenCode 的本地技能目录安装本仓库。

## macOS / Linux

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

## Windows PowerShell

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

## 验证

检查 `~/.config/opencode/skills/software-development-lifecycle-skills-cn` 是否正确指向仓库下的 `skills/`。

