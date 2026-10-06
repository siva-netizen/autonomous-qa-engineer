# QA Engineer TUI — Tasks

- [x] Add `QualityEngineerSession` and QA engineer system prompt.
- [x] Add Textual app with green theme, chat log, input, and activity rail.
- [x] Add animated loading phases for chat and `/agent` invocations.
- [x] Add `QATUIOrchestrator`, agent result formatting, and `/agent` parsing.
- [x] Add `services/local_env.py` for optional `.env` loading at TUI startup.
- [x] Add unit tests for session, orchestrator, and dotenv behavior.
- [x] Document TUI usage in README as the primary interactive entry point.

## Traceability

- REQ-TUI-001/002/007 → Textual app, theme CSS, slash commands.
- REQ-TUI-003/008 → `local_env.py` and pre-flight Gemini configuration checks.
- REQ-TUI-004 → `qa_engineer.py` session and system prompt.
- REQ-TUI-005/006 → `ActivityRail`, `animate_phases_while`, `/agent` dispatch.
- REQ-TUI-009 → unit tests under `tests/unit/`.
- REQ-TUI-010 → prompt/orchestrator constraints; no browser simulation in TUI.

## Follow-up (optional)

- Wire Playwright MCP actions from TUI commands (out of MVP scope).
- Add requirement ID flags to `/agent` parsing.

## Note on parallel dispatch

Concurrent multi-agent dispatch was removed from `agents/runtime.py` and `agents/run.py` to reduce provider overload. Sequential multi-agent invocation and TUI `/agent` calls remain supported.
