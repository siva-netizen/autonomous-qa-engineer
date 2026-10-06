from __future__ import annotations

import pytest

from agents.contracts import AgentRole
from agents.tui_commands import SlashAction, parse_slash_command


def test_agents_lists_roles() -> None:
    command = parse_slash_command("/agents")
    assert command is not None
    assert command.action is SlashAction.LIST_AGENTS


def test_agent_invoke_parses_role_and_prompt() -> None:
    command = parse_slash_command("/agent qa-reviewer Review evidence gaps for checkout")
    assert command is not None
    assert command.action is SlashAction.RUN_AGENT
    assert command.agent_role is AgentRole.QA_REVIEWER
    assert command.agent_prompt == "Review evidence gaps for checkout"


def test_agents_prefix_alias_for_invoke() -> None:
    command = parse_slash_command("/agents requirement-analyzer Review checkout")
    assert command is not None
    assert command.action is SlashAction.RUN_AGENT
    assert command.agent_role is AgentRole.REQUIREMENT_ANALYZER


def test_bare_agent_shows_help_not_chat() -> None:
    command = parse_slash_command("/agent")
    assert command is not None
    assert command.action is SlashAction.AGENT_HELP


def test_unknown_slash_command() -> None:
    command = parse_slash_command("/foo bar")
    assert command is not None
    assert command.action is SlashAction.UNKNOWN


def test_normal_text_is_not_a_command() -> None:
    assert parse_slash_command("Review checkout") is None


def test_unknown_agent_role() -> None:
    command = parse_slash_command("/agent not-a-role do work")
    assert command is not None
    assert command.action is SlashAction.UNKNOWN
    assert "Unknown agent" in (command.message or "")


def test_flow_command_parses_goal() -> None:
    command = parse_slash_command("/flow ShopDemo checkout coverage")
    assert command is not None
    assert command.action is SlashAction.RUN_FLOW
    assert command.agent_prompt == "ShopDemo checkout coverage"
