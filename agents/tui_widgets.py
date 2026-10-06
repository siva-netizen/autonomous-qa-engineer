"""Textual widgets for the QA engineer TUI."""

from __future__ import annotations

from collections.abc import Iterator

from rich.text import Text

from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import LoadingIndicator, Static

_PHASE_ICONS: tuple[tuple[str, str], ...] = (
    ("Agent ·", "🤖"),
    ("Tool · file-tools · write", "💾"),
    ("Tool · file-tools · read", "📁"),
    ("Tool · file-tools", "📁"),
    ("Tool · playwright-mcp", "🌐"),
    ("Tool · gemini-reasoning", "✦"),
    ("Structured output", "✓"),
)


def format_activity_phase(message: str) -> str:
    for prefix, icon in _PHASE_ICONS:
        if message.startswith(prefix):
            return f"{icon}  {message}"
    return f"▸  {message}"


def _is_tool_phase(message: str) -> bool:
    return message.startswith("Tool ·")


def build_stream_preview_text(heading: str, body: str, *, max_chars: int = 1200) -> Text:
    preview = body if len(body) <= max_chars else f"…{body[-max_chars:]}"
    content = Text()
    content.append(f"{heading}\n", style="bold #58ff58")
    content.append(preview, style="dim")
    return content


class StreamPreview(Static):
    """Live token preview while Gemini streams."""

    DEFAULT_CSS = """
    StreamPreview {
        display: none;
        height: auto;
        max-height: 5;
        overflow-y: auto;
        background: #0a1f0a;
        border: solid #1faa59;
        padding: 0 1;
        color: #9dff9d;
    }
    StreamPreview.-live {
        display: block;
    }
    """

    def show_stream(self, heading: str, body: str) -> None:
        """Render streamed JSON/text without interpreting `[` as Rich markup."""

        self.add_class("-live")
        self.update(build_stream_preview_text(heading, body))

    def hide_stream(self) -> None:
        self.remove_class("-live")
        self.update("")


class ActivityRail(Vertical):
    """Spinner, current phase, and animated tool-call trail."""

    DEFAULT_CSS = """
    ActivityRail {
        display: none;
        height: auto;
    }
    ActivityRail.-active {
        display: block;
    }
    """

    message = reactive("")
    _last_phase = ""
    _trail_lines: list[str]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._trail_lines = []

    def compose(self) -> Iterator[Horizontal | Static]:
        with Horizontal(id="activity-head"):
            yield LoadingIndicator(id="spinner")
            yield Static("", id="activity-text")
        yield Static("", id="tool-trail")

    def start(self, message: str) -> None:
        self.message = message
        self._last_phase = message
        self.add_class("-active")
        self.add_class("-pulse")
        self.query_one("#activity-text", Static).update(format_activity_phase(message))
        self._trail_lines = []
        self.query_one("#tool-trail", Static).update("")
        self.query_one("#spinner", LoadingIndicator).remove_class("-hidden")

    def set_phase(self, message: str) -> None:
        if self._last_phase and _is_tool_phase(self._last_phase):
            self._append_tool_trail(self._last_phase, done=True)
        self.message = message
        self._last_phase = message
        self.add_class("-pulse")
        self.query_one("#activity-text", Static).update(format_activity_phase(message))
        if _is_tool_phase(message):
            self._append_tool_trail(message, done=False)

    def _append_tool_trail(self, message: str, *, done: bool) -> None:
        trail = self.query_one("#tool-trail", Static)
        icon = "✅" if done else "⏳"
        line = f"{icon} {format_activity_phase(message)}"
        if not done:
            self._trail_lines.append(line)
        elif self._trail_lines and self._trail_lines[-1].startswith("⏳"):
            self._trail_lines[-1] = line
        else:
            self._trail_lines.append(line)
        trail.update("\n".join(self._trail_lines[-6:]))

    def stop(self) -> None:
        if self._last_phase and _is_tool_phase(self._last_phase):
            self._append_tool_trail(self._last_phase, done=True)
        self.remove_class("-active")
        self.remove_class("-pulse")
        self.query_one("#activity-text", Static).update("")
        self.query_one("#tool-trail", Static).update("")


class IdleStatusRail(Horizontal):
    """Subtle ready line when not busy."""

    DEFAULT_CSS = """
    IdleStatusRail {
        height: 1;
        background: #0a2a0a;
        padding: 0 1;
        color: #4a9a4a;
    }
    IdleStatusRail.-hidden {
        display: none;
    }
    """

    def compose(self) -> Iterator[LoadingIndicator | Static]:
        yield Static("Ready — spinner and tool trail appear while agents run.", id="idle-text")

    def set_busy(self, busy: bool) -> None:
        if busy:
            self.add_class("-hidden")
        else:
            self.remove_class("-hidden")
