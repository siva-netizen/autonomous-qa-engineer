# QA Engineer TUI — Requirements

## Scope

Provide an interactive terminal UI for conversing with a software quality engineer persona and for explicitly invoking specialized agents. The TUI is the primary human-facing entry point; the JSON CLI runner remains available for automation.

## Requirements

- **REQ-TUI-001:** The TUI MUST run via `python -m agents.tui` and use the Textual library for layout, input, and rendering.
- **REQ-TUI-002:** The UI MUST use a green-themed stylesheet for screen, header, footer, chat, and input surfaces.
- **REQ-TUI-003:** The TUI MUST load project `.env` values when corresponding variables are not already exported in the shell.
- **REQ-TUI-004:** Free-form user messages MUST use a multi-turn software quality engineer system prompt aligned with ShopDemo QA, evidence rules, and traceability conventions.
- **REQ-TUI-005:** While waiting on Gemini or an agent, the TUI MUST show an animated loading indicator and rotating activity phases (tools/agents/reasoning labels).
- **REQ-TUI-006:** The TUI MUST support `/agents` to list roles and `/agent <role> <prompt>` (or `/agents <role> <prompt>`) to invoke one registered specialized agent. Lines starting with `/` MUST be treated as commands, not chat input.
- **REQ-TUI-011:** Assistant and agent replies MUST render markdown in the chat log (headings, lists, code fences) rather than raw markdown text.
- **REQ-TUI-007:** The TUI MUST support `/help`, `/clear`, and `/quit` without exposing credentials in the chat log.
- **REQ-TUI-008:** Missing `GEMINI_API_KEY` MUST fail before the UI starts, with actionable stderr guidance.
- **REQ-TUI-009:** Tests MUST cover chat session history, orchestrator parsing/phases, and `.env` loading without live provider access.
- **REQ-TUI-010:** The TUI MUST NOT fabricate browser execution, PASS/FAIL claims, or evidence paths.

## Acceptance criteria

1. `uv run --no-sync python -m agents.tui` starts when a local Gemini key is configured.
2. Chat and `/agent` commands show animated activity phases during blocking work.
3. Invalid `/agent` roles produce safe in-UI errors.
4. Unit tests pass with fake reasoning clients only.
5. README documents the TUI as the primary interactive entry point.
