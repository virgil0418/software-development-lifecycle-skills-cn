# 为 OpenCode 安装中文软件开发全生命周期技能库

通过 OpenCode 的本地 plugin 与 skills 发现机制安装本仓库。

安装完成后：

- `~/.config/opencode/plugins` 会发现本仓库的 OpenCode plugin
- `~/.config/opencode/skills` 会发现本仓库全部 skill
- OpenCode 启动时会自动注入 `生命周期总控` bootstrap 上下文

## macOS / Linux

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

## Windows PowerShell

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

确认：

- plugin 链接指向 `.opencode/plugins/software-development-lifecycle-skills-cn.js`
- skills 链接指向仓库下 `skills/`
- OpenCode 新会话启动后会预加载 `生命周期总控`

## 更新

```bash
cd ~/.config/opencode/software-development-lifecycle-skills-cn && git pull
```

由于 plugin 与 skills 都通过软链接暴露，更新仓库后无需重新建立链接。
