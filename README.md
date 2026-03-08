# 软件开发全生命周期技能库

这是一个面向多种 coding agent 的中文 skill 仓库，用来把软件开发从“直接写代码”升级为“先澄清、再设计、再拆解、再实施、再验证、再收尾”的标准化流程，并补齐项目过程文档与经验沉淀能力。

仓库参考了 `superpowers` 的阶段化思想，也参考了 `opencode_ios_client` 的文档分层方法，但核心目标不是复制某一个模板，而是建立一套可持续产出高质量设计文档、工作记录和经验沉淀的中文 skill 系统。

## 平台定位

这个仓库不应该被理解为“Codex 专用”。

更准确的定位是：

- skill 内容本身是 agent-neutral 的
- 安装方式因不同工具而不同
- 当前优先提供 `Codex` 与 `OpenCode` 的安装入口
- 后续可以继续扩展到支持本地 skills 或插件机制的其他 coding agent

## 安装

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

## 设计原则

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
├─ ROADMAP.md
├─ CONTRIBUTING.md
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
└─ skills/
   ├─ 生命周期总控/
   ├─ 需求澄清/
   ├─ 技术方案/
   ├─ 任务拆解/
   ├─ 编码实施/
   ├─ 测试验证/
   ├─ 代码评审/
   ├─ 缺陷修复/
   ├─ 交付收尾/
   ├─ WORKING/
   └─ lessons/
```

## 能力分层

本仓库现在包含三层能力：

### 生命周期主线

- 生命周期总控
- 需求澄清
- 技术方案
- 任务拆解
- 编码实施
- 测试验证
- 代码评审
- 缺陷修复
- 交付收尾

### 文档决策增强

- `需求澄清` 负责问题定义、边界和非目标
- `技术方案` 负责技术决策、取舍和风险
- `任务拆解` 负责把设计决策转成执行计划

### 横向文档机制

- `WORKING`：维护项目当前动态工作文档
- `lessons`：沉淀可复用的经验、反模式与默认做法

## 使用方式

### 方式一：按阶段使用生命周期 skill

- 目标不清时，用 `需求澄清`
- 方案未定时，用 `技术方案`
- 任务过大时，用 `任务拆解`
- 开始落代码时，用 `编码实施`
- 需要证明结果时，用 `测试验证`
- 需要质量把关时，用 `代码评审`
- 出现 bug 时，用 `缺陷修复`
- 准备结束时，用 `交付收尾`

### 方式二：由 `生命周期总控` 分流

先触发 `生命周期总控`，再由它判断当前阶段与是否需要补充 `WORKING` / `lessons`。

### 方式三：文档机制独立触发

以下情况即使不在正式生命周期阶段，也适合触发：

- 出现新决策、新阻塞、新实测结论时，更新 `WORKING`
- 形成可迁移经验、失败教训、模式性 review 结论时，沉淀 `lessons`

## 仓库校验

### 校验 skill 结构

```bash
python scripts/validate_skills.py
```

### 校验示例场景完整性

```bash
python scripts/run_scenario_checks.py
```

## 当前状态

当前版本已经包含：

- 多工具安装入口
- 11 个中文 skill
- 8 个模板
- 3 个场景示例
- 2 个基础校验脚本

当前仓库已经从“生命周期 skill 库”升级为“生命周期 + 文档机制 + 经验沉淀”的完整工作流仓库。
