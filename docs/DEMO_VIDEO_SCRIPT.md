# Autonomous QA Engineer — 3-Minute Demo Script (Kiro 2026)

Target length: ~3 minutes at normal pace (~380–450 words).  
Format: narration with `[SHOW]`, `[RUN]`, `[TYPE]`, `[OPEN]`, `[CLICK]` cues.

---

[0:00–0:18] [SHOW: repo root + README.md]

This is **Autonomous QA Engineer**, my project for the Kiro 2026 University Challenge. QA teams spend hours turning requirements into tests, running browsers, and writing reports—and it’s easy to miss traceability or call a generated test “passed” without real evidence. I built an **agentic pipeline** that uses **Kiro steering, specs, hooks, skills, and custom agents**, plus **Playwright MCP**, to go from requirements to executable tests, execution evidence, and QA review.

[0:18–1:05] [SHOW: architecture diagram in README] [RUN: `uv sync && uv run python -m agents.tui`]

Here’s what the product does, concretely. **Input** is a user story or goal—like checkout on our ShopDemo app. [TYPE in TUI: `test the cart to billing path`] The **multi-agent flow** runs in sequence: the **requirement analyzer** structures obligations, the **test planner** emits traceable scenarios with `REQ-*` and `TC-*` IDs, and the **playwright engineer** generates Playwright code. [SHOW: `tests/e2e/generated/*.spec.ts`] Tool steps use **file tools** and **Playwright MCP**—navigate and snapshot the real app at localhost—not just LLM text. [RUN: `npm run test:e2e -- --project=chromium` — optional] Failures go to the **failure analyzer**; the **QA reviewer** checks coverage and evidence before anything is “verified.” Output is **structured JSON plus artifacts**—tests, traces, and a report mindset that separates **generated**, **executed**, and **verified**.

[1:05–2:15] [SHOW: `.kiro/` folder expanded]

This folder is the proof of **Kiro-first development**. [OPEN: `.kiro/steering/product.md`, `tech.md`, `testing.md`] **Steering** sets product boundaries, stack rules, and testing policy—agents must not invent PASS/FAIL without browser evidence. [OPEN: `.kiro/specs/requirement-analysis/` or `playwright-execution/` — `requirements.md`, `design.md`, `tasks.md`] **Specs** drive features before code: requirements, design, and tasks stay aligned with the Python runtime and TUI. [OPEN: `.kiro/agents/`] **Custom agents**—requirement-analyzer, test-planner, playwright-engineer, failure-analyzer, qa-reviewer—each with a single role, tool permissions, and contracts loaded at runtime from these markdown files. [OPEN: `.kiro/hooks/test-on-change.json`] **Hooks** automate quality: when agent or test code changes, pytest runs automatically; lint and security hooks keep the scaffold honest. [OPEN: `.kiro/settings/mcp.json`] **MCP** configures **Playwright** for IDE sessions—real browser automation for the engineer and reviewer roles. [OPEN: `.kiro/skills/playwright-testing/SKILL.md`, `failure-analysis/SKILL.md`] **Skills** hold reusable testing knowledge so agents reference one source instead of re-prompting everything. These artifacts show **spec-driven, Kiro-native** engineering—not a one-off chatbot.

[2:15–2:55] [SHOW: `agents/run.py` or TUI activity rail during a flow]

So what does Autonomous QA Engineer **do**? It turns requirements into **traceable scenarios, Playwright tests, MCP-backed browser context, and conservative failure review**—with evidence, not guesses. **What did Kiro enable?** Steering and specs kept five agents and a Python runtime consistent; custom agents encoded QA specialties; hooks removed manual “did we run tests?” steps; MCP gave **real browser capability** beyond reasoning; skills made Playwright and failure-analysis rules **portable and repeatable**. That’s hard to maintain in a single monolithic prompt.

[2:55–3:10] [SHOW: generated spec + `docs/MCP.md` or `python scripts/diagnose_mcp.py`]

**Status today:** MVP end-to-end flow works—TUI multi-agent run, test file generation, ShopDemo target, and structured agent outputs. **Next:** broader ShopDemo scenarios, richer MCP execution records, and stronger failure-to-requirement reporting. Details and setup are in the README—thanks for watching.
