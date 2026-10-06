"""Shared contracts for independently invokable QA agents."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping, cast


class AgentRole(StrEnum):
    REQUIREMENT_ANALYZER = "requirement-analyzer"
    TEST_PLANNER = "test-planner"
    PLAYWRIGHT_ENGINEER = "playwright-engineer"
    FAILURE_ANALYZER = "failure-analyzer"
    QA_REVIEWER = "qa-reviewer"


class AgentTool(StrEnum):
    GEMINI = "gemini-reasoning"
    FILES = "file-tools"
    PLAYWRIGHT_MCP = "playwright-mcp"
    GITHUB_MCP_READ = "github-mcp-read"


class Lifecycle(StrEnum):
    GENERATED = "generated"
    EXECUTED = "executed"
    VERIFIED = "verified"


class AgentOutcome(StrEnum):
    NOT_RUN = "not-run"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class AgentInputError(ValueError):
    """Raised when an agent request is empty or malformed."""


class StructuredOutputError(ValueError):
    """Raised when provider content violates the structured agent contract."""


class UnknownAgentError(KeyError):
    """Raised when a caller selects an unregistered agent role."""


_REQUIREMENT_ID = re.compile(r"^REQ-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$")
_SCENARIO_ID = re.compile(r"^TC-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$")
_EVIDENCE_KINDS = frozenset({"screenshot", "trace", "console", "network", "dom", "stdout"})
_ROLE_FIELDS: dict[AgentRole, tuple[str, ...]] = {
    AgentRole.REQUIREMENT_ANALYZER: ("requirements",),
    AgentRole.TEST_PLANNER: ("scenarios",),
    AgentRole.PLAYWRIGHT_ENGINEER: ("generated_test", "evidence_plan"),
    AgentRole.FAILURE_ANALYZER: (
        "classification",
        "observed_behavior",
        "expected_behavior",
        "confidence",
        "recommended_action",
    ),
    AgentRole.QA_REVIEWER: (
        "coverage_gaps",
        "evidence_gaps",
        "verification_recommendation",
    ),
}


def _non_empty(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StructuredOutputError(f"{field_name} must be a non-empty string")
    return value.strip()


def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise StructuredOutputError(f"{field_name} must be a JSON array")
    values: list[str] = []
    for index, item in enumerate(value):
        values.append(_non_empty(item, f"{field_name}[{index}]"))
    return tuple(values)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise StructuredOutputError(f"{field_name} must be a JSON object")
    return value


def _evidence(value: Any) -> tuple[EvidenceReference, ...]:
    if not isinstance(value, list):
        raise StructuredOutputError("evidence must be a JSON array")
    references: list[EvidenceReference] = []
    for index, raw_reference in enumerate(value):
        reference = _mapping(raw_reference, f"evidence[{index}]")
        kind = _non_empty(reference.get("kind"), f"evidence[{index}].kind")
        if kind not in _EVIDENCE_KINDS:
            raise StructuredOutputError(f"evidence[{index}].kind is unsupported")
        path = _non_empty(reference.get("path"), f"evidence[{index}].path")
        description = _non_empty(
            reference.get("description"), f"evidence[{index}].description"
        )
        references.append(
            EvidenceReference(kind=cast(Any, kind), path=path, description=description)
        )
    return tuple(references)


def _validate_ids(values: tuple[str, ...], pattern: re.Pattern[str], field_name: str) -> None:
    for value in values:
        if not pattern.fullmatch(value):
            raise StructuredOutputError(f"{field_name} contains invalid traceability ID: {value}")


def _strip_code_fences(content: str) -> str:
    """Remove a surrounding markdown code fence if the model added one.

    Only a single fenced block that wraps the whole payload is unwrapped; any
    other content is returned unchanged so genuinely malformed output still
    fails strict JSON parsing.
    """

    text = content.strip()
    if not text.startswith("```"):
        return text
    first_newline = text.find("\n")
    if first_newline == -1:
        return text
    body = text[first_newline + 1 :]
    closing = body.rfind("```")
    if closing == -1:
        return text
    return body[:closing].strip()


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    """A persisted artifact reference; it does not claim the artifact is valid by itself."""

    kind: str
    path: str
    description: str


@dataclass(frozen=True, slots=True)
class AgentRequest:
    """Input supplied to one or more independent agents."""

    request_id: str
    prompt: str
    requirement_ids: tuple[str, ...] = ()
    context: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.request_id.strip():
            raise AgentInputError("request_id must not be empty")
        if not self.prompt.strip():
            raise AgentInputError("prompt must not be empty")


@dataclass(frozen=True, slots=True)
class AgentSpec:
    """Contract metadata mirrored by each `.kiro/agents/*.md` file."""

    role: AgentRole
    name: str
    description: str
    tools: tuple[AgentTool, ...]
    input_contract: str
    output_contract: str
    prohibited_claims: tuple[str, ...]
    system_prompt: str


@dataclass(frozen=True, slots=True)
class StructuredAgentOutput:
    """Validated, role-specific JSON returned by an independently invoked agent."""

    request_id: str
    role: AgentRole
    summary: str
    lifecycle: Lifecycle
    requirement_ids: tuple[str, ...]
    scenario_ids: tuple[str, ...]
    payload: Mapping[str, Any]
    assumptions: tuple[str, ...] = ()
    open_questions: tuple[str, ...] = ()
    evidence: tuple[EvidenceReference, ...] = ()
    outcome: AgentOutcome | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(
        cls,
        content: str,
        *,
        expected_request_id: str,
        expected_role: AgentRole,
        expected_requirement_ids: tuple[str, ...] = (),
    ) -> "StructuredAgentOutput":
        try:
            decoded = json.loads(_strip_code_fences(content))
        except json.JSONDecodeError as exc:
            raise StructuredOutputError("agent content must be valid JSON") from exc
        if not isinstance(decoded, dict):
            raise StructuredOutputError("agent content must be a JSON object")

        try:
            lifecycle = Lifecycle(decoded["lifecycle"])
        except (KeyError, ValueError, TypeError) as exc:
            raise StructuredOutputError("lifecycle must be generated, executed, or verified") from exc

        raw_role = decoded.get("role")
        if not isinstance(raw_role, str):
            raise StructuredOutputError("role is not a supported agent role")
        try:
            role = AgentRole(raw_role)
        except ValueError as exc:
            raise StructuredOutputError("role is not a supported agent role") from exc

        raw_outcome = decoded.get("outcome")
        if raw_outcome is None:
            outcome = None
        else:
            try:
                outcome = AgentOutcome(raw_outcome)
            except (ValueError, TypeError) as exc:
                raise StructuredOutputError("outcome is not supported") from exc

        output = cls(
            request_id=_non_empty(decoded.get("request_id"), "request_id"),
            role=role,
            summary=_non_empty(decoded.get("summary"), "summary"),
            lifecycle=lifecycle,
            requirement_ids=_string_tuple(decoded.get("requirement_ids"), "requirement_ids"),
            scenario_ids=_string_tuple(decoded.get("scenario_ids"), "scenario_ids"),
            payload=_mapping(decoded.get("payload"), "payload"),
            assumptions=_string_tuple(decoded.get("assumptions", []), "assumptions"),
            open_questions=_string_tuple(decoded.get("open_questions", []), "open_questions"),
            evidence=_evidence(decoded.get("evidence", [])),
            outcome=outcome,
            metadata=_mapping(decoded.get("metadata", {}), "metadata"),
        )
        output.validate(
            expected_request_id=expected_request_id,
            expected_role=expected_role,
            expected_requirement_ids=expected_requirement_ids,
        )
        return output

    def validate(
        self,
        *,
        expected_request_id: str | None = None,
        expected_role: AgentRole | None = None,
        expected_requirement_ids: tuple[str, ...] = (),
    ) -> None:
        if not self.request_id.strip():
            raise StructuredOutputError("request_id must not be empty")
        if expected_request_id is not None and self.request_id != expected_request_id:
            raise StructuredOutputError("structured output request_id does not match request")
        if expected_role is not None and self.role is not expected_role:
            raise StructuredOutputError("structured output role does not match invoking agent")
        if not self.summary.strip():
            raise StructuredOutputError("summary must not be empty")
        if not self.requirement_ids and not self.scenario_ids:
            raise StructuredOutputError("structured output must include requirement_ids or scenario_ids")
        _validate_ids(self.requirement_ids, _REQUIREMENT_ID, "requirement_ids")
        _validate_ids(self.scenario_ids, _SCENARIO_ID, "scenario_ids")
        missing_requirement_ids = set(expected_requirement_ids).difference(self.requirement_ids)
        if missing_requirement_ids:
            missing = ", ".join(sorted(missing_requirement_ids))
            raise StructuredOutputError(f"structured output dropped requirement IDs: {missing}")
        for field_name in _ROLE_FIELDS[self.role]:
            if field_name not in self.payload:
                raise StructuredOutputError(
                    f"payload for {self.role.value} requires {field_name}"
                )
        list_fields = {
            "requirements",
            "scenarios",
            "evidence_plan",
            "coverage_gaps",
            "evidence_gaps",
        }
        for field_name in list_fields.intersection(self.payload):
            if not isinstance(self.payload[field_name], list):
                raise StructuredOutputError(f"payload.{field_name} must be a JSON array")
        if self.role is AgentRole.PLAYWRIGHT_ENGINEER:
            _non_empty(self.payload["generated_test"], "payload.generated_test")
        if self.role is AgentRole.FAILURE_ANALYZER:
            for field_name in (
                "classification",
                "observed_behavior",
                "expected_behavior",
                "recommended_action",
            ):
                _non_empty(self.payload[field_name], f"payload.{field_name}")
            confidence = self.payload["confidence"]
            if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
                raise StructuredOutputError("payload.confidence must be numeric")
            if not 0 <= confidence <= 1:
                raise StructuredOutputError("payload.confidence must be between 0 and 1")
        if self.role is AgentRole.QA_REVIEWER:
            _non_empty(
                self.payload["verification_recommendation"],
                "payload.verification_recommendation",
            )
        if self.lifecycle is not Lifecycle.GENERATED and not self.evidence:
            raise StructuredOutputError("executed and verified outputs require evidence references")
        if self.outcome is AgentOutcome.PASSED and self.lifecycle is Lifecycle.GENERATED:
            raise StructuredOutputError("generated output cannot claim a passed execution")
        for reference in self.evidence:
            _non_empty(reference.kind, "evidence.kind")
            _non_empty(reference.path, "evidence.path")
            _non_empty(reference.description, "evidence.description")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "role": self.role.value,
            "summary": self.summary,
            "lifecycle": self.lifecycle.value,
            "requirement_ids": list(self.requirement_ids),
            "scenario_ids": list(self.scenario_ids),
            "payload": dict(self.payload),
            "assumptions": list(self.assumptions),
            "open_questions": list(self.open_questions),
            "evidence": [
                {
                    "kind": reference.kind,
                    "path": reference.path,
                    "description": reference.description,
                }
                for reference in self.evidence
            ],
            "outcome": self.outcome.value if self.outcome is not None else None,
            "metadata": dict(self.metadata),
        }


_ROLE_PAYLOAD_GUIDANCE: dict[AgentRole, str] = {
    AgentRole.REQUIREMENT_ANALYZER: (
        '"requirements" (JSON array of requirement obligation strings)'
    ),
    AgentRole.TEST_PLANNER: (
        '"scenarios" (JSON array of scenario objects or strings)'
    ),
    AgentRole.PLAYWRIGHT_ENGINEER: (
        '"generated_test" (non-empty string of Playwright test code) and '
        '"evidence_plan" (JSON array of planned evidence steps)'
    ),
    AgentRole.FAILURE_ANALYZER: (
        '"classification", "observed_behavior", "expected_behavior", '
        '"recommended_action" (non-empty strings) and "confidence" '
        "(number between 0 and 1)"
    ),
    AgentRole.QA_REVIEWER: (
        '"coverage_gaps" (JSON array), "evidence_gaps" (JSON array), and '
        '"verification_recommendation" (non-empty string)'
    ),
}


def build_output_instructions(
    role: AgentRole,
    *,
    request_id: str,
    requirement_ids: tuple[str, ...] = (),
) -> str:
    """Describe the exact structured JSON the provider must return for this role.

    The schema is derived from the contract so the instruction and the validator
    cannot drift apart.
    """

    lifecycles = ", ".join(member.value for member in Lifecycle)
    outcomes = ", ".join(member.value for member in AgentOutcome)
    required_requirements = (
        f" You MUST include every one of these requirement IDs in requirement_ids: "
        f"{', '.join(requirement_ids)}."
        if requirement_ids
        else ""
    )
    payload_fields = _ROLE_PAYLOAD_GUIDANCE[role]
    return (
        "Return ONLY a single JSON object and nothing else. No prose, no markdown, "
        "no code fences. The object MUST contain these keys:\n"
        f'- "request_id": exactly "{request_id}"\n'
        f'- "role": exactly "{role.value}"\n'
        '- "summary": a concise non-empty string\n'
        f'- "lifecycle": one of [{lifecycles}]. Use "generated" for reasoning-only '
        "output with no real browser execution evidence.\n"
        '- "requirement_ids": JSON array of REQ-* IDs (for example "REQ-RA-001"). '
        'Use "scenario_ids" (TC-* IDs) instead or in addition when relevant; at '
        "least one of the two arrays must be non-empty." + required_requirements + "\n"
        '- "scenario_ids": JSON array of TC-* IDs (may be empty).\n'
        f'- "payload": a JSON object that MUST include {payload_fields}.\n'
        '- "assumptions": JSON array of strings (may be empty).\n'
        '- "open_questions": JSON array of strings (may be empty).\n'
        '- "evidence": JSON array of objects, each with "kind" (one of '
        f"[{', '.join(sorted(_EVIDENCE_KINDS))}]), \"path\", and \"description\". "
        'Only include evidence that genuinely exists. For "generated" lifecycle '
        "this MUST be an empty array because no real execution occurred.\n"
        f'- "outcome": optional, one of [{outcomes}]. Never use "passed" with the '
        '"generated" lifecycle because reasoning alone is not a verified pass.\n'
        '- "metadata": optional JSON object.\n'
        "Do not invent product behavior, selectors, screenshots, or execution results."
    )


@dataclass(frozen=True, slots=True)
class AgentResult:
    """Validated reasoning output; it is not automatically a browser execution result."""

    request_id: str
    role: AgentRole
    content: str
    lifecycle: Lifecycle = Lifecycle.GENERATED
    model: str | None = None
    evidence: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    output: StructuredAgentOutput | None = None

    def validate(self) -> None:
        if not self.request_id.strip():
            raise ValueError("AgentResult.request_id must not be empty")
        if not self.content.strip():
            raise ValueError("AgentResult.content must not be empty")
        if self.output is not None:
            self.output.validate(expected_request_id=self.request_id, expected_role=self.role)
            if self.lifecycle is not self.output.lifecycle:
                raise ValueError("AgentResult lifecycle must match structured output")
            if self.evidence != tuple(reference.path for reference in self.output.evidence):
                raise ValueError("AgentResult evidence must match structured output")
        elif self.lifecycle is not Lifecycle.GENERATED and not self.evidence:
            raise ValueError("non-generated results require evidence references")
