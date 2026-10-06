"""Property-based correctness tests for structured agent output (Kiro Spec Correctness)."""

from __future__ import annotations

import json
from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from agents.contracts import (
    AgentOutcome,
    AgentRole,
    Lifecycle,
    StructuredAgentOutput,
    StructuredOutputError,
)
from test_agent_output_contracts import valid_document

pytestmark = pytest.mark.property


@given(
    role=st.sampled_from(list(AgentRole)),
    summary=st.text(min_size=1, max_size=240).filter(lambda value: value.strip()),
)
@settings(max_examples=100)
def test_prop_valid_minimum_documents_always_parse(role: AgentRole, summary: str) -> None:
    """PROP-AOC-001: minimum valid JSON for any role always validates."""
    document = valid_document(role)
    document["summary"] = summary.strip()
    output = StructuredAgentOutput.from_json(
        json.dumps(document),
        expected_request_id="REQ-AOC-TEST-001",
        expected_role=role,
        expected_requirement_ids=("REQ-RA-001",),
    )
    assert output.role is role
    assert output.lifecycle is Lifecycle.GENERATED


@given(invalid_id=st.text(min_size=1, max_size=64).filter(lambda value: not value.startswith("REQ-")))
@settings(max_examples=100)
def test_prop_invalid_requirement_ids_are_rejected(invalid_id: str) -> None:
    """PROP-AOC-002: malformed REQ IDs never pass validation."""
    document = valid_document(AgentRole.TEST_PLANNER)
    document["requirement_ids"] = [invalid_id]
    with pytest.raises(StructuredOutputError, match="requirement_ids"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=AgentRole.TEST_PLANNER,
        )


@given(role=st.sampled_from(list(AgentRole)))
@settings(max_examples=50)
def test_prop_generated_output_cannot_claim_passed(role: AgentRole) -> None:
    """PROP-AOC-003: generated lifecycle cannot claim passed execution."""
    document = valid_document(role, outcome=AgentOutcome.PASSED)
    with pytest.raises(StructuredOutputError, match="passed execution"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=role,
        )


@given(
    role=st.sampled_from(list(AgentRole)),
    lifecycle=st.sampled_from([Lifecycle.EXECUTED, Lifecycle.VERIFIED]),
)
@settings(max_examples=50)
def test_prop_non_generated_lifecycle_requires_evidence(
    role: AgentRole, lifecycle: Lifecycle
) -> None:
    """PROP-AOC-004: executed/verified without evidence is always rejected."""
    document: dict[str, Any] = valid_document(role, lifecycle=lifecycle, evidence=[])
    with pytest.raises(StructuredOutputError, match="evidence"):
        StructuredAgentOutput.from_json(
            json.dumps(document),
            expected_request_id="REQ-AOC-TEST-001",
            expected_role=role,
        )
