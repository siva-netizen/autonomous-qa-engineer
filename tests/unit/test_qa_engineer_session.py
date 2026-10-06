from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest

from agents.qa_engineer import QA_ENGINEER_SYSTEM_PROMPT, QualityEngineerSession
from services.gemini_client import ChatCompletion, ChatMessage
from services.local_env import load_project_dotenv


class EchoClient:
    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
    ) -> ChatCompletion:
        assert messages[0].content == QA_ENGINEER_SYSTEM_PROMPT
        assert messages[-1].role == "user"
        return ChatCompletion(
            content=f"echo:{messages[-1].content}",
            model=model or "fake",
            usage={},
        )


def test_session_keeps_system_prompt_and_history() -> None:
    session = QualityEngineerSession(EchoClient())
    first = session.respond("Review checkout")
    second = session.respond("List test gaps")

    assert first == "echo:Review checkout"
    assert second == "echo:List test gaps"
    assert session.messages[0].role == "system"
    assert session.messages[-1].role == "assistant"
    assert len(session.messages) == 1 + 2 * 2  # system + two user/assistant pairs


def test_clear_resets_conversation() -> None:
    session = QualityEngineerSession(EchoClient())
    session.respond("hello")
    session.clear()

    assert len(session.messages) == 1
    assert session.messages[0].role == "system"


def test_empty_user_message_is_rejected() -> None:
    session = QualityEngineerSession(EchoClient())
    with pytest.raises(ValueError, match="empty"):
        session.respond("   ")


def test_load_project_dotenv_does_not_override(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import os

    root = tmp_path
    env_file = root / ".env"
    env_file.write_text("LOADED_FROM_FILE=1\nNEW_ONLY=1\n", encoding="utf-8")
    monkeypatch.chdir(root)
    monkeypatch.setenv("LOADED_FROM_FILE", "from-shell")

    load_project_dotenv(root)

    assert os.environ["LOADED_FROM_FILE"] == "from-shell"
    assert os.environ["NEW_ONLY"] == "1"
