"""skill_eval_core: 统一的契约校验引擎。

支持两种 check_type:
  - skill_text:   校验仓库内的 skill/模板源文件（开发时门禁）
  - skill_output: 校验 agent 使用 skill 后的实际产出（使用后抽检）
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    name: str
    check_type: str
    ok: bool
    missing: list[str] = field(default_factory=list)
    forbidden_hits: list[str] = field(default_factory=list)

    @property
    def penalty(self) -> int:
        return len(self.missing) + len(self.forbidden_hits) * 2


def load_contracts(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_text(text: str, must_contain: list[str], must_not_contain: list[str]) -> tuple[list[str], list[str]]:
    missing = [p for p in must_contain if p not in text]
    forbidden = [p for p in must_not_contain if p in text]
    return missing, forbidden


# ── skill_text 校验：读仓库内文件 ──────────────────────────────

def run_skill_text_checks(contracts: list[dict[str, Any]], repo_root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for c in contracts:
        if c.get("check_type") != "skill_text":
            continue
        target = repo_root / c["target"]
        if not target.exists():
            results.append(CheckResult(
                name=c["name"], check_type="skill_text", ok=False,
                missing=[f"目标文件不存在: {c['target']}"],
            ))
            continue
        text = target.read_text(encoding="utf-8")
        missing, forbidden = check_text(
            text, c.get("must_contain", []), c.get("must_not_contain", []),
        )
        results.append(CheckResult(
            name=c["name"], check_type="skill_text",
            ok=not missing and not forbidden,
            missing=missing, forbidden_hits=forbidden,
        ))
    return results


# ── skill_output 校验：读外部文件 ──────────────────────────────

def run_skill_output_check(
    contracts: list[dict[str, Any]], skill_name: str, text: str,
) -> CheckResult:
    for c in contracts:
        if c.get("check_type") != "skill_output":
            continue
        if c.get("skill") != skill_name:
            continue
        missing, forbidden = check_text(
            text, c.get("must_contain", []), c.get("must_not_contain", []),
        )
        return CheckResult(
            name=c["name"], check_type="skill_output",
            ok=not missing and not forbidden,
            missing=missing, forbidden_hits=forbidden,
        )
    available = sorted({c["skill"] for c in contracts if c.get("check_type") == "skill_output"})
    raise KeyError(f"未找到 skill_output 契约: {skill_name}. 可选: {', '.join(available)}")


# ── 结构校验：skill 目录 + frontmatter ─────────────────────────

def validate_skill_structure(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"{skill_dir.name}: 缺少 SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        errors.append(f"{skill_dir.name}: 缺少 YAML frontmatter")
    else:
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw = parts[1].strip().splitlines()
            data: dict[str, str] = {}
            for line in raw:
                if ":" in line:
                    k, v = line.split(":", 1)
                    data[k.strip()] = v.strip()
            for key in ("name", "description"):
                if not data.get(key):
                    errors.append(f"{skill_dir.name}: frontmatter 缺少 {key}")
        else:
            errors.append(f"{skill_dir.name}: YAML frontmatter 不完整")

    for section in ("# ", "## 目标", "## 输出", "## 工作约束"):
        if section not in text:
            errors.append(f"{skill_dir.name}: 缺少必需段落 {section}")

    return errors


def run_structure_checks(repo_root: Path) -> list[str]:
    skills_dir = repo_root / "skills"
    if not skills_dir.exists():
        return ["未找到 skills 目录"]
    errors: list[str] = []
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir():
            errors.extend(validate_skill_structure(d))
    return errors


# ── 场景校验：examples/ 目录 ───────────────────────────────────

EXAMPLE_HEADINGS = ["# 场景：", "## 场景描述", "## 推荐 skill 流程", "## 应得到的最小产物"]


def run_example_checks(repo_root: Path) -> list[str]:
    examples_dir = repo_root / "examples"
    if not examples_dir.exists():
        return ["未找到 examples 目录"]
    errors: list[str] = []
    for f in sorted(examples_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        for heading in EXAMPLE_HEADINGS:
            if heading not in text:
                errors.append(f"{f.name}: 缺少段落 {heading}")
    return errors
