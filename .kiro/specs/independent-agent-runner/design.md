# Independent Agent Runner — Design

## CLI boundary

`agents/run.py` uses `argparse` and standard-library JSON only. It parses comma-separated roles and request data, constructs `GeminiChatClient(GeminiConfig.from_env())`, builds `AgentRegistry`, and delegates to `MultiAgentRuntime`.

The helper `run_request(..., client=...)` accepts a `ReasoningClient` injection so tests can execute without credentials or network access. The production `main()` uses the environment-backed Gemini client.

## Arguments

- `--agents`: required comma-separated role values.
- `--request-id`: required request identifier.
- `--prompt`: required task prompt.
- `--requirement-ids`: optional comma-separated `REQ-*` IDs.
- `--context-json`: optional JSON object passed unchanged as caller context.

The CLI prints one JSON object containing the request ID, selected roles, and serialized `AgentResult` objects. It never prints authorization headers or provider keys.

## Dispatch semantics

The CLI invokes each selected role once, in `--agents` order, via `MultiAgentRuntime.invoke`. It does not insert a workflow or pass one agent's output implicitly to another. Parallel/concurrent dispatch is out of scope for the MVP runner.

## Error handling

Argument and context errors use argparse's non-zero exit path. Unknown/duplicate roles, provider configuration failures, structured-output failures, and runtime errors are reported to stderr with the exception type/message and return code 2. Raw provider content is not echoed in error diagnostics.

## Testing

Test argument parsing, role normalization, duplicate rejection, malformed context JSON, sequential multi-agent fake-client execution, structured result serialization, and missing-key rejection before transport access.
