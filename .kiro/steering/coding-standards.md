# Coding Standards

- Use Python 3.11+ and type annotations for public functions, dataclasses, protocols, and agent contracts.
- Keep modules small: agents reason, services perform provider I/O, MCP/browser adapters observe external state, and reports assemble evidence.
- Use stable traceability IDs such as `REQ-RA-001`, `REQ-TP-002`, `TC-001`, and preserve them in inputs/outputs.
- Raise typed, actionable errors with safe context; never include API keys, authorization headers, passwords, cookies, or full sensitive payloads in messages.
- Prefer synchronous deterministic code for validation and agent dispatch; run blocking provider calls off the Textual UI thread. Do not add a workflow engine for the MVP.
- Agent prompts must declare role, tools, input, output, evidence requirements, uncertainty behavior, and prohibited claims.
- Use dependency injection for transports so tests use fakes and live Gemini calls are opt-in.
- Playwright locators must come from target inspection; browser results require actual Playwright MCP execution.
