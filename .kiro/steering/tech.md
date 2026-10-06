# Technology Context

## Selected baseline

- Runtime: Python 3.11+ with type hints
- Agent implementation: small independent typed agent classes; no mandatory workflow engine
- LLM provider: Google Gemini OpenAI-compatible chat endpoint through `services/gemini_client.py`
- Primary model: configurable `GEMINI_MODEL`, default `gemini-3.1-flash-lite`
- Optional fallback: configurable `GEMINI_FALLBACK_MODEL`
- Browser execution: Playwright MCP as the browser capability boundary
- Target: local ShopDemo (`ettaverse/dummy-ecommerce`), Next.js/MSW
- Artifact storage: local filesystem under ignored `artifacts/`
- Tests: pytest for Python agents/services, Playwright Test for the inspected target
- Interactive UI: Textual TUI (`python -m agents.tui`) with green theme and activity indicators; declared in `requirements-dev.txt`
- Build/lint baseline: Python compile/type-oriented checks plus existing npm checks for the browser test package

## Technology rules

The Python multi-agent runtime is primary for agent reasoning and contracts. TypeScript remains only for the existing inspected ShopDemo browser test and scaffold compatibility until the execution adapter is migrated. Deterministic code handles IDs, validation, dispatch, evidence references, and report assembly. Gemini is used only where language reasoning adds value.

No provider key is stored in source control. Unit tests inject a fake transport and never require network access.
