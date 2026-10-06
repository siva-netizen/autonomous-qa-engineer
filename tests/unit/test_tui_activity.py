from __future__ import annotations

from agents.tui_widgets import format_activity_phase


def test_activity_phase_icons() -> None:
    assert "🤖" in format_activity_phase("Agent · Test Planner")
    assert "📁" in format_activity_phase("Tool · file-tools · read")
    assert "🌐" in format_activity_phase("Tool · playwright-mcp · preflight")
