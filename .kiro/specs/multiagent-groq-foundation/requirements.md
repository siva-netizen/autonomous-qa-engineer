# Multi-Agent Groq Foundation — Requirements

## Scope

Introduce a Python 3.11+ multi-agent foundation in which the five specialized QA agents are independently addressable, use explicit contracts, and can call a Groq-compatible reasoning adapter through environment configuration. This feature does not implement a fixed workflow or claim browser execution by itself.

## Requirements

- **REQ-MA-001:** Each required agent—Requirement Analyzer, Test Planner, Playwright Engineer, Failure Analyzer, and QA Reviewer—MUST be independently invokable through a common typed agent contract.
- **REQ-MA-002:** Each agent MUST declare its role, accepted input shape, output shape, available tools, evidence requirements, and prohibited claims.
- **REQ-MA-003:** The reasoning adapter MUST read the API key, primary model, optional fallback model, endpoint, and timeout from environment variables; no credential may appear in source, tests, fixtures, or committed configuration.
- **REQ-MA-004:** The default primary Groq model MUST be `llama-3.3-70b-versatile`; `openai/gpt-oss-120b` MAY be configured as a fallback through environment variables without hardcoding a secret.
- **REQ-MA-005:** The runtime MUST support selecting one agent or invoking multiple selected agents independently in caller order. It MUST NOT encode a mandatory linear workflow or hide agent decisions inside one giant agent. (Historical note: parallel dispatch was later removed from the MVP runtime.)
- **REQ-MA-006:** Agents MUST be testable with a deterministic fake transport so unit and integration tests do not require a live Groq key.
- **REQ-MA-007:** Playwright MCP MUST remain the declared browser-interaction boundary for navigation, DOM inspection, user actions, screenshots, and console/network evidence. The agent foundation MUST NOT simulate browser results.
- **REQ-MA-008:** All agent outputs MUST preserve requirement/scenario identifiers and lifecycle/evidence constraints needed for later traceability.
- **REQ-MA-009:** The Python implementation MUST use type hints, small modules, explicit error handling, and no secret-bearing logs.
- **REQ-MA-010:** The Kiro agent contracts under `.kiro/agents/` MUST stay aligned with the executable Python agent specifications.

## Acceptance criteria

1. `agents/` exposes five independent typed agents and a registry/runtime that can invoke a selected subset without a fixed sequence.
2. A Groq client can be constructed from environment configuration and rejects missing credentials before making a request.
3. Tests prove model/config handling, independent dispatch, fake-transport operation, empty input handling, and secret scanning.
4. `.env.example`, MCP documentation, steering, and the feature design explain the setup without containing the user-provided key.
5. No test or report marks browser behavior as passed without a real Playwright/MCP execution record.
