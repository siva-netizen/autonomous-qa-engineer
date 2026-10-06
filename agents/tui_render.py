"""Rich render helpers for the QA engineer TUI."""

from __future__ import annotations

from rich.markdown import Markdown
from textual.widgets import RichLog


def write_assistant_markdown(log: RichLog, heading: str, body: str) -> None:
    """Write a labeled assistant reply with markdown body rendering."""

    log.write(heading)
    log.write(Markdown(body))
