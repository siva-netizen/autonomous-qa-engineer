# MCP and provider notes

## Playwright MCP

Playwright MCP is the browser capability boundary for navigation, DOM inspection, user actions, screenshots, and console/network evidence. It is configured in `.kiro/settings/mcp.json` with no credentials. The Playwright Engineer, Failure Analyzer, and QA Reviewer may declare this capability; no agent may fabricate browser results.

### Two runtimes

| Context | What uses MCP |
|--------|------------------|
| **Kiro / Cursor IDE** | `.kiro/settings/mcp.json` starts `@playwright/mcp` for the editor agent session |
| **Python TUI / CLI** (`python -m agents.tui`, `python -m agents.run`) | Uses `agents/tool_runner.py` + `services/playwright_mcp_client.py`: file reads, **stdio Playwright MCP** (`browser_navigate`, `browser_snapshot`), writes `tests/e2e/generated/*.spec.ts`. Default TUI input runs the multi-agent `/flow`. |

Use `/flow <goal>` in the TUI to run **requirement-analyzer → test-planner → playwright-engineer** with shared context and automatic test file write after the engineer step.

Use only the local target:

```text
PLAYWRIGHT_BASE_URL=http://localhost:3000
SHOPDEMO_BASE_URL=http://localhost:3000
```

**Important:** `.kiro/settings/mcp.json` must use a **literal** URL for `PLAYWRIGHT_BASE_URL`. Kiro/Cursor does **not** expand `${SHOPDEMO_BASE_URL}` from `.env` inside that file — a placeholder leaves MCP pointing at an invalid base and causes navigation failures (including HTTP 503 from a bad gateway or proxy).

### Troubleshooting HTTP 503

| Where you see 503 | Likely cause | Fix |
|-------------------|--------------|-----|
| **Kiro/Cursor Playwright MCP** | ShopDemo not running, wrong `PLAYWRIGHT_BASE_URL`, or MCP server could not reach the app | Run `python scripts/diagnose_mcp.py`. Start ShopDemo on port 3000 until `/` returns **200**. Restart MCP in the IDE. |
| **TUI “Provider error … HTTP 503”** | Google Gemini temporary overload (not Playwright MCP) | Retry; set `GEMINI_FALLBACK_MODEL=gemini-2.0-flash` in `.env`; use shorter prompts (`/agent` one role vs huge chat). |
| **Python `/flow` preflight** | Same as ShopDemo down / 503 on localhost | Fix target first; MCP preflight only checks URL — it does not replace a running app. |

```bash
python scripts/diagnose_mcp.py
```

## Gemini

The independent agents use Google's OpenAI-compatible Gemini chat endpoint through `services/gemini_client.py`:

```text
GEMINI_API_KEY=       # local .env only; never commit or paste into chat
GEMINI_MODEL=gemini-3.1-flash-lite
GEMINI_FALLBACK_MODEL=
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
GEMINI_TIMEOUT_SECONDS=60
```

Requests use `Authorization: Bearer $GEMINI_API_KEY` and append `/chat/completions` to the base URL. Offline tests use a fake transport. Live provider validation is opt-in and requires a local Gemini key. Keys are never logged or placed in prompts, MCP settings, source, or reports.

## GitHub

GitHub CLI authentication is separate from Gemini. The repository's local Git author is `siva-netizen <sivasabarivel008@gmail.com>`, but switching the active `gh` account requires authenticating that GitHub account with `gh auth login`; the provider key cannot perform that action. GitHub MCP is not enabled in the MVP.
