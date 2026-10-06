# Repository Structure

```text
agents/
  contracts.py       typed requests/results/roles
  base.py            common independently invokable agent
  specialized.py     five role-specific agents
  registry.py        explicit agent lookup
  runtime.py         single-agent invoke boundary
  run.py             JSON CLI runner for automation
  qa_engineer.py     multi-turn QA engineer chat session
  tui.py             Textual TUI entry point
  tui_theme.py       green TUI stylesheet
  tui_widgets.py     activity/loading widgets
  tui_orchestrator.py chat and /agent orchestration
services/
  gemini_client.py   env-backed Gemini adapter and transport boundary
  groq_client.py     deprecated compatibility aliases only
  local_env.py       optional project .env loader
playwright/
  contracts.py       Playwright MCP/browser capability protocols
mcp/
  config.py          non-secret MCP configuration
reports/
  contracts.py       evidence and report types
scripts/
  security_scan.py   source/config secret scan
tests/
  unit/              deterministic Python unit tests
  integration/       fake transport and multi-agent tests
  e2e/               inspected ShopDemo Playwright tests
src/                 legacy scaffold contracts retained during migration
.kiro/               steering, specs, agents, skills, hooks, MCP settings
docs/                plans, target inspection, MCP notes, and evidence guidance
```

Agent reasoning never owns browser side effects. `services/` owns provider I/O, `mcp/` owns MCP configuration, `playwright/` owns browser capability contracts, and `reports/` owns evidence/report types. The runtime does not encode a fixed agent sequence. Human interaction starts in `agents/tui.py`; automation uses `agents/run.py`.
