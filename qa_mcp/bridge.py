"""Playwright MCP bridge notes and lightweight target preflight for the Python runtime."""

from __future__ import annotations

import json
import urllib.error
from collections.abc import Mapping
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from qa_mcp.config import PlaywrightMCPConfig

_REPO_ROOT = Path(__file__).resolve().parent.parent
_KIRO_MCP_SETTINGS = _REPO_ROOT / ".kiro" / "settings" / "mcp.json"


@dataclass(frozen=True, slots=True)
class MCPBridgeStatus:
    kiro_settings_present: bool
    playwright_server_declared: bool
    base_url: str
    target_reachable: bool | None
    target_http_status: int | None
    note: str


def load_kiro_playwright_mcp_declared() -> bool:
    if not _KIRO_MCP_SETTINGS.is_file():
        return False
    try:
        document = json.loads(_KIRO_MCP_SETTINGS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    servers = document.get("mcpServers")
    return isinstance(servers, dict) and "playwright" in servers


def playwright_bridge_status(environ: Mapping[str, str] | None = None) -> MCPBridgeStatus:
    """Summarize MCP config. Kiro IDE uses `.kiro/settings/mcp.json`; Python uses preflight + file tools."""

    config = PlaywrightMCPConfig.from_env(environ)
    declared = load_kiro_playwright_mcp_declared()
    reachable: bool | None = None
    http_status: int | None = None
    try:
        request = urllib.request.Request(config.base_url, method="GET")
        with urllib.request.urlopen(request, timeout=3) as response:
            http_status = response.status
            reachable = 200 <= response.status < 500
    except urllib.error.HTTPError as exc:
        http_status = exc.code
        reachable = False
    except (urllib.error.URLError, TimeoutError, ValueError):
        reachable = False

    note = (
        "Playwright MCP is configured for Kiro/Cursor via .kiro/settings/mcp.json. "
        "The Python agent runtime performs target preflight and file-tool writes; "
        "full MCP tool calls from Python require the IDE MCP session or a future stdio bridge."
    )
    if http_status == 503:
        note += (
            " ShopDemo (or proxy on SHOPDEMO_BASE_URL) returned HTTP 503 — start the app "
            "under shopdemo/ and confirm http://localhost:3000 returns 200 before MCP navigation."
        )
    elif reachable is False and http_status is None:
        note += (
            " Target is not reachable (connection refused or timeout). Clone/start ShopDemo "
            "and set SHOPDEMO_BASE_URL in .env to match PLAYWRIGHT_BASE_URL in mcp.json."
        )

    return MCPBridgeStatus(
        kiro_settings_present=_KIRO_MCP_SETTINGS.is_file(),
        playwright_server_declared=declared,
        base_url=config.base_url,
        target_reachable=reachable,
        target_http_status=http_status,
        note=note,
    )
