"""Small Gemini OpenAI-compatible client with an injectable transport."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from services.stream_context import get_stream_callback


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini provider configuration is incomplete."""


class GeminiRequestError(RuntimeError):
    """Raised when Gemini cannot return a valid completion."""


@dataclass(frozen=True, slots=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True, slots=True)
class ChatCompletion:
    content: str
    model: str
    usage: Mapping[str, Any]


class ReasoningClient(Protocol):
    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
    ) -> ChatCompletion: ...


@dataclass(frozen=True, slots=True)
class GeminiConfig:
    api_key: str | None
    model: str = "gemini-3.1-flash-lite"
    fallback_model: str | None = None
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    timeout_seconds: float = 60.0

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "GeminiConfig":
        values = os.environ if environ is None else environ
        timeout_raw = values.get("GEMINI_TIMEOUT_SECONDS", "60").strip()
        try:
            timeout = float(timeout_raw)
        except ValueError as exc:
            raise GeminiConfigurationError("GEMINI_TIMEOUT_SECONDS must be numeric") from exc
        if timeout <= 0:
            raise GeminiConfigurationError("GEMINI_TIMEOUT_SECONDS must be greater than zero")

        fallback = values.get("GEMINI_FALLBACK_MODEL", "").strip()
        return cls(
            api_key=values.get("GEMINI_API_KEY", "").strip() or None,
            model=values.get("GEMINI_MODEL", "gemini-3.1-flash-lite").strip()
            or "gemini-3.1-flash-lite",
            fallback_model=fallback or None,
            base_url=values.get(
                "GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai",
            ).rstrip("/"),
            timeout_seconds=timeout,
        )


class ChatTransport(Protocol):
    def send(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout_seconds: float,
    ) -> Mapping[str, Any]: ...

    def send_stream(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout_seconds: float,
        on_delta: Callable[[str], None],
    ) -> Mapping[str, Any]: ...


_RETRYABLE_HTTP_CODES = frozenset({429, 500, 502, 503, 504})


class UrllibChatTransport:
    """Network transport kept separate so tests never need provider access."""

    def send(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=dict(headers),
            method="POST",
        )
        raw: str
        try:
            last_http_error: HTTPError | None = None
            for attempt in range(2):
                try:
                    with urlopen(request, timeout=timeout_seconds) as response:
                        raw = response.read().decode("utf-8")
                    break
                except HTTPError as exc:
                    last_http_error = exc
                    if exc.code in _RETRYABLE_HTTP_CODES and attempt == 0:
                        continue
                    raise GeminiRequestError(f"Gemini request failed with HTTP {exc.code}") from exc
            else:
                assert last_http_error is not None
                raise GeminiRequestError(
                    f"Gemini request failed with HTTP {last_http_error.code}"
                ) from last_http_error
        except (URLError, TimeoutError) as exc:
            raise GeminiRequestError(f"Gemini request failed: {type(exc).__name__}") from exc
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GeminiRequestError("Gemini returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise GeminiRequestError("Gemini returned an invalid response shape")
        return decoded

    def send_stream(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout_seconds: float,
        on_delta: Callable[[str], None],
    ) -> Mapping[str, Any]:
        stream_payload = {**payload, "stream": True}
        request = Request(
            url,
            data=json.dumps(stream_payload).encode("utf-8"),
            headers=dict(headers),
            method="POST",
        )
        content_parts: list[str] = []
        model_name = str(payload.get("model", ""))
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                while True:
                    raw_line = response.readline()
                    if not raw_line:
                        break
                    line = raw_line.decode("utf-8").strip()
                    if not line or line == "data: [DONE]":
                        continue
                    if not line.startswith("data: "):
                        continue
                    try:
                        event = json.loads(line[6:])
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(event, dict):
                        continue
                    for choice in event.get("choices", []):
                        if not isinstance(choice, dict):
                            continue
                        delta = choice.get("delta", {})
                        if isinstance(delta, dict):
                            piece = delta.get("content")
                            if isinstance(piece, str) and piece:
                                content_parts.append(piece)
                                on_delta(piece)
                        message = choice.get("message", {})
                        if isinstance(message, dict):
                            piece = message.get("content")
                            if isinstance(piece, str) and piece:
                                content_parts.append(piece)
                                on_delta(piece)
                    if isinstance(event.get("model"), str):
                        model_name = event["model"]
        except HTTPError as exc:
            raise GeminiRequestError(f"Gemini request failed with HTTP {exc.code}") from exc
        except (URLError, TimeoutError) as exc:
            raise GeminiRequestError(f"Gemini request failed: {type(exc).__name__}") from exc

        content = "".join(content_parts)
        if not content.strip():
            raise GeminiRequestError("Gemini stream returned empty content")
        return {
            "choices": [{"message": {"content": content}}],
            "usage": {},
            "model": model_name,
        }


class GeminiChatClient:
    """Call Gemini only when explicitly configured with a local environment key."""

    def __init__(
        self,
        config: GeminiConfig | None = None,
        transport: ChatTransport | None = None,
    ) -> None:
        self.config = config or GeminiConfig.from_env()
        self.transport = transport or UrllibChatTransport()

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
    ) -> ChatCompletion:
        if not messages:
            raise GeminiConfigurationError("at least one chat message is required")
        if not self.config.api_key:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured; set it in local .env before live calls"
            )

        selected = model or self.config.model
        models = [selected]
        if self.config.fallback_model and self.config.fallback_model != selected:
            models.append(self.config.fallback_model)

        last_error: GeminiRequestError | None = None
        for candidate in models:
            try:
                response = self._request(candidate, messages)
                return self._decode(response, candidate)
            except GeminiRequestError as exc:
                last_error = exc
        assert last_error is not None
        raise last_error

    def _request(
        self,
        model: str,
        messages: Sequence[ChatMessage],
    ) -> Mapping[str, Any]:
        payload = {
            "model": model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in messages
            ],
            "temperature": 0,
        }
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        timeout = self.config.timeout_seconds
        stream_cb = get_stream_callback()
        if stream_cb is not None and hasattr(self.transport, "send_stream"):
            return self.transport.send_stream(
                url=url,
                headers=headers,
                payload=payload,
                timeout_seconds=timeout,
                on_delta=stream_cb,
            )
        return self.transport.send(
            url=url,
            headers=headers,
            payload=payload,
            timeout_seconds=timeout,
        )

    @staticmethod
    def _decode(response: Mapping[str, Any], model: str) -> ChatCompletion:
        try:
            choice = response["choices"][0]
            message = choice["message"]
            content = message["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise GeminiRequestError("Gemini response did not contain a chat message") from exc
        if not isinstance(content, str) or not content.strip():
            raise GeminiRequestError("Gemini response contained empty content")
        usage = response.get("usage", {})
        return ChatCompletion(
            content=content,
            model=model,
            usage=usage if isinstance(usage, dict) else {},
        )
