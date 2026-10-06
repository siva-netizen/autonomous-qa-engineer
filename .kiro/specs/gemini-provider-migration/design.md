# Gemini Provider Migration — Design

## Provider boundary

Add `services/gemini_client.py` as the canonical OpenAI-compatible adapter. It retains the existing `ChatMessage`, `ChatCompletion`, `ChatTransport`, and `ReasoningClient` contracts while defining `GeminiConfig`, `GeminiChatClient`, `GeminiConfigurationError`, and `GeminiRequestError`.

The default endpoint is `https://generativelanguage.googleapis.com/v1beta/openai`; requests append `/chat/completions`, send `Authorization: Bearer <GEMINI_API_KEY>`, and use configurable `GEMINI_MODEL`.

## Agent integration

`agents/base.py`, the registry, specialized definitions, `agents/run.py`, and the TUI orchestrator import the Gemini adapter. Dispatch, structured JSON parsing, lifecycle/evidence validation, and explicit selected-agent semantics do not change.

A small `services/groq_client.py` compatibility shim may re-export Gemini contracts under deprecated Groq names so old external imports fail safely only at the provider naming layer; it is not used by production agent execution.

## Environment

`.env.example` uses `GEMINI_API_KEY`, `GEMINI_MODEL=gemini-3.1-flash-lite`, optional `GEMINI_FALLBACK_MODEL`, `GEMINI_BASE_URL`, and `GEMINI_TIMEOUT_SECONDS`. The actual key is entered locally by the user and is never read into tool output or committed files.

## Testing

Fake transport tests validate request URL, model, authorization header, fallback model, missing key, HTTP status sanitization, and response decoding. Existing structured-agent and runner tests remain provider-neutral. No live Gemini request is made during repository validation.
