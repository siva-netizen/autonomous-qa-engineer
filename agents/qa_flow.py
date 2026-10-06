"""Sequential QA pipeline: requirement analysis → test planning → Playwright generation."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Sequence

from agents.contracts import AgentRequest, AgentResult, AgentRole
from agents.registry import AgentRegistry
from agents.tool_runner import AgentToolRunner, PhaseCallback, StreamCallback
from agents.formatting import format_agent_result

DEFAULT_QA_FLOW: tuple[AgentRole, ...] = (
    AgentRole.REQUIREMENT_ANALYZER,
    AgentRole.TEST_PLANNER,
    AgentRole.PLAYWRIGHT_ENGINEER,
)


def run_qa_flow(
    registry: AgentRegistry,
    prompt: str,
    *,
    requirement_ids: Sequence[str] = ("REQ-RA-001",),
    roles: Sequence[AgentRole] = DEFAULT_QA_FLOW,
    on_phase: PhaseCallback | None = None,
    on_stream: StreamCallback | None = None,
) -> tuple[AgentResult, ...]:
    runner = AgentToolRunner()
    flow_id = f"FLOW-{uuid.uuid4().hex[:8].upper()}"
    context: dict[str, object] = {"flow_id": flow_id, "steps": []}
    results: list[AgentResult] = []
    active_requirement_ids = tuple(requirement_ids)

    for index, role in enumerate(roles):
        step_request = AgentRequest(
            request_id=f"{flow_id}-{index + 1}",
            prompt=(
                f"Pipeline step {index + 1}/{len(roles)} for flow {flow_id}. "
                f"User goal: {prompt}"
            ),
            requirement_ids=active_requirement_ids,
            context=dict(context),
        )
        result = runner.run(
            registry.get(role),
            step_request,
            on_phase=on_phase,
            on_stream=on_stream,
        )
        results.append(result)
        if result.output and result.output.requirement_ids:
            active_requirement_ids = result.output.requirement_ids
        context["steps"] = [
            *context.get("steps", []),
            {
                "role": result.role.value,
                "summary": result.output.summary if result.output else result.content,
                "payload": dict(result.output.payload) if result.output else {},
            },
        ]

    return tuple(results)


def format_qa_flow_results(results: Sequence[AgentResult]) -> str:
    sections: list[str] = [
        "**QA flow complete** — agents ran in sequence with shared context.",
        "",
    ]
    for result in results:
        sections.append(format_agent_result(result))
        written = result.metadata.get("written_test_path")
        if isinstance(written, str):
            sections.extend(["", f"**Written test file:** `{written}`"])
        sections.append("")
    return "\n".join(sections).strip()


def run_qa_flow_formatted(
    registry: AgentRegistry,
    prompt: str,
    *,
    requirement_ids: Sequence[str] = ("REQ-RA-001",),
    on_phase: PhaseCallback | None = None,
    on_stream: StreamCallback | None = None,
) -> str:
    ids = tuple(requirement_ids) if requirement_ids else ("REQ-RA-001",)
    results = run_qa_flow(
        registry,
        prompt,
        requirement_ids=ids,
        on_phase=on_phase,
        on_stream=on_stream,
    )
    return format_qa_flow_results(results)
