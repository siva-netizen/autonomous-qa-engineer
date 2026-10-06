"""Explicit registry for independently invokable specialized agents."""

from __future__ import annotations

from collections.abc import Mapping

from agents.base import BaseAgent
from agents.contracts import AgentRole, UnknownAgentError
from agents.specialized import AGENT_CLASSES
from services.gemini_client import ReasoningClient


class AgentRegistry:
    def __init__(self, agents: Mapping[AgentRole, BaseAgent]) -> None:
        self._agents = dict(agents)

    @classmethod
    def from_client(cls, client: ReasoningClient) -> "AgentRegistry":
        return cls({role: agent_class(client) for role, agent_class in AGENT_CLASSES.items()})

    def get(self, role: AgentRole | str) -> BaseAgent:
        try:
            normalized = role if isinstance(role, AgentRole) else AgentRole(role)
        except ValueError as exc:
            raise UnknownAgentError(role) from exc
        try:
            return self._agents[normalized]
        except KeyError as exc:
            raise UnknownAgentError(normalized) from exc

    def roles(self) -> tuple[AgentRole, ...]:
        return tuple(self._agents)
