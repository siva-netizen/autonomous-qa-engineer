# QA Engineer TUI — Design

## Modules

```text
agents/
  tui.py                 Textual application entry point
  tui_theme.py           green CSS theme
  tui_widgets.py         ActivityRail (LoadingIndicator + status text)
  tui_orchestrator.py    chat/agent dispatch and phase animation helper
  qa_engineer.py         multi-turn QA engineer session
services/
  local_env.py           load `.env` without overriding exported variables
```

## UI layout

- Header and footer use the green theme.
- `RichLog` displays user and assistant/agent messages with markup.
- `ActivityRail` docks above the input, hidden until work starts; Textual `LoadingIndicator` animates while phases rotate.
- Input is disabled while a turn is in progress.

## Interaction modes

1. **Chat:** `QATUIOrchestrator.respond_chat()` appends user/assistant messages to `QualityEngineerSession` and calls Gemini once per turn.
2. **Agent:** `/agent <role> <prompt>` builds an `AgentRequest`, runs the selected agent through `AgentRegistry`, and formats structured output as markdown-like text in the log.

Activity phases are cosmetic labels derived from chat defaults or the invoked agent's declared tools; they rotate on the UI thread while blocking work runs in `asyncio.to_thread`.

## Error handling

Configuration errors exit before app launch. Provider and validation errors are written to the chat log without stack traces or secret-bearing diagnostics.

## Testing

Unit-test session history, orchestrator command parsing, agent phase lists, and dotenv merge rules. Do not require Textual screen automation in CI for the MVP.
