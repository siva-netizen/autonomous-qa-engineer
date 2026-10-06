from __future__ import annotations

from agents.contracts import AgentTool
from agents.specialized import RequirementAnalyzer
from agents.tui_orchestrator import activity_phases_for_agent
from services.gemini_client import ChatCompletion, ChatMessage


class StubClient:
    def complete(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion(content="{}", model="fake", usage={})


def test_activity_phases_include_agent_tools() -> None:
    spec = RequirementAnalyzer(StubClient()).spec
    phases = activity_phases_for_agent(spec)

    assert phases[0] == f"Agent · {spec.name}"
    assert "Tool · gemini-reasoning" in phases
    assert "Tool · file-tools" in phases
    assert phases[-1] == "Structured output validation"
    assert AgentTool.GEMINI.value in phases[1]
