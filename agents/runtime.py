"""Selected-agent runtime; callers choose the agents and any context handoff."""

from __future__ import annotations

from agents.contracts import AgentRequest, AgentResult, AgentRole
from agents.registry import AgentRegistry


class MultiAgentRuntime:
    """Invoke one or explicitly selected agents; no mandatory ordering is encoded."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def invoke(self, role: AgentRole | str, request: AgentRequest) -> AgentResult:
        return self.registry.get(role).run(request)
