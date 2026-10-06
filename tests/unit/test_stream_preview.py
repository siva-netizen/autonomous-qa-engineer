from __future__ import annotations

from agents.tui_widgets import build_stream_preview_text


def test_stream_preview_text_treats_json_brackets_as_literal() -> None:
    rendered = build_stream_preview_text(
        "Streaming",
        '{"role": "requirement-analyzer", "payload": []}',
    )
    assert "requirement-analyzer" in rendered.plain
    assert "[/]" not in rendered.plain
