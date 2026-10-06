# Independent Agent Runner — Requirements

## Scope

Provide a standard-library CLI for explicitly invoking one agent or a caller-selected set of agents in deterministic argument order. The CLI is an automation adapter over the existing runtime; it MUST NOT create a mandatory workflow or fabricate execution evidence. Interactive use is handled by `agents.tui` (see `.kiro/specs/qa-engineer-tui/`).

## Requirements

- **REQ-RUN-001:** The CLI MUST accept one or more explicit agent roles from the registered five roles.
- **REQ-RUN-002:** The CLI MUST invoke selected roles independently in deterministic `--agents` order (sequential dispatch only).
- **REQ-RUN-003:** The CLI MUST require a non-empty request ID and prompt and MUST preserve optional requirement IDs and JSON context.
- **REQ-RUN-004:** The CLI MUST construct Gemini configuration from environment variables and MUST reject missing `GEMINI_API_KEY` before network access.
- **REQ-RUN-005:** The CLI MUST emit machine-readable JSON results to stdout and diagnostics/errors to stderr without exposing credentials.
- **REQ-RUN-006:** Output MUST preserve each agent's validated structured output, lifecycle, evidence references, model, and safe metadata.
- **REQ-RUN-007:** Invalid roles, duplicate roles, malformed JSON options, missing values, and provider/configuration errors MUST produce a non-zero exit code and actionable stderr.
- **REQ-RUN-008:** Tests MUST inject a deterministic fake reasoning client and MUST NOT require a live provider key or network access.
- **REQ-RUN-009:** The CLI MUST remain an explicit dispatch adapter; it MUST NOT sequence Requirement Analyzer → Test Planner → Playwright Engineer automatically.

## Acceptance criteria

1. `python -m agents.run --help` documents explicit role selection and request options.
2. A fake-client smoke test serializes selected independent results as JSON.
3. Invalid selection and malformed option tests fail safely without provider calls.
4. The documented invocation uses `python -m agents.run` or `uv run python -m agents.run`, not `uv agents.run`.
5. Existing Python, TypeScript, security, scaffold, and browser baseline checks remain green.
