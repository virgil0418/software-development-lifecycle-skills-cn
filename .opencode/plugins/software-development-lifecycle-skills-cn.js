/**
 * OpenCode plugin for 软件开发全生命周期技能库
 *
 * Injects the 生命周期总控 bootstrap skill into the system prompt while
 * keeping all other skills discoverable through OpenCode's native skill tool.
 */

import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function stripFrontmatter(markdown) {
  const match = markdown.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
  return match ? match[1] : markdown;
}

function normalizePath(input, homeDir) {
  if (!input || typeof input !== "string") {
    return null;
  }

  const trimmed = input.trim();
  if (!trimmed) {
    return null;
  }

  if (trimmed === "~") {
    return homeDir;
  }

  if (trimmed.startsWith("~/")) {
    return path.resolve(homeDir, trimmed.slice(2));
  }

  return path.resolve(trimmed);
}

export const SoftwareDevelopmentLifecycleSkillsCnPlugin = async () => {
  const homeDir = os.homedir();
  const envConfigDir = normalizePath(process.env.OPENCODE_CONFIG_DIR, homeDir);
  const configDir = envConfigDir || path.join(homeDir, ".config", "opencode");
  const skillPath = path.resolve(__dirname, "../../skills/生命周期总控/SKILL.md");

  const getBootstrapContent = () => {
    if (!fs.existsSync(skillPath)) {
      return null;
    }

    const content = fs.readFileSync(skillPath, "utf8");
    const skillBody = stripFrontmatter(content);

    return `<EXTREMELY_IMPORTANT>
你已装备「软件开发全生命周期技能库」。

以下内容来自「生命周期总控」skill，已在当前会话中预加载。不要再次使用 skill 工具重复加载它；其余 skill 请继续通过 OpenCode 原生 skill 工具按需调用。

${skillBody}

**Tool Mapping for OpenCode**
- \`Skill\` tool -> OpenCode native \`skill\` tool
- \`TodoWrite\` -> \`update_plan\`
- 需要子代理时 -> 使用 OpenCode 的原生代理/协作能力
- 技能目录 -> \`${configDir}/skills/software-development-lifecycle-skills-cn\`

如果用户目标不明确，先由「生命周期总控」判断当前阶段，再决定是否进入 `需求澄清`、`技术方案`、`任务拆解`、`测试先行`、`编码实施`、`测试验证` 等 skill。
</EXTREMELY_IMPORTANT>`;
  };

  return {
    "experimental.chat.system.transform": async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (!bootstrap) {
        return;
      }

      output.system ||= [];
      output.system.push(bootstrap);
    },
  };
};

export default SoftwareDevelopmentLifecycleSkillsCnPlugin;
