"""Chat and specialized-agent orchestration for the TUI."""

from __future__ import annotations

import uuid
from collections.abc import Callable, Sequence

from agents.contracts import AgentInputError, AgentRequest, AgentRole, AgentSpec, UnknownAgentError
from agents.formatting import format_agent_result
from agents.qa_engineer import QualityEngineerSession
from agents.qa_flow import run_qa_flow_formatted
from agents.registry import AgentRegistry
from agents.tool_runner import AgentToolRunner, PhaseCallback, StreamCallback

CHAT_ACTIVITY_PHASES: tuple[str, ...] = (
    "Tool · gemini-reasoning",
    "Reviewing QA context",
    "Drafting guidance",
)

def activity_phases_for_agent(spec: AgentSpec) -> tuple[str, ...]:
    tool_steps = tuple(f"Tool · {tool.value}" for tool in spec.tools)
    return (f"Agent · {spec.name}", *tool_steps, "gemini-reasoning", "Structured output validation")


class QATUIOrchestrator:
    """Runs conversational QA or explicit specialized agents for the TUI."""

    def __init__(self, session: QualityEngineerSession, registry: AgentRegistry | None = None) -> None:
        self.session = session
        self.registry = registry or AgentRegistry.from_client(session.client)
        self.tool_runner = AgentToolRunner()

    def chat_phases(self) -> Sequence[str]:
        return CHAT_ACTIVITY_PHASES

    def agent_phases(self, role: AgentRole) -> Sequence[str]:
        return activity_phases_for_agent(self.registry.get(role).spec)

    def respond_chat(self, user_text: str, *, on_stream: StreamCallback | None = None) -> str:
        return self.session.respond(user_text, on_stream=on_stream)

    def invoke_agent(
        self,
        role: AgentRole,
        prompt: str,
        *,
        requirement_ids: Sequence[str] = (),
        on_phase: PhaseCallback | None = None,
        on_stream: StreamCallback | None = None,
    ) -> str:
        request = AgentRequest(
            request_id=f"TUI-{uuid.uuid4().hex[:8].upper()}",
            prompt=prompt,
            requirement_ids=tuple(requirement_ids),
        )
        try:
            request.validate()
            result = self.tool_runner.run(
                self.registry.get(role),
                request,
                on_phase=on_phase,
                on_stream=on_stream,
            )
        except (AgentInputError, UnknownAgentError, ValueError) as exc:
            raise ValueError(str(exc)) from exc
        return format_agent_result(result)

    def invoke_qa_flow(
        self,
        prompt: str,
        *,
        requirement_ids: Sequence[str] = (),
        on_phase: PhaseCallback | None = None,
        on_stream: StreamCallback | None = None,
    ) -> str:
        try:
            return run_qa_flow_formatted(
                self.registry,
                prompt,
                requirement_ids=requirement_ids,
                on_phase=on_phase,
                on_stream=on_stream,
            )
        except (AgentInputError, UnknownAgentError, ValueError) as exc:
            raise ValueError(str(exc)) from exc


async def animate_phases_while(
    phases: Sequence[str],
    work: Callable[[], str],
    *,
    on_phase: Callable[[str], None],
    interval_seconds: float = 0.45,
) -> str:
    """Rotate phase labels on the UI thread while blocking work runs in a worker thread."""

    import asyncio

    if not phases:
        on_phase("Working…")
        return await asyncio.to_thread(work)

    task = asyncio.create_task(asyncio.to_thread(work))
    index = 0
    on_phase(phases[0])
    while not task.done():
        await asyncio.sleep(interval_seconds)
        if task.done():
            break
        index = (index + 1) % len(phases)
        on_phase(phases[index])
    return await task
