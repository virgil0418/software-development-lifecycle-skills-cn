# 多平台接入层对齐设计

## 背景

当前仓库已经具备 `Claude Code`、`Codex`、`OpenCode` 三端安装说明，但仍主要停留在“文档告诉用户如何装”的层面。与同级目录中的 `superpowers` 相比，缺少以下三类产品化接入能力：

- `OpenCode` 的 plugin 注入层
- 根目录 `commands/` 命令兼容入口
- 更统一的安装、更新、排障文档结构

这导致当前仓库虽然“能装”，但在使用体验、心智模型与跨平台一致性上仍弱于 `superpowers`。

## 目标

构建一套参考 `superpowers` 的完整接入层，使本仓库具备：

1. 三端一致的安装入口与工作原理说明
2. `OpenCode` 会话启动时的 bootstrap 注入能力
3. 可发现的命令入口，降低用户从命令到 skill 的迁移成本
4. 与现有 skill 内容保持平台中立，不重写 skill 本体

## 非目标

- 不实现单一跨平台安装脚本
- 不重写现有 skill 内容或 frontmatter
- 不引入复杂的 npm 工程或额外构建链
- 不复制 `superpowers` 的全部命令体系与测试框架

## 方案对比

| 维度 | 方案A：完整仓库接入层 | 方案B：只补安装文档 | 方案C：统一安装脚本 |
|------|----------------------|--------------------|--------------------|
| 短期收益 | 高 | 中 | 中 |
| 长期维护 | 高 | 中 | 中 |
| 实现复杂度 | 中 | 低 | 中高 |
| 平台一致性 | 高 | 低 | 中 |
| 返工风险 | 低 | 高 | 中 |

【取舍说明】选择方案A。在时间维度上接受中等实现量，换取长期更稳定的平台接入结构；在复杂度维度上避免统一脚本的跨平台分支膨胀，转而使用各平台原生机制。

## 总体设计

### 1. Claude Code

保持当前 `.claude-plugin/` 与 `hooks/` 机制不变，只补 README 与平台对照说明。

### 2. Codex

继续使用 `.codex/INSTALL.md` 暴露 `skills/` 到 `~/.agents/skills/`。文档中补充更新、卸载、验证步骤，并与其他平台采用一致章节结构。

### 3. OpenCode

在 `.opencode/plugins/` 下新增 `software-development-lifecycle-skills-cn.js`，作为 OpenCode plugin 入口。

职责：

- 读取 `skills/生命周期总控/SKILL.md`
- 去除 frontmatter，仅注入正文
- 拼接 OpenCode 的工具映射说明
- 在 `experimental.chat.system.transform` 中注入 bootstrap 上下文

这样可以让 OpenCode 既通过 `skills/` 发现本仓库的 skill，又在会话启动时获得“先触发生命周期总控”的初始约束。

### 4. Commands

新增根目录 `commands/`，提供与 `superpowers` 风格一致的命令兼容入口。

初版命令不承载复杂逻辑，只承担两种职责：

- 作为用户可见的命令入口
- 明确提示应转向对应 skill

首批命令：

- `brainstorm.md`
- `write-plan.md`
- `execute-plan.md`

这些命令采用英文文件名，优先兼容 `superpowers` 使用习惯；正文则映射到本仓库的中文 skill，例如 `需求澄清`、`技术方案`、`任务拆解`、`编码实施`。

## 数据流

### OpenCode 启动流程

1. 用户按 `.opencode/INSTALL.md` 克隆仓库
2. 建立 `plugins/` 与 `skills/` 的软链接
3. OpenCode 启动时发现 plugin 与 skills
4. plugin 读取 `生命周期总控` 并注入系统上下文
5. 会话中再按需通过原生 `skill` 工具加载其他 skill

### Codex / Claude 流程

二者继续沿用各自原生机制，但 README 统一呈现安装、验证、更新、排障。

## 错误处理

- `OpenCode plugin` 读取 skill 失败时，不抛异常中断，而是跳过 bootstrap 注入
- 路径解析支持 `~` 展开，避免依赖固定用户目录
- 安装文档显式包含“删除旧软链接/目录后再建立”的步骤，减少重复安装失败

## 测试与验证

本次先采用轻量验证，不引入额外测试框架：

1. 新增 Python 测试，校验：
   - `commands/` 文件存在
   - `.opencode/plugins/software-development-lifecycle-skills-cn.js` 存在且引用 `生命周期总控`
   - `README.md`、`docs/README.opencode.md`、`.opencode/INSTALL.md` 都包含 plugin 安装说明
2. 使用 Node 对 plugin 文件做一次语法检查
3. 运行现有 `skill_eval.py check`，确认仓库基础结构未被破坏

## 技术债评估

- 命令层当前仅为兼容/引导入口，尚未形成更丰富的命令体系
- OpenCode plugin 采用零依赖实现，后续若共用 frontmatter 解析逻辑，可再抽公共模块
- 目前没有真正的跨平台安装器，这是刻意推迟的能力，而非遗漏

## 预演失败

- 如果 OpenCode 的 plugin API 后续变动，当前实现可能需要适配
- 如果未来增加更多 bootstrap 逻辑，单文件 plugin 可能需要拆分
- 如果命令入口增多，README 需要再按“命令层”和“skill 层”重构导航

## 交付结果

完成后，仓库将从“有三端安装说明”升级为“有三端接入层、OpenCode plugin、命令兼容层和统一文档”的完整结构。
