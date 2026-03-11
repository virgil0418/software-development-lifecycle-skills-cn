from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class PlatformIntegrationTest(unittest.TestCase):
    def test_opencode_plugin_exists_with_bootstrap_markers(self) -> None:
        plugin_path = REPO_ROOT / ".opencode" / "plugins" / "software-development-lifecycle-skills-cn.js"
        self.assertTrue(plugin_path.exists(), f"missing plugin file: {plugin_path}")

        content = plugin_path.read_text(encoding="utf-8")
        self.assertIn("生命周期总控", content)
        self.assertIn("experimental.chat.system.transform", content)
        self.assertIn("OpenCode", content)

    def test_command_entrypoints_exist(self) -> None:
        for command_name in ("brainstorm.md", "write-plan.md", "execute-plan.md"):
            command_path = REPO_ROOT / "commands" / command_name
            self.assertTrue(command_path.exists(), f"missing command file: {command_path}")

    def test_readme_mentions_commands_and_platform_integration(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## 命令入口", readme)
        self.assertIn("OpenCode plugin", readme)
        self.assertIn("commands/", readme)

    def test_opencode_docs_cover_plugin_and_skill_symlinks(self) -> None:
        install_doc = (REPO_ROOT / ".opencode" / "INSTALL.md").read_text(encoding="utf-8")
        public_doc = (REPO_ROOT / "docs" / "README.opencode.md").read_text(encoding="utf-8")

        for content in (install_doc, public_doc):
            self.assertIn(".opencode/plugins/software-development-lifecycle-skills-cn.js", content)
            self.assertIn("~/.config/opencode/plugins", content)
            self.assertIn("~/.config/opencode/skills", content)
            self.assertIn("生命周期总控", content)

    def test_platform_docs_have_verify_and_update_sections(self) -> None:
        docs = {
            "claude": (REPO_ROOT / "docs" / "README.claude.md").read_text(encoding="utf-8"),
            "codex": (REPO_ROOT / "docs" / "README.codex.md").read_text(encoding="utf-8"),
            "opencode": (REPO_ROOT / "docs" / "README.opencode.md").read_text(encoding="utf-8"),
        }

        for name, content in docs.items():
            self.assertIn("## 验证", content, f"{name} doc missing verify section")
            self.assertIn("## 更新", content, f"{name} doc missing update section")


if __name__ == "__main__":
    unittest.main()
