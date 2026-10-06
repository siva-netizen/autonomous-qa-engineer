from __future__ import annotations

import json
from typing import Any

from agents.run import main
from services.gemini_client import (
    ChatCompletion,
    ChatMessage,
    GeminiChatClient,
    GeminiConfig,
    GeminiRequestError,
)
from tests.support.fake_gemini import FakeGeminiClient


FakeClient = FakeGeminiClient


def cli_args(*extra: str) -> list[str]:
    return [
        "--agents",
        "requirement-analyzer,qa-reviewer",
        "--request-id",
        "REQ-RUN-TEST-001",
        "--prompt",
        "Review this explicit requirement.",
        "--requirement-ids",
        "REQ-RUN-001",
        "--context-json",
        '{"source":"test"}',
        *extra,
    ]


def test_cli_serializes_explicit_multi_agent_results(capsys: Any) -> None:
    exit_code = main(cli_args(), client=FakeClient())

    captured = capsys.readouterr()
    assert exit_code == 0
    document = json.loads(captured.out)
    assert document["selected_agents"] == ["requirement-analyzer", "qa-reviewer"]
    assert set(document["results"]) == {"requirement-analyzer", "qa-reviewer"}
    assert document["results"]["qa-reviewer"]["output"]["lifecycle"] == "generated"
    assert captured.err == ""


def test_cli_rejects_duplicate_roles_without_provider_call(capsys: Any) -> None:
    exit_code = main(
        [
            "--agents",
            "requirement-analyzer,requirement-analyzer",
            "--request-id",
            "REQ-RUN-TEST-002",
            "--prompt",
            "prompt",
        ],
        client=FakeClient(),
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "duplicate" in captured.err
    assert captured.out == ""


def test_cli_rejects_malformed_context(capsys: Any) -> None:
    exit_code = main(
        cli_args("--context-json", "[]"),
        client=FakeClient(),
    )

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "JSON object" in captured.err
    assert captured.out == ""


def test_cli_rejects_missing_key_before_transport(capsys: Any) -> None:
    class NeverCalledTransport:
        def send(self, **kwargs: Any) -> dict[str, Any]:
            raise AssertionError("transport must not be called")

    client = GeminiChatClient(GeminiConfig(api_key=None), NeverCalledTransport())
    exit_code = main(cli_args(), client=client)

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "GEMINI_API_KEY" in captured.err
    assert captured.out == ""


def test_cli_reports_provider_http_error_without_traceback(capsys: Any) -> None:
    class ForbiddenClient:
        def complete(
            self,
            messages: Sequence[ChatMessage],
            *,
            model: str | None = None,
        ) -> ChatCompletion:
            raise GeminiRequestError("Gemini request failed with HTTP 403")

    exit_code = main(cli_args(), client=ForbiddenClient())

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "GeminiRequestError" in captured.err
    assert "HTTP 403" in captured.err
    assert "Traceback" not in captured.err
    assert captured.out == ""
