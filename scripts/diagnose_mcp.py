#!/usr/bin/env python3
"""Check ShopDemo, Kiro MCP settings, and Gemini before live agent/MCP use."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa_mcp.bridge import load_kiro_playwright_mcp_declared, playwright_bridge_status
from qa_mcp.config import PlaywrightMCPConfig
from services.gemini_client import ChatMessage, GeminiChatClient, GeminiConfig, GeminiRequestError
from services.local_env import load_project_dotenv


def _check_mcp_json_env() -> list[str]:
    issues: list[str] = []
    path = ROOT / ".kiro" / "settings" / "mcp.json"
    if not path.is_file():
        issues.append("Missing .kiro/settings/mcp.json")
        return issues
    document = json.loads(path.read_text(encoding="utf-8"))
    env = document.get("mcpServers", {}).get("playwright", {}).get("env", {})
    base = env.get("PLAYWRIGHT_BASE_URL", "")
    if not base or base.startswith("${"):
        issues.append(
            "PLAYWRIGHT_BASE_URL in mcp.json is unset or still a ${...} placeholder — "
            "Kiro/Cursor does not expand .env there; use http://localhost:3000 (or your real URL)."
        )
    return issues


def main() -> int:
    load_project_dotenv()
    print("Autonomous QA Engineer — MCP / runtime diagnostics\n")

    config = PlaywrightMCPConfig.from_env()
    print(f"SHOPDEMO_BASE_URL (Python): {config.base_url}")
    status = playwright_bridge_status()
    print(f"Kiro playwright MCP declared: {status.playwright_server_declared}")
    print(f"Target reachable: {status.target_reachable}")
    if status.target_http_status is not None:
        print(f"Target HTTP status: {status.target_http_status}")
    for issue in _check_mcp_json_env():
        print(f"ISSUE: {issue}")

    if status.target_http_status == 503:
        print(
            "\nHTTP 503 on ShopDemo — MCP browser navigation will fail. "
            "Start ShopDemo (see README) until / returns 200."
        )
    elif status.target_reachable is False:
        print(
            "\nShopDemo not reachable — clone/start dummy-ecommerce under shopdemo/ "
            "and run its dev server on port 3000."
        )

    gemini = GeminiConfig.from_env()
    print(f"\nGEMINI_MODEL: {gemini.model}")
    print(f"GEMINI_API_KEY set: {bool(gemini.api_key)}")
    if gemini.api_key:
        try:
            GeminiChatClient(gemini).complete([ChatMessage("user", "Reply with exactly: ok")])
            print("Gemini chat: OK")
        except GeminiRequestError as exc:
            print(f"Gemini chat: FAIL — {exc}")
            if "503" in str(exc):
                print(
                    "  HTTP 503 from Gemini is provider overload — retry later or set "
                    "GEMINI_FALLBACK_MODEL=gemini-2.0-flash in .env"
                )

    print("\nNote: python -m agents.tui does not start Playwright MCP; use Kiro/Cursor MCP for browser tools.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
