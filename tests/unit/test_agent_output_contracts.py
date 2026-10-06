from __future__ import annotations

import json
from typing import Any

import pytest

from agents.contracts import (
    AgentOutcome,
    AgentRole,
    Lifecycle,
    StructuredAgentOutput,
    StructuredOutputError,
    build_output_instructions,
)


def valid_document(
    role: AgentRole,
    *,
    lifecycle: Lifecycle = Lifecycle.GENERATED,
    evidence: list[dict[str, str]] | None = None,
    outcome: AgentOutcome | None = None,
) -> dict[str, Any]:
    payloads: dict[AgentRole, dict[str, Any]] = {
        AgentRole.REQUIREMENT_ANALYZER: {"requirements": [{"id": "REQ-RA-001"}]},
        AgentRole.TEST_PLANNER: {"scenarios": [{"id": "TC-001"}]},
        AgentRole.PLAYWRIGHT_ENGINEER: {
            "generated_test": "tests/e2e/example.spec.ts",
            "evidence_plan": ["screenshot", "trace"],
        },
        AgentRole.FAILURE_ANALYZER: {
            "classification": "unknown",
            "observed_behavior": "The request timed out.",
            "expected_behavior": "The page should load.",
            "confidence": 0.75,
            "recommended_action": "Collect network evidence.",
        },
        AgentRole.QA_REVIEWER: {
            "coverage_gaps": [],
            "evidence_gaps": [],
            "verification_recommendation": "Run the planned browser test.",
        },
    }
    return {
        "request_id": "REQ-AOC-TEST-001",
        "role": role.value,
        "summary": f"Structured output for {role.value}.",
        "lifecycle": lifecycle.value,
        "requirement_ids": ["REQ-RA-001"],
        "scenario_ids": ["TC-001"],
        "payload": payloads[role],
        "assumptions": [],
        "open_questions": [],
        "evidence": evidence or [],
        "outcome": outcome.value if outcome is not None else None,
        "metadata": {"source": "fake-transport"},
    }


@pytest.mark.parametrize("role", list(AgentRole))
def test_each_role_accepts_its_minimum_structured_payload(role: AgentRole) -> None:
    output = StructuredAgentOutput.from_json(
        json.dumps(valid_document(role)),
        expected_request_id="REQ-AOC-TEST-001",
        expected_role=role,
    )

    assert output.role is role
    assert output.lifecycle is Lifecycle.GENERATED
    assert output.requirement_ids == ("REQ-RA-001",)
    assert output.to_dict()["role"] == role.value


def test_malformed_json_is_rejected() -> None:
    with pytest.raises(StructuredOutputError, match="valid JSON"):
        StructuredAgentOutput.from_json(
            "not-json",
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.REQUIREMENT_ANALYZER,
        )


def test_request_and_role_mismatches_are_rejected() -> None:
    document = valid_document(AgentRole.TEST_PLANNER)
    document["request_id"] = "REQ-AOC-OTHER-001"

    with pytest.raises(StructuredOutputError, match="request_id"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.TEST_PLANNER,
        )

    document["request_id"] = "REQ-AOC-TEST-001"
    with pytest.raises(StructuredOutputError, match="role"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.REQUIREMENT_ANALYZER,
        )


def test_missing_role_payload_field_is_rejected() -> None:
    document = valid_document(AgentRole.FAILURE_ANALYZER)
    del document["payload"]["confidence"]

    with pytest.raises(StructuredOutputError, match="confidence"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.FAILURE_ANALYZER,
        )


def test_executed_output_requires_evidence() -> None:
    document = valid_document(AgentRole.TEST_PLANNER, lifecycle=Lifecycle.EXECUTED)

    with pytest.raises(StructuredOutputError, match="evidence"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.TEST_PLANNER,
        )


def test_caller_requirement_ids_cannot_be_dropped() -> None:
    document = valid_document(AgentRole.TEST_PLANNER)
    document["requirement_ids"] = []

    with pytest.raises(StructuredOutputError, match="dropped requirement IDs"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.TEST_PLANNER,
            expected_requirement_ids=("REQ-RA-001",),
        )


def test_generated_output_cannot_claim_passed_execution() -> None:
    document = valid_document(AgentRole.QA_REVIEWER, outcome=AgentOutcome.PASSED)

    with pytest.raises(StructuredOutputError, match="passed execution"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.QA_REVIEWER,
        )


def test_verified_passed_output_requires_real_evidence_reference() -> None:
    document = valid_document(
        AgentRole.QA_REVIEWER,
        lifecycle=Lifecycle.VERIFIED,
        outcome=AgentOutcome.PASSED,
        evidence=[
            {
                "kind": "trace",
                "path": "artifacts/run/trace.zip",
                "description": "Real Playwright execution trace",
            }
        ],
    )

    output = StructuredAgentOutput.from_json(
        json.dumps(document),
        expected_request_id="REQ-AOC-TEST-001",
        expected_role=AgentRole.QA_REVIEWER,
    )

    assert output.outcome is AgentOutcome.PASSED
    assert output.evidence[0].path == "artifacts/run/trace.zip"


def test_markdown_fenced_json_is_parsed() -> None:
    document = valid_document(AgentRole.REQUIREMENT_ANALYZER)
    fenced = "```json\n" + json.dumps(document) + "\n```"

    output = StructuredAgentOutput.from_json(
        fenced,
        expected_request_id="REQ-AOC-TEST-001",
        expected_role=AgentRole.REQUIREMENT_ANALYZER,
    )

    assert output.role is AgentRole.REQUIREMENT_ANALYZER
    assert output.requirement_ids == ("REQ-RA-001",)


def test_plain_fence_without_language_is_parsed() -> None:
    document = valid_document(AgentRole.TEST_PLANNER)
    fenced = "```\n" + json.dumps(document) + "\n```"

    output = StructuredAgentOutput.from_json(
        fenced,
        expected_request_id="REQ-AOC-TEST-001",
        expected_role=AgentRole.TEST_PLANNER,
    )

    assert output.role is AgentRole.TEST_PLANNER


def test_non_json_prose_is_still_rejected() -> None:
    with pytest.raises(StructuredOutputError, match="valid JSON"):
        StructuredAgentOutput.from_json(
            "Here is my analysis: everything looks fine.",
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.REQUIREMENT_ANALYZER,
        )


@pytest.mark.parametrize("role", list(AgentRole))
def test_output_instructions_describe_contract(role: AgentRole) -> None:
    instructions = build_output_instructions(
        role,
        request_id="REQ-AOC-TEST-001",
        requirement_ids=("REQ-RA-001",),
    )

    assert '"lifecycle"' in instructions
    assert "generated" in instructions
    assert role.value in instructions
    assert "REQ-AOC-TEST-001" in instructions
    assert "REQ-RA-001" in instructions


def test_instructed_document_satisfies_validator() -> None:
    # The instructions promise an "generated" + empty-evidence document is valid;
    # verify that promise holds against the real validator for every role.
    for role in AgentRole:
        document = valid_document(role)
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=role,
            expected_requirement_ids=("REQ-RA-001",),
        )
