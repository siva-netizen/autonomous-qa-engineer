# Architecture

The product uses a group of specialized agents, not one giant agent and not a mandatory workflow:

```text
Human ──► agents.tui (QA chat + /agent) ──► Gemini adapter
Automation ──► agents.run (JSON) ──► Agent Registry
                              ├─ Requirement Analyzer
                              ├─ Test Planner
                              ├─ Playwright Engineer ── Playwright MCP ── Browser
                              ├─ Failure Analyzer
                              └─ QA Reviewer
```

Selected agents run independently in caller-supplied order. A caller may pass prior artifacts to any agent, but no runtime rule forces Analyzer → Planner → Engineer ordering. Concurrent parallel dispatch is not part of the MVP runtime.

Each agent has a typed input/output contract and a Kiro prompt contract. The agent calls the Gemini reasoning adapter only for interpretation/review. The adapter is configured through `GEMINI_*` environment variables and can be replaced by a fake transport in tests.

Browser navigation, DOM inspection, actions, screenshots, traces, console logs, and network evidence belong to Playwright MCP. Agents cannot manufacture browser results. Reports preserve lifecycle state and evidence references, and a QA Reviewer can downgrade unsupported claims to unknown.

GitHub access, when enabled later, is read-only context or explicit defect/test issue creation through a separate scoped integration. It is not part of agent reasoning by default.
