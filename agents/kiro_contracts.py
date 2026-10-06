"""Load Kiro agent contract markdown used as the runtime system prompt."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from agents.contracts import AgentRole

_REPO_ROOT = Path(__file__).resolve().parent.parent
_AGENT_DIR = _REPO_ROOT / ".kiro" / "agents"

_ROLE_FILES: dict[AgentRole, str] = {
    AgentRole.REQUIREMENT_ANALYZER: "requirement-analyzer.md",
    AgentRole.TEST_PLANNER: "test-planner.md",
    AgentRole.PLAYWRIGHT_ENGINEER: "playwright-engineer.md",
    AgentRole.FAILURE_ANALYZER: "failure-analyzer.md",
    AgentRole.QA_REVIEWER: "qa-reviewer.md",
}

COMMON_REQUIRED_SECTIONS: tuple[str, ...] = (
    "## Purpose",
    "## Role",
    "## Tools",
    "## Structured output",
    "## Steering compliance",
    "## Skills",
    "## Failure handling",
    "## Security",
    "## Input contract",
    "## Output contract",
    "## Evidence and constraints",
    "## Implementation reference",
)

MCP_AGENT_ROLES: frozenset[AgentRole] = frozenset(
    {
        AgentRole.PLAYWRIGHT_ENGINEER,
        AgentRole.FAILURE_ANALYZER,
        AgentRole.QA_REVIEWER,
    }
)


def agent_contract_path(role: AgentRole) -> Path:
    return _AGENT_DIR / _ROLE_FILES[role]


def required_sections_for(role: AgentRole) -> tuple[str, ...]:
    sections = COMMON_REQUIRED_SECTIONS
    if role in MCP_AGENT_ROLES:
        return sections + ("## MCP",)
    return sections


def validate_agent_contract_markdown(content: str, role: AgentRole) -> list[str]:
    """Return missing section headings; empty list means the contract is complete."""

    missing = [section for section in required_sections_for(role) if section not in content]
    return missing


_TITLE_TO_ROLE: dict[str, AgentRole] = {
    "# Requirement Analyzer Agent": AgentRole.REQUIREMENT_ANALYZER,
    "# Test Planner Agent": AgentRole.TEST_PLANNER,
    "# Playwright Engineer Agent": AgentRole.PLAYWRIGHT_ENGINEER,
    "# Failure Analyzer Agent": AgentRole.FAILURE_ANALYZER,
    "# QA Reviewer Agent": AgentRole.QA_REVIEWER,
}


def role_from_kiro_system_prompt(system: str) -> AgentRole:
    first_line = system.splitlines()[0].strip() if system.splitlines() else ""
    try:
        return _TITLE_TO_ROLE[first_line]
    except KeyError as exc:
        raise ValueError(f"Unknown Kiro agent contract title: {first_line!r}") from exc


@lru_cache(maxsize=len(AgentRole))
def load_kiro_agent_prompt(role: AgentRole) -> str:
    path = agent_contract_path(role)
    content = path.read_text(encoding="utf-8").strip()
    missing = validate_agent_contract_markdown(content, role)
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"{path}: missing required sections: {joined}")
    return content
