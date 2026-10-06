"""Protocols for real browser evidence supplied by Playwright MCP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class BrowserEvidence:
    kind: str
    path: str
    description: str


class PlaywrightMCP(Protocol):
    def navigate(self, url: str) -> None: ...

    def inspect_dom(self, selector: str | None = None) -> str: ...

    def click(self, selector: str) -> None: ...

    def fill(self, selector: str, value: str) -> None: ...

    def select(self, selector: str, value: str) -> None: ...

    def screenshot(self, path: str, *, full_page: bool = True) -> BrowserEvidence: ...
