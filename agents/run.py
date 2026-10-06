"""Command-line entry point for explicit independent agent dispatch."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from agents.contracts import AgentRequest, AgentResult, AgentRole
from agents.registry import AgentRegistry
from agents.tool_runner import AgentToolRunner
from services.gemini_client import (
    GeminiChatClient,
    GeminiConfigurationError,
    GeminiRequestError,
    ReasoningClient,
)


def _parse_roles(raw: str) -> tuple[AgentRole, ...]:
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    if not values:
        raise ValueError("--agents must contain at least one agent role")
    roles: list[AgentRole] = []
    for value in values:
        try:
            roles.append(AgentRole(value))
        except ValueError as exc:
            supported = ", ".join(role.value for role in AgentRole)
            raise ValueError(f"unknown agent role '{value}'; choose from: {supported}") from exc
    if len(set(roles)) != len(roles):
        raise ValueError("--agents must not contain duplicate roles")
    return tuple(roles)


def _parse_csv(raw: str, option_name: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    if not values and raw.strip():
        raise ValueError(f"{option_name} contains no usable values")
    return values


def _parse_context(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("--context-json must be valid JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("--context-json must contain a JSON object")
    return value


def _result_to_dict(result: AgentResult) -> dict[str, Any]:
    serialized: dict[str, Any] = {
        "request_id": result.request_id,
        "role": result.role.value,
        "lifecycle": result.lifecycle.value,
        "model": result.model,
        "evidence": list(result.evidence),
        "metadata": dict(result.metadata),
    }
    if result.output is not None:
        serialized["output"] = result.output.to_dict()
    return serialized


def run_request(
    request: AgentRequest,
    roles: Sequence[AgentRole],
    *,
    client: ReasoningClient | None = None,
) -> dict[AgentRole, AgentResult]:
    """Run exactly the caller-selected roles; no implicit workflow is added."""

    request.validate()
    if not roles:
        raise ValueError("at least one agent role must be selected")
    if len(set(roles)) != len(roles):
        raise ValueError("selected agent roles must be unique")
    registry = AgentRegistry.from_client(client or GeminiChatClient())
    runner = AgentToolRunner()
    return {
        role: runner.run(registry.get(role), request)
        for role in roles
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Invoke explicitly selected QA agents independently in argument order."
    )
    parser.add_argument(
        "--agents",
        required=True,
        help="Comma-separated roles: requirement-analyzer,test-planner,playwright-engineer,failure-analyzer,qa-reviewer",
    )
    parser.add_argument("--request-id", required=True, help="Traceable request identifier.")
    parser.add_argument("--prompt", required=True, help="Task prompt supplied to each selected agent.")
    parser.add_argument(
        "--requirement-ids",
        default="",
        help="Optional comma-separated requirement IDs, for example REQ-RA-001.",
    )
    parser.add_argument(
        "--context-json",
        default="{}",
        help="Optional JSON object passed as caller context.",
    )
    return parser


def main(argv: Sequence[str] | None = None, *, client: ReasoningClient | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        roles = _parse_roles(args.agents)
        requirement_ids = _parse_csv(args.requirement_ids, "--requirement-ids")
        context = _parse_context(args.context_json)
        request = AgentRequest(
            request_id=args.request_id,
            prompt=args.prompt,
            requirement_ids=requirement_ids,
            context=context,
        )
        results = run_request(request, roles, client=client)
        payload = {
            "request_id": request.request_id,
            "selected_agents": [role.value for role in roles],
            "results": {role.value: _result_to_dict(result) for role, result in results.items()},
        }
        print(json.dumps(payload, default=str, sort_keys=True))
        return 0
    except (GeminiConfigurationError, GeminiRequestError, ValueError, KeyError) as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
