from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"

REQUIRED_HEADINGS = [
    "# 场景：",
    "## 场景描述",
    "## 推荐 skill 流程",
    "## 应得到的最小产物",
]


def validate_example(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"{path.name}: 缺少段落 {heading}")
    return errors


def main() -> int:
    if not EXAMPLES_DIR.exists():
        print("未找到 examples 目录")
        return 1

    example_files = sorted(EXAMPLES_DIR.glob("*.md"))
    errors: list[str] = []
    for example_file in example_files:
        errors.extend(validate_example(example_file))

    if errors:
        print("场景检查失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"场景检查通过，共检查 {len(example_files)} 个示例。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

