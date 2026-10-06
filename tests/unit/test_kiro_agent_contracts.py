from __future__ import annotations

from agents.contracts import AgentRole
from agents.kiro_contracts import (
    agent_contract_path,
    load_kiro_agent_prompt,
    validate_agent_contract_markdown,
)
from agents.specialized import AGENT_CLASSES
from services.gemini_client import ChatCompletion, ChatMessage


class _StubClient:
    def complete(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion(content="{}", model="fake", usage={})


def test_each_kiro_agent_markdown_has_required_sections() -> None:
    for role in AgentRole:
        content = agent_contract_path(role).read_text(encoding="utf-8")
        missing = validate_agent_contract_markdown(content, role)
        assert missing == [], f"{role}: missing {missing}"


def test_runtime_system_prompt_loads_from_kiro_markdown() -> None:
    for role, agent_cls in AGENT_CLASSES.items():
        expected = load_kiro_agent_prompt(role)
        spec = agent_cls(_StubClient()).spec
        assert spec.system_prompt == expected
        assert "## Structured output" in spec.system_prompt
        assert ".kiro/steering/product.md" in spec.system_prompt
