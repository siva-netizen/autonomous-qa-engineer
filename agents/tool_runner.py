"""Execute declared agent tools (file I/O, MCP preflight) around Gemini structured output."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from contextlib import nullcontext
from dataclasses import replace
from typing import Any

from services.stream_context import stream_callback_scope

from agents.base import BaseAgent
from agents.contracts import AgentRequest, AgentResult, AgentRole, AgentTool
from qa_mcp.bridge import playwright_bridge_status
from services.artifact_persist import normalize_generated_test
from services.file_tools import (
    default_generated_test_path,
    read_context_files,
    write_repo_text,
)
from services.playwright_mcp_client import PlaywrightMCPError, inspect_target

PhaseCallback = Callable[[str], None]
StreamCallback = Callable[[str], None]


def _noop_phase(_message: str) -> None:
    return None


def _emit(on_phase: PhaseCallback, message: str) -> None:
    on_phase(message)


class AgentToolRunner:
    """Runs real file/MCP preflight steps, then the agent, then optional artifact persistence."""

    def run(
        self,
        agent: BaseAgent,
        request: AgentRequest,
        *,
        on_phase: PhaseCallback | None = None,
        on_stream: StreamCallback | None = None,
    ) -> AgentResult:
        phase = on_phase or _noop_phase
        stream_scope = (
            stream_callback_scope(on_stream) if on_stream is not None else nullcontext()
        )
        spec = agent.spec
        context: dict[str, Any] = dict(request.context)

        _emit(phase, f"Agent · {spec.name}")

        if AgentTool.FILES in spec.tools:
            _emit(phase, "Tool · file-tools · read")
            file_paths = tuple(context.get("context_files", ())) or None
            if file_paths:
                from services.file_tools import read_repo_text

                loaded = {
                    path: read_repo_text(str(path))
                    for path in file_paths
                    if isinstance(path, str)
                }
            else:
                loaded = read_context_files()
            context["file_context"] = loaded

        if AgentTool.PLAYWRIGHT_MCP in spec.tools:
            _emit(phase, "Tool · playwright-mcp · preflight")
            status = playwright_bridge_status()
            context["playwright_mcp"] = {
                "kiro_mcp_configured": status.playwright_server_declared,
                "base_url": status.base_url,
                "target_reachable": status.target_reachable,
                "target_http_status": status.target_http_status,
                "bridge_note": status.note,
            }
            if status.target_http_status == 503 or status.target_reachable is False:
                _emit(
                    phase,
                    "Tool · playwright-mcp · preflight warning (target unavailable or HTTP 503)",
                )
            elif status.target_reachable:
                try:
                    context["playwright_mcp_session"] = inspect_target(
                        status.base_url,
                        on_phase=phase,
                    )
                except PlaywrightMCPError as exc:
                    context["playwright_mcp_error"] = str(exc)

        _emit(phase, "Tool · gemini-reasoning")
        enriched = AgentRequest(
            request_id=request.request_id,
            prompt=request.prompt,
            requirement_ids=request.requirement_ids,
            context=context,
        )
        with stream_scope:
            result = agent.run(enriched)
        _emit(phase, "Structured output validation")

        if spec.role is AgentRole.PLAYWRIGHT_ENGINEER and result.output is not None:
            _emit(phase, "Tool · file-tools · write")
            written = self._persist_generated_test(result)
            if written is not None:
                metadata = dict(result.metadata)
                metadata["written_test_path"] = written
                result = replace(result, metadata=metadata)

        return result

    def _persist_generated_test(self, result: AgentResult) -> str | None:
        if result.output is None:
            return None
        code = normalize_generated_test(result)
        if code is None:
            return None
        relative = result.output.metadata.get("artifact_path")
        if not isinstance(relative, str) or not relative.strip():
            relative = default_generated_test_path(result.request_id)
        write_repo_text(relative, code)
        return relative
