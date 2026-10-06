# Multi-Agent Groq Foundation — Design

## Technology boundary

Use Python 3.11+ with the standard library for the initial runtime and `pytest` for tests. The Groq adapter uses the OpenAI-compatible HTTPS endpoint through a small transport boundary, so unit tests can inject a fake transport and no provider SDK is required yet.

## Modules

```text
agents/
  contracts.py       typed requests, results, roles, and tool declarations
  base.py            common independent agent implementation
  specialized.py     five role-specific prompt/spec definitions
  registry.py        explicit role lookup; no hidden sequence
  runtime.py         single-agent invoke boundary
services/
  groq_client.py     environment config and provider transport
playwright/
  contracts.py       browser/MCP capability protocol; no simulated pass
mcp/
  config.py          non-secret Playwright MCP configuration reader
reports/
  contracts.py       evidence/lifecycle report types
```

## Agent model

Each specialized agent owns a role prompt and validation policy. `Agent.run()` accepts one typed request and returns one typed result. The role definitions reference the corresponding `.kiro/agents/*.md` contract and Skill. The runtime accepts an explicit list of roles and uses independent dispatch; it does not implement Requirement Analyzer → Planner → Executor sequencing.

## Groq model configuration

Environment variables:

- `GROQ_API_KEY` — required secret, local `.env` only
- `GROQ_MODEL` — defaults to `llama-3.3-70b-versatile`
- `GROQ_FALLBACK_MODEL` — optional, defaults to `openai/gpt-oss-120b`
- `GROQ_BASE_URL` — defaults to `https://api.groq.com/openai/v1`
- `GROQ_TIMEOUT_SECONDS` — bounded request timeout

The client sends only the caller-provided agent messages to Groq and never logs the key or authorization header. Provider errors remain explicit and do not become QA results.

## MCP boundary

`playwright/` exposes a protocol for the later Playwright MCP adapter. Browser actions and evidence collection belong there; agents may declare the capability but cannot fabricate a browser result. The existing Kiro MCP configuration remains the operational server configuration and is documented separately.

## Security and testability

No live provider calls occur in unit tests. A fake chat transport returns deterministic JSON/text. Secret scanning examines tracked source/config paths and ignores `.env` values. The runtime rejects malformed role names and empty agent input with typed errors.
