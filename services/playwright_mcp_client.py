"""Call Playwright MCP over stdio from the Python agent runtime."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Callable, Sequence
from typing import Any

from qa_mcp.config import PlaywrightMCPConfig

PhaseCallback = Callable[[str], None]


class PlaywrightMCPError(RuntimeError):
    """Raised when Playwright MCP cannot complete a requested action."""


async def _inspect_async(base_url: str, *, on_phase: PhaseCallback | None = None) -> dict[str, Any]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    config = PlaywrightMCPConfig.from_env()
    phase = on_phase or (lambda _message: None)
    env = os.environ.copy()
    env["PLAYWRIGHT_BASE_URL"] = base_url.rstrip("/")

    params = StdioServerParameters(
        command=config.command,
        args=["--yes", config.package],
        env=env,
    )
    tools_called: list[str] = []
    phase("Tool · playwright-mcp · initialize")
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_names = [tool.name for tool in (await session.list_tools()).tools]
            navigate = "browser_navigate" if "browser_navigate" in tool_names else None
            snapshot = "browser_snapshot" if "browser_snapshot" in tool_names else None
            if navigate is None:
                raise PlaywrightMCPError(
                    f"browser_navigate not in MCP tools: {', '.join(tool_names[:12])}"
                )
            phase("Tool · playwright-mcp · browser_navigate")
            await session.call_tool(navigate, {"url": base_url})
            tools_called.append(navigate)
            snapshot_text = ""
            if snapshot is not None:
                phase("Tool · playwright-mcp · browser_snapshot")
                result = await session.call_tool(snapshot, {})
                tools_called.append(snapshot)
                snapshot_text = _tool_result_text(result)
            return {
                "base_url": base_url,
                "tools_called": tools_called,
                "available_tools": tool_names,
                "dom_snapshot": snapshot_text[:120_000],
            }


def _tool_result_text(result: Any) -> str:
    content = getattr(result, "content", None)
    if not content:
        return str(result)
    chunks: list[str] = []
    for item in content:
        text = getattr(item, "text", None)
        if isinstance(text, str):
            chunks.append(text)
    return "\n".join(chunks) if chunks else str(content)


def inspect_target(
    base_url: str | None = None,
    *,
    on_phase: PhaseCallback | None = None,
) -> dict[str, Any]:
    """Synchronously run a minimal Playwright MCP navigate + snapshot sequence."""

    url = (base_url or PlaywrightMCPConfig.from_env().base_url).rstrip("/")
    try:
        return asyncio.run(_inspect_async(url, on_phase=on_phase))
    except PlaywrightMCPError:
        raise
    except Exception as exc:
        raise PlaywrightMCPError(f"Playwright MCP failed: {type(exc).__name__}: {exc}") from exc
