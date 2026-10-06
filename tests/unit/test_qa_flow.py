from __future__ import annotations

from agents.qa_flow import run_qa_flow
from agents.registry import AgentRegistry
from tests.support.fake_gemini import FakeGeminiClient


def test_qa_flow_runs_three_agents_in_order() -> None:
    registry = AgentRegistry.from_client(FakeGeminiClient())
    results = run_qa_flow(registry, "ShopDemo checkout happy path")

    assert len(results) == 3
    assert [item.role.value for item in results] == [
        "requirement-analyzer",
        "test-planner",
        "playwright-engineer",
    ]
