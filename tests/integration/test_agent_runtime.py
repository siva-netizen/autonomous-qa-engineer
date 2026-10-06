from __future__ import annotations

import pytest

from agents.contracts import AgentInputError, AgentRequest, AgentRole
from agents.registry import AgentRegistry
from agents.runtime import MultiAgentRuntime
from reports.contracts import EvidenceReference, ExecutionRecord
from tests.support.fake_gemini import FakeGeminiClient


FakeClient = FakeGeminiClient


def request() -> AgentRequest:
    return AgentRequest(
        request_id="REQ-MA-TEST-001",
        prompt="Analyze this explicit test requirement.",
        requirement_ids=("REQ-RA-001",),
        context={"source": "unit-test"},
    )


def test_each_required_agent_is_registered_independently() -> None:
    registry = AgentRegistry.from_client(FakeClient())

    assert set(registry.roles()) == set(AgentRole)
    assert registry.get(AgentRole.REQUIREMENT_ANALYZER).spec.role is AgentRole.REQUIREMENT_ANALYZER
    assert registry.get("qa-reviewer").spec.role is AgentRole.QA_REVIEWER


def test_empty_prompt_is_rejected_before_provider_call() -> None:
    agent = AgentRegistry.from_client(FakeClient()).get(AgentRole.TEST_PLANNER)

    with pytest.raises(AgentInputError, match="prompt"):
        agent.run(AgentRequest(request_id="REQ-MA-TEST-002", prompt=""))


def test_caller_selected_agents_run_independently_without_sequence() -> None:
    runtime = MultiAgentRuntime(AgentRegistry.from_client(FakeClient()))
    selected = (AgentRole.FAILURE_ANALYZER, AgentRole.REQUIREMENT_ANALYZER)

    results = {role: runtime.invoke(role, request()) for role in selected}

    assert tuple(results) == selected
    assert results[AgentRole.FAILURE_ANALYZER].role is AgentRole.FAILURE_ANALYZER
    assert results[AgentRole.FAILURE_ANALYZER].output is not None
    assert results[AgentRole.REQUIREMENT_ANALYZER].lifecycle.value == "generated"


def test_report_pass_requires_real_evidence() -> None:
    without_evidence = ExecutionRecord(
        requirement_ids=("REQ-RA-001",),
        scenario_id="TC-001",
        lifecycle="executed",
        outcome="passed",
        duration_ms=12,
        evidence=(),
    )
    with_evidence = ExecutionRecord(
        requirement_ids=("REQ-RA-001",),
        scenario_id="TC-001",
        lifecycle="executed",
        outcome="passed",
        duration_ms=12,
        evidence=(EvidenceReference("stdout", "artifacts/run.json", "Playwright result"),),
    )

    assert not without_evidence.can_claim_pass()
    assert with_evidence.can_claim_pass()
