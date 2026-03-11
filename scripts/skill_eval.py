#!/usr/bin/env python3
"""skill_eval: 统一评估 CLI。

子命令:
  check     对仓库执行全量校验（结构 + 场景 + 契约）
  output    校验某次 agent 产出是否满足输出契约
  compare   对比两份 agent 产出

用法:
  python scripts/skill_eval.py check [--repo .]
  python scripts/skill_eval.py output --skill 测试验证 --file path/to/output.md
  python scripts/skill_eval.py compare --skill 测试验证 --a a.md --b b.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from skill_eval_core import (
    CheckResult,
    load_contracts,
    run_example_checks,
    run_skill_output_check,
    run_skill_text_checks,
    run_structure_checks,
)


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_contracts_path(repo_root: Path) -> Path:
    return repo_root / "tests" / "contracts.json"


# ── check 子命令 ───────────────────────────────────────────────

def cmd_check(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    contracts_path = Path(args.contracts) if args.contracts else default_contracts_path(repo)

    all_ok = True
    summary: dict[str, object] = {}

    # 1. 结构校验
    struct_errors = run_structure_checks(repo)
    skills_dir = repo / "skills"
    skill_count = len([d for d in skills_dir.iterdir() if d.is_dir()]) if skills_dir.exists() else 0
    if struct_errors:
        all_ok = False
        summary["structure"] = {"ok": False, "errors": struct_errors}
        print("结构校验失败：")
        for e in struct_errors:
            print(f"  - {e}")
    else:
        summary["structure"] = {"ok": True, "count": skill_count}
        print(f"结构校验通过，共检查 {skill_count} 个 skill。")

    # 2. 场景校验
    example_errors = run_example_checks(repo)
    examples_dir = repo / "examples"
    example_count = len(list(examples_dir.glob("*.md"))) if examples_dir.exists() else 0
    if example_errors:
        all_ok = False
        summary["examples"] = {"ok": False, "errors": example_errors}
        print("场景校验失败：")
        for e in example_errors:
            print(f"  - {e}")
    else:
        summary["examples"] = {"ok": True, "count": example_count}
        print(f"场景校验通过，共检查 {example_count} 个示例。")

    # 3. 契约校验（skill_text）
    try:
        contracts = load_contracts(contracts_path)
    except Exception as exc:
        print(f"契约加载失败: {exc}")
        return 2

    text_results = run_skill_text_checks(contracts, repo)
    text_failures = [r for r in text_results if not r.ok]
    if text_failures:
        all_ok = False
        summary["contracts"] = {
            "ok": False,
            "total": len(text_results),
            "failures": [{
                "name": r.name,
                "missing": r.missing,
                "forbidden_hits": r.forbidden_hits,
            } for r in text_failures],
        }
        print("契约校验失败：")
        for r in text_failures:
            for m in r.missing:
                print(f"  - {r.name}: 缺少 {m}")
            for f in r.forbidden_hits:
                print(f"  - {r.name}: 命中禁止内容 {f}")
    else:
        summary["contracts"] = {"ok": True, "total": len(text_results)}
        print(f"契约校验通过，共检查 {len(text_results)} 条规则。")

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0 if all_ok else 1


# ── output 子命令 ──────────────────────────────────────────────

def cmd_output(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    contracts_path = Path(args.contracts) if args.contracts else default_contracts_path(repo)
    output_path = Path(args.file)

    if not output_path.exists():
        print(f"输出文件不存在: {args.file}")
        return 2

    try:
        contracts = load_contracts(contracts_path)
        result = run_skill_output_check(
            contracts, args.skill, output_path.read_text(encoding="utf-8"),
        )
    except Exception as exc:
        print(f"校验失败: {exc}")
        return 2

    if args.json:
        print(json.dumps({
            "skill": args.skill,
            "file": str(output_path),
            "ok": result.ok,
            "missing": result.missing,
            "forbidden_hits": result.forbidden_hits,
            "penalty": result.penalty,
        }, ensure_ascii=False, indent=2))
    elif result.ok:
        print("输出校验通过。")
    else:
        print("输出校验失败：")
        for m in result.missing:
            print(f"  - 缺少: {m}")
        for f in result.forbidden_hits:
            print(f"  - 命中禁止内容: {f}")

    return 0 if result.ok else 1


# ── compare 子命令 ─────────────────────────────────────────────

def cmd_compare(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    contracts_path = Path(args.contracts) if args.contracts else default_contracts_path(repo)
    path_a, path_b = Path(args.a), Path(args.b)

    if not path_a.exists() or not path_b.exists():
        print("输出文件不存在。")
        return 2

    try:
        contracts = load_contracts(contracts_path)
        ra = run_skill_output_check(contracts, args.skill, path_a.read_text(encoding="utf-8"))
        rb = run_skill_output_check(contracts, args.skill, path_b.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"评估失败: {exc}")
        return 2

    score_a = _load_score(args.score_a)
    score_b = _load_score(args.score_b)

    summary = {
        "skill": args.skill,
        "a": {"file": str(path_a), "ok": ra.ok, "penalty": ra.penalty,
              "missing": ra.missing, "forbidden_hits": ra.forbidden_hits, "score": score_a},
        "b": {"file": str(path_b), "ok": rb.ok, "penalty": rb.penalty,
              "missing": rb.missing, "forbidden_hits": rb.forbidden_hits, "score": score_b},
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print(f"Skill: {args.skill}")
    print(f"A penalty: {ra.penalty} | ok: {ra.ok}")
    print(f"B penalty: {rb.penalty} | ok: {rb.ok}")
    if ra.penalty < rb.penalty:
        winner = "A"
    elif rb.penalty < ra.penalty:
        winner = "B"
    else:
        winner = "平局（建议结合人工评分）"
    print(f"Contract winner: {winner}")
    return 0


def _load_score(path_str: str | None) -> dict[str, object] | None:
    if not path_str:
        return None
    return json.loads(Path(path_str).read_text(encoding="utf-8"))


# ── 参数解析 ───────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill_eval",
        description="统一评估工具：校验 skill 定义质量 + agent 产出质量",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    p_check = sub.add_parser("check", help="对仓库执行全量校验（结构 + 场景 + 契约）")
    p_check.add_argument("--repo", default=str(default_repo_root()), help="skill 仓库根目录")
    p_check.add_argument("--contracts", default=None, help="契约文件路径")
    p_check.add_argument("--json", action="store_true", help="追加 JSON 摘要")

    # output
    p_output = sub.add_parser("output", help="校验 agent 产出是否满足输出契约")
    p_output.add_argument("--skill", required=True, help="skill 名称")
    p_output.add_argument("--file", required=True, help="待校验的输出文件")
    p_output.add_argument("--repo", default=str(default_repo_root()), help="skill 仓库根目录")
    p_output.add_argument("--contracts", default=None, help="契约文件路径")
    p_output.add_argument("--json", action="store_true", help="JSON 输出")

    # compare
    p_compare = sub.add_parser("compare", help="对比两份 agent 产出")
    p_compare.add_argument("--skill", required=True, help="skill 名称")
    p_compare.add_argument("--a", required=True, help="输出 A")
    p_compare.add_argument("--b", required=True, help="输出 B")
    p_compare.add_argument("--repo", default=str(default_repo_root()), help="skill 仓库根目录")
    p_compare.add_argument("--contracts", default=None, help="契约文件路径")
    p_compare.add_argument("--score-a", default=None, help="A 的人工评分 JSON")
    p_compare.add_argument("--score-b", default=None, help="B 的人工评分 JSON")
    p_compare.add_argument("--json", action="store_true", help="JSON 输出")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "check": cmd_check,
        "output": cmd_output,
        "compare": cmd_compare,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
