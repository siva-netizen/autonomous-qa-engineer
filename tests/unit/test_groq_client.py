from __future__ import annotations

from typing import Any, Mapping
from unittest.mock import patch
from urllib.error import HTTPError

import pytest

from services.gemini_client import (
    ChatMessage,
    GeminiChatClient,
    GeminiConfigurationError,
    GeminiConfig,
    GeminiRequestError,
    UrllibChatTransport,
)


class FakeTransport:
    def __init__(self, responses: list[Mapping[str, Any] | Exception]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    def send(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        self.calls.append(
            {
                "url": url,
                "headers": dict(headers),
                "payload": dict(payload),
                "timeout": timeout_seconds,
            }
        )
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response

    def send_stream(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout_seconds: float,
        on_delta: Any,
    ) -> Mapping[str, Any]:
        response = self.send(
            url=url,
            headers=headers,
            payload=payload,
            timeout_seconds=timeout_seconds,
        )
        content = response["choices"][0]["message"]["content"]
        if isinstance(content, str) and content:
            on_delta(content)
        return response


def success(content: str = "ok") -> Mapping[str, Any]:
    return {"choices": [{"message": {"content": content}}], "usage": {"total_tokens": 3}}


def test_defaults_use_gemini_model_and_endpoint() -> None:
    config = GeminiConfig.from_env({"GEMINI_API_KEY": "local-test-key"})
    assert config.model == "gemini-3.1-flash-lite"
    assert config.fallback_model is None
    assert config.base_url == "https://generativelanguage.googleapis.com/v1beta/openai"
    assert config.timeout_seconds == 60


def test_missing_key_is_rejected_before_transport() -> None:
    transport = FakeTransport([success()])
    client = GeminiChatClient(GeminiConfig(api_key=None), transport)

    with pytest.raises(GeminiConfigurationError, match="GEMINI_API_KEY"):
        client.complete([ChatMessage("user", "hello")])

    assert transport.calls == []


def test_fake_transport_receives_gemini_url_and_bearer_key() -> None:
    transport = FakeTransport([success("structured response")])
    client = GeminiChatClient(GeminiConfig(api_key="local-test-key"), transport)

    result = client.complete([ChatMessage("user", "requirement text")])

    assert result.content == "structured response"
    assert transport.calls[0]["url"] == (
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    )
    assert transport.calls[0]["payload"]["model"] == "gemini-3.1-flash-lite"
    assert transport.calls[0]["headers"]["Authorization"] == "Bearer local-test-key"


def test_request_error_uses_configured_gemini_fallback_model() -> None:
    transport = FakeTransport([GeminiRequestError("temporary provider failure"), success("fallback")])
    config = GeminiConfig(api_key="local-test-key", fallback_model="gemini-2.5-flash")
    client = GeminiChatClient(config, transport)

    result = client.complete([ChatMessage("user", "requirement text")])

    assert result.model == "gemini-2.5-flash"
    assert [call["payload"]["model"] for call in transport.calls] == [
        "gemini-3.1-flash-lite",
        "gemini-2.5-flash",
    ]


def test_http_forbidden_error_includes_status_without_response_body() -> None:
    error = HTTPError(
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        403,
        "Forbidden",
        hdrs=None,
        fp=None,
    )

    with patch("services.gemini_client.urlopen", side_effect=error):
        with pytest.raises(GeminiRequestError, match="HTTP 403") as raised:
            UrllibChatTransport().send(
                url="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                headers={"Authorization": "Bearer redacted-in-test"},
                payload={"model": "test-model"},
                timeout_seconds=1,
            )

    assert "Forbidden" not in str(raised.value)
    assert "redacted-in-test" not in str(raised.value)
