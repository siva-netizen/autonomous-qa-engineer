"""Bridge worker-thread activity + streaming callbacks to Textual widgets."""

from __future__ import annotations

import time
from collections.abc import Callable

from agents.tui_widgets import ActivityRail, StreamPreview

_STREAM_UI_INTERVAL_SECONDS = 0.08

StreamCallback = Callable[[str], None]
PhaseCallback = Callable[[str], None]
PostToUi = Callable[[Callable[[], None]], None]


def build_ui_callbacks(
    activity: ActivityRail,
    stream: StreamPreview,
    *,
    stream_heading: str,
    post_to_ui: PostToUi,
) -> tuple[PhaseCallback, StreamCallback, Callable[[], None]]:
    buffer: list[str] = []
    last_ui_update = 0.0

    def on_phase(message: str) -> None:
        post_to_ui(lambda m=message: activity.set_phase(m))

    def flush_stream() -> None:
        if not buffer:
            return
        body = "".join(buffer)
        post_to_ui(lambda b=body: stream.show_stream(stream_heading, b))

    def on_stream(delta: str) -> None:
        nonlocal last_ui_update
        buffer.append(delta)
        now = time.monotonic()
        if now - last_ui_update < _STREAM_UI_INTERVAL_SECONDS:
            return
        last_ui_update = now
        flush_stream()

    return on_phase, on_stream, flush_stream
