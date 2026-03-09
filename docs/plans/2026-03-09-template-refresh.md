# Template Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the requirement and technical design templates so they better support PRD/RFC-quality outputs without changing skill workflows.

**Architecture:** Keep the existing repository structure and skill contracts intact, and strengthen only the two template documents. The new templates should encode richer document structure, clearer decision prompts, and stronger separation between problem definition and solution design.

**Tech Stack:** Markdown, existing repository templates, repository documentation conventions.

---

### Task 1: Refresh requirement template

**Files:**
- Modify: `templates/需求说明模板.md`
- Reference: `README.md`
- Reference: `skills/需求澄清/SKILL.md`

**Step 1: Inspect current requirement template**

Run: `sed -n '1,200p' templates/需求说明模板.md`
Expected: A minimal outline with only top-level section names.

**Step 2: Replace with richer PRD-style structure**

Update the file to include:
- metadata
- positioning / problem definition
- non-goals
- target users and scenarios
- scope / constraints / dependencies
- functional and non-functional requirements
- acceptance criteria
- open questions / decisions

**Step 3: Review for repository fit**

Run: `sed -n '1,260p' templates/需求说明模板.md`
Expected: A repository-aligned template that stays generic and avoids implementation details.

### Task 2: Refresh technical design template

**Files:**
- Modify: `templates/技术方案模板.md`
- Reference: `README.md`
- Reference: `skills/技术方案/SKILL.md`

**Step 1: Inspect current technical design template**

Run: `sed -n '1,200p' templates/技术方案模板.md`
Expected: A minimal outline with only broad design headings.

**Step 2: Replace with richer RFC-style structure**

Update the file to include:
- metadata and summary
- background, goals, constraints
- candidate options and trade-offs
- recommended architecture and module boundaries
- data flow, API contract, error handling
- security / performance / compatibility
- phased rollout, risks, decisions, open items

**Step 3: Review for implementation neutrality**

Run: `sed -n '1,320p' templates/技术方案模板.md`
Expected: A template that guides strong technical decisions without turning into a task breakdown.

### Task 3: Verify change impact

**Files:**
- Modify: `docs/plans/2026-03-09-template-refresh.md`
- Verify: repository working tree

**Step 1: Run change verification**

Run: `python ~/.codex/skills/run_skill.py verify-change --mode working`
Expected: A report covering changed documentation files and impact assessment.

**Step 2: Review git diff**

Run: `git diff -- templates/需求说明模板.md templates/技术方案模板.md docs/plans/2026-03-09-template-refresh.md`
Expected: Only the planned documentation changes appear.
