# Gemini Provider Migration — Requirements

## Scope

Replace the live reasoning provider boundary from Groq to Google's Gemini OpenAI-compatible API while preserving typed contracts, fake transport testing, explicit agent selection, structured outputs, and evidence rules. No API key is committed or written by the implementation.

## Requirements

- **REQ-GEM-001:** The reasoning adapter MUST use Gemini's OpenAI-compatible chat-completions endpoint at `https://generativelanguage.googleapis.com/v1beta/openai/` by default.
- **REQ-GEM-002:** The adapter MUST read `GEMINI_API_KEY`, `GEMINI_MODEL`, optional `GEMINI_FALLBACK_MODEL`, `GEMINI_BASE_URL`, and `GEMINI_TIMEOUT_SECONDS` from the environment.
- **REQ-GEM-003:** The default model MUST be configurable and default to the configured project default Gemini model `gemini-3.1-flash-lite`; no key may appear in source, tests, fixtures, or committed configuration.
- **REQ-GEM-004:** Gemini authentication MUST use the Bearer `GEMINI_API_KEY` header and provider errors MUST never expose the key or response body.
- **REQ-GEM-005:** The existing `ReasoningClient` protocol, structured output validation, fake transport tests, and selected-agent runtime MUST remain provider-independent.
- **REQ-GEM-006:** Missing Gemini credentials MUST be rejected before transport access. HTTP status errors MUST be reported safely with status code only.
- **REQ-GEM-007:** `.env.example`, README, MCP/provider docs, active steering, and executable agent imports MUST describe Gemini rather than Groq.
- **REQ-GEM-008:** A compatibility shim MAY remain for old imports, but production agent execution MUST use the Gemini adapter and Gemini environment variables.

## Acceptance criteria

1. Agent runner constructs `GeminiChatClient` from `GEMINI_*` environment variables.
2. Fake transport tests prove Gemini URL, model, Bearer header, fallback behavior, and missing-key rejection.
3. No provider secret is added; the local `.env` requires manual entry of the user's Gemini key.
4. Existing Python, TypeScript, scaffold, security, and real ShopDemo browser checks remain green.
