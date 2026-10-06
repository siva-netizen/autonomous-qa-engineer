"""Slash-command parsing for the QA engineer TUI."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from agents.contracts import AgentRole

_AGENT_INVOKE = re.compile(
    r"^/agent(?:s)?\s+(?P<role>[a-z-]+)\s+(?P<prompt>.+)$",
    re.IGNORECASE | re.DOTALL,
)

_FLOW = re.compile(r"^/flow\s+(?P<prompt>.+)$", re.IGNORECASE | re.DOTALL)
_CHAT = re.compile(r"^/chat\s+(?P<prompt>.+)$", re.IGNORECASE | re.DOTALL)


class SlashAction(StrEnum):
    HELP = "help"
    QUIT = "quit"
    CLEAR = "clear"
    LIST_AGENTS = "list_agents"
    AGENT_HELP = "agent_help"
    RUN_AGENT = "run_agent"
    RUN_FLOW = "run_flow"
    FLOW_HELP = "flow_help"
    RUN_CHAT = "run_chat"
    CHAT_HELP = "chat_help"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class SlashCommand:
    action: SlashAction
    agent_role: AgentRole | None = None
    agent_prompt: str | None = None
    raw: str = ""
    message: str = ""


def parse_slash_command(text: str) -> SlashCommand | None:
    """Return a slash command, or None if the line is normal chat input."""

    stripped = text.strip()
    if not stripped.startswith("/"):
        return None

    lowered = stripped.lower()
    if lowered in {"/quit", "/exit", "/q"}:
        return SlashCommand(action=SlashAction.QUIT)
    if lowered == "/help":
        return SlashCommand(action=SlashAction.HELP)
    if lowered == "/clear":
        return SlashCommand(action=SlashAction.CLEAR)
    if lowered in {"/agents", "/agent-list", "/list-agents"}:
        return SlashCommand(action=SlashAction.LIST_AGENTS)
    if lowered in {"/agent", "/agents"}:
        return SlashCommand(
            action=SlashAction.AGENT_HELP,
            message="Usage: /agent <role> <prompt>",
        )
    if lowered in {"/flow", "/pipeline", "/qa-flow"}:
        return SlashCommand(
            action=SlashAction.FLOW_HELP,
            message="Usage: /flow <goal> — runs requirement-analyzer → test-planner → playwright-engineer",
        )

    chat_match = _CHAT.match(stripped)
    if chat_match:
        prompt = chat_match.group("prompt").strip()
        if not prompt:
            return SlashCommand(
                action=SlashAction.CHAT_HELP,
                message="Usage: /chat <question> — advisor-only, no files or MCP tools",
            )
        return SlashCommand(action=SlashAction.RUN_CHAT, agent_prompt=prompt)

    if lowered == "/chat":
        return SlashCommand(
            action=SlashAction.CHAT_HELP,
            message="Usage: /chat <question> — advisor-only, no files or MCP tools",
        )

    flow_match = _FLOW.match(stripped)
    if flow_match:
        prompt = flow_match.group("prompt").strip()
        if not prompt:
            return SlashCommand(
                action=SlashAction.FLOW_HELP,
                message="Usage: /flow <goal>",
            )
        return SlashCommand(action=SlashAction.RUN_FLOW, agent_prompt=prompt)

    match = _AGENT_INVOKE.match(stripped)
    if match:
        role_raw = match.group("role").lower()
        prompt = match.group("prompt").strip()
        if not prompt:
            return SlashCommand(
                action=SlashAction.AGENT_HELP,
                message="Usage: /agent <role> <prompt>",
            )
        try:
            role = AgentRole(role_raw)
        except ValueError:
            supported = ", ".join(item.value for item in AgentRole)
            return SlashCommand(
                action=SlashAction.UNKNOWN,
                raw=stripped,
                message=f"Unknown agent '{role_raw}'. Choose from: {supported}",
            )
        return SlashCommand(action=SlashAction.RUN_AGENT, agent_role=role, agent_prompt=prompt)

    if lowered.startswith("/agent"):
        return SlashCommand(
            action=SlashAction.AGENT_HELP,
            message="Usage: /agent <role> <prompt>",
        )

    return SlashCommand(
        action=SlashAction.UNKNOWN,
        raw=stripped,
        message=f"Unknown command '{stripped.split()[0]}'. Type /help.",
    )
