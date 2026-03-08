from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["缺少 YAML frontmatter 起始分隔线 ---"]

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, ["YAML frontmatter 不完整"]

    raw_yaml = parts[1].strip().splitlines()
    data: dict[str, str] = {}
    for line in raw_yaml:
        if ":" not in line:
            errors.append(f"frontmatter 行格式错误: {line}")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    for key in ("name", "description"):
        if not data.get(key):
            errors.append(f"frontmatter 缺少必填字段: {key}")

    return data, errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"{skill_dir.name}: 缺少 SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    _, frontmatter_errors = parse_frontmatter(text)
    errors.extend(f"{skill_dir.name}: {error}" for error in frontmatter_errors)

    required_sections = [
        "# ",
        "## 目标",
        "## 输出",
        "## 工作约束",
    ]
    for section in required_sections:
        if section not in text:
            errors.append(f"{skill_dir.name}: 缺少必需段落 {section}")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print("未找到 skills 目录")
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    if errors:
        print("技能校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"技能校验通过，共检查 {len(skill_dirs)} 个 skill。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

