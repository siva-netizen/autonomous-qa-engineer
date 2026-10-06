# Autonomous QA Engineer

An evidence-driven, multi-agent QA system that turns requirements into test scenarios, executable Playwright tests, observed browser results, failure analysis, and traceable QA reports.

## Architecture

```text
Structured Requirement
        │
        ├── Requirement Analyzer agent
        ├── Test Planner agent
        ├── Playwright Engineer agent ── Playwright MCP ── ShopDemo
        ├── Failure Analyzer agent
        └── QA Reviewer agent
                 │
                 ▼
        Evidence-backed QA report
```

These are independently invokable agents. The runtime accepts an explicit selected set and invokes them in argument order; it does not force a hidden linear workflow.

## Current implementation

- Python 3.11+ typed multi-agent foundation under `agents/`, `services/`, `playwright/`, `mcp/`, and `reports/`.
- Gemini OpenAI-compatible reasoning adapter configured only through environment variables.
- Kiro requirements/design/tasks exist under `.kiro/specs/` before implementation.
- Playwright MCP is the browser interaction boundary; generated code alone never becomes execution evidence.
- ShopDemo is checked out under ignored `shopdemo/` and the first inspected Playwright test is in `tests/e2e/shopdemo-baseline.spec.ts`.

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
python -m pytest -q
npm install
npm run validate:scaffold
npm run typecheck
npm run test:e2e -- --project=chromium
```

## QA engineer TUI

Interactive terminal chat with a software quality engineer persona (requirements, test design, Playwright evidence, ShopDemo QA). Put `GEMINI_API_KEY` in `.env`; the TUI loads it automatically when the variable is not already exported.

```bash
python -m pip install -r requirements-dev.txt
python -m agents.tui
```

With `uv` (dev deps are in `pyproject.toml` → install with sync, not `--no-sync` alone):

```bash
uv sync
uv run python -m agents.tui
```

Green-themed Textual UI with animated loading while Gemini or specialized agents run.

Commands: `/help`, `/clear`, `/quit`, `/agent <role> <prompt>` (or Ctrl+Q).

## Structured agent runner (automation)

For scripted JSON output with explicit specialized roles (`requirement-analyzer`, `qa-reviewer`, etc.):

```bash
uv run --no-sync python -m agents.run \
  --agents requirement-analyzer,qa-reviewer \
  --request-id REQ-RUN-001 \
  --prompt "Review the ShopDemo checkout requirement." \
  --requirement-ids REQ-RA-001
```

Never commit `.env`. Offline tests use a fake transport and do not require a provider key.


## Kiro-first development

- Steering: `.kiro/steering/`
- Feature specs: `.kiro/specs/`
- Agent contracts: `.kiro/agents/`
- Reusable Skills: `.kiro/skills/`
- Hooks: `.kiro/hooks/` (includes `agent-on-spec-change.json` to invoke Requirement Analyzer on spec edits)
- Property-based testing (IDE): `.kiro/specs/agent-output-contracts/correctness.md` and `pytest tests/unit/test_agent_output_contracts_pbt.py -m property`
- Runtime agent prompts: loaded from `.kiro/agents/*.md` via `agents/kiro_contracts.py`

Interactive TUI (`python -m agents.tui`): free-form QA chat, `/agent <role> <prompt>` with real file/MCP-preflight tools, and `/flow <goal>` for analyzer → planner → playwright-engineer (writes `tests/e2e/generated/*.spec.ts`). IDE Playwright MCP is configured in `.kiro/settings/mcp.json`; see `docs/MCP.md` for IDE vs Python behavior.
- MCP settings: `.kiro/settings/mcp.json`
- Implementation plan and target inspection: `docs/IMPLEMENTATION_PLAN.md`, `docs/SHOPDEMO_INSPECTION.md`, and `docs/MCP.md`

## Evidence policy

A generated test is not an executed test. Reports distinguish `generated`, `executed`, and `verified`, preserve evidence paths, and classify uncertain failures as uncertain. A pass requires a real Playwright/MCP execution record.

## GitHub identity

The local Git author is configured as `siva-netizen <sivasabarivel008@gmail.com>`. GitHub CLI account authentication is separate and requires an interactive login for the `siva-netizen` account; no provider key is used for that login.
