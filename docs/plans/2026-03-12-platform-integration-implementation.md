# Platform Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a superpowers-style multi-platform integration layer for this repository, including OpenCode plugin bootstrap, command entrypoints, and unified installation documentation.

**Architecture:** Keep skills platform-neutral, add a thin OpenCode plugin that injects the bootstrap skill, add command compatibility files at repo root, and normalize repository documentation around Claude Code, Codex, and OpenCode. Verification stays lightweight and repository-local.

**Tech Stack:** Markdown, JavaScript (ESM), Python unittest, existing `scripts/skill_eval.py`

---

### Task 1: Add failing integration structure tests

**Files:**
- Create: `tests/test_platform_integration.py`

**Step 1: Write the failing test**

Create tests that assert:

- `.opencode/plugins/software-development-lifecycle-skills-cn.js` exists
- `commands/brainstorm.md`, `commands/write-plan.md`, `commands/execute-plan.md` exist
- `.opencode/INSTALL.md`, `docs/README.opencode.md`, and `README.md` mention OpenCode plugin installation
- plugin file references `生命周期总控`

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: FAIL because files or text do not exist yet.

**Step 3: Write minimal implementation**

Add the missing plugin, command files, and doc updates required by the tests.

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: PASS

### Task 2: Implement OpenCode plugin bootstrap layer

**Files:**
- Create: `.opencode/plugins/software-development-lifecycle-skills-cn.js`
- Modify: `.opencode/INSTALL.md`
- Modify: `docs/README.opencode.md`

**Step 1: Write the failing test**

Add assertions for plugin export shape markers and OpenCode installation instructions covering both `plugins/` and `skills/` symlinks.

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: FAIL on missing plugin-specific strings.

**Step 3: Write minimal implementation**

Implement a dependency-free ESM plugin that:

- reads `skills/生命周期总控/SKILL.md`
- strips frontmatter
- injects bootstrap text via `experimental.chat.system.transform`
- documents installation for macOS/Linux and Windows

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: PASS

### Task 3: Add command compatibility entrypoints

**Files:**
- Create: `commands/brainstorm.md`
- Create: `commands/write-plan.md`
- Create: `commands/execute-plan.md`
- Modify: `README.md`

**Step 1: Write the failing test**

Add assertions that each command file exists and that README mentions the commands layer.

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: FAIL until command files and README changes exist.

**Step 3: Write minimal implementation**

Create command files that redirect users to the corresponding lifecycle skills, and update README with a dedicated commands section.

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: PASS

### Task 4: Normalize top-level documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/README.codex.md`
- Modify: `docs/README.claude.md`
- Modify: `docs/README.opencode.md`
- Modify: `.codex/INSTALL.md`
- Modify: `.opencode/INSTALL.md`

**Step 1: Write the failing test**

Add assertions for platform docs covering install, verify, update, and uninstall/troubleshooting structure where applicable.

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: FAIL on missing normalized sections.

**Step 3: Write minimal implementation**

Update docs to present three platforms consistently and explain command compatibility and bootstrap behavior.

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_platform_integration -v`
Expected: PASS

### Task 5: Verify plugin syntax and repository integrity

**Files:**
- No code changes expected unless verification reveals defects

**Step 1: Verify JavaScript syntax**

Run: `node --check .opencode/plugins/software-development-lifecycle-skills-cn.js`
Expected: no syntax errors

**Step 2: Verify repository checks**

Run: `PYTHONPATH=scripts python scripts/skill_eval.py check`
Expected: repository checks complete successfully

**Step 3: Review git diff**

Run: `git diff -- README.md docs/README.claude.md docs/README.codex.md docs/README.opencode.md .codex/INSTALL.md .opencode/INSTALL.md .opencode/plugins/software-development-lifecycle-skills-cn.js commands tests/test_platform_integration.py docs/plans`
Expected: only intended platform integration changes
