"""Read Playwright MCP settings without handling secrets."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class PlaywrightMCPConfig:
    command: str = "npx"
    package: str = "@playwright/mcp@0.0.31"
    base_url: str = "http://localhost:3000"

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "PlaywrightMCPConfig":
        values = os.environ if environ is None else environ
        return cls(
            command=values.get("PLAYWRIGHT_MCP_COMMAND", "npx").strip() or "npx",
            package=values.get("PLAYWRIGHT_MCP_PACKAGE", "@playwright/mcp@0.0.31").strip(),
            base_url=values.get("SHOPDEMO_BASE_URL", "http://localhost:3000").strip().rstrip("/"),
        )
