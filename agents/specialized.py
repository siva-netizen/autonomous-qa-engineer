"""Specialized agent definitions; each can be invoked without a pipeline."""

from __future__ import annotations

from agents.base import BaseAgent
from agents.contracts import AgentRole, AgentSpec, AgentTool
from agents.kiro_contracts import load_kiro_agent_prompt
from services.gemini_client import ReasoningClient


def _spec(
    role: AgentRole,
    name: str,
    description: str,
    tools: tuple[AgentTool, ...],
    input_contract: str,
    output_contract: str,
    prohibited_claims: tuple[str, ...],
) -> AgentSpec:
    return AgentSpec(
        role=role,
        name=name,
        description=description,
        tools=tools,
        input_contract=input_contract,
        output_contract=output_contract,
        prohibited_claims=prohibited_claims,
        system_prompt=load_kiro_agent_prompt(role),
    )


class RequirementAnalyzer(BaseAgent):
    spec = _spec(
        AgentRole.REQUIREMENT_ANALYZER,
        "Requirement Analyzer",
        "Interpret requirements into explicit, traceable QA obligations.",
        (AgentTool.GEMINI, AgentTool.FILES),
        "User story, acceptance criteria, and optional specification references.",
        "REQ-RA-* requirements, acceptance criteria, assumptions, questions, and scenario candidates.",
        ("Do not claim browser behavior.", "Do not produce PASS or FAIL."),
    )


class TestPlanner(BaseAgent):
    spec = _spec(
        AgentRole.TEST_PLANNER,
        "Test Planner",
        "Design prioritized traceable scenarios from validated requirements.",
        (AgentTool.GEMINI, AgentTool.FILES),
        "Validated requirements, target notes, and assumptions.",
        "REQ-TP-* mappings and TC-* scenarios with expected results and execution strategy.",
        ("Do not report execution outcomes.", "Do not invent unsupported product behavior."),
    )


class PlaywrightEngineer(BaseAgent):
    spec = _spec(
        AgentRole.PLAYWRIGHT_ENGINEER,
        "Playwright Engineer",
        "Generate executable browser tests from inspected scenarios.",
        (AgentTool.GEMINI, AgentTool.FILES, AgentTool.PLAYWRIGHT_MCP),
        "Scenario, target inspection notes, base URL, and test conventions.",
        "Generated Playwright test, locator rationale, evidence plan, and unresolved issues.",
        ("Do not claim execution success.", "Do not guess selectors."),
    )


class FailureAnalyzer(BaseAgent):
    spec = _spec(
        AgentRole.FAILURE_ANALYZER,
        "Failure Analyzer",
        "Classify real execution failures conservatively from evidence.",
        (AgentTool.GEMINI, AgentTool.FILES, AgentTool.PLAYWRIGHT_MCP),
        "Execution result, error, stack, observed state, evidence, and expected behavior.",
        "Classification, observed/expected behavior, confidence, evidence gaps, severity, and next action.",
        ("Do not fabricate evidence.", "Do not call every assertion failure an application bug."),
    )


class QAReviewer(BaseAgent):
    spec = _spec(
        AgentRole.QA_REVIEWER,
        "QA Reviewer",
        "Independently review traceability, evidence, and false-positive risk.",
        (AgentTool.GEMINI, AgentTool.FILES, AgentTool.PLAYWRIGHT_MCP, AgentTool.GITHUB_MCP_READ),
        "Requirements, scenarios, generated tests, execution records, evidence, and analyses.",
        "Coverage gaps, evidence gaps, false-positive risks, and verification recommendation.",
        ("Do not upgrade unexecuted work to PASS.", "Do not hide contradictory evidence."),
    )


AGENT_CLASSES = {
    AgentRole.REQUIREMENT_ANALYZER: RequirementAnalyzer,
    AgentRole.TEST_PLANNER: TestPlanner,
    AgentRole.PLAYWRIGHT_ENGINEER: PlaywrightEngineer,
    AgentRole.FAILURE_ANALYZER: FailureAnalyzer,
    AgentRole.QA_REVIEWER: QAReviewer,
}
