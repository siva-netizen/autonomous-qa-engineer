from __future__ import annotations

from pathlib import Path

from agents.contracts import AgentRequest, AgentRole
from agents.registry import AgentRegistry
from agents.tool_runner import AgentToolRunner
from tests.support.fake_gemini import FakeGeminiClient


def test_playwright_engineer_writes_generated_test_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "SHOPDEMO_INSPECTION.md").write_text("# inspection\n", encoding="utf-8")

    import services.file_tools as file_tools

    monkeypatch.setattr(file_tools, "_REPO_ROOT", tmp_path)

    registry = AgentRegistry.from_client(FakeGeminiClient())
    agent = registry.get(AgentRole.PLAYWRIGHT_ENGINEER)
    request = AgentRequest(
        request_id="REQ-WRITE-001",
        prompt="Generate checkout smoke test",
        requirement_ids=("REQ-RA-001",),
    )
    phases: list[str] = []

    monkeypatch.setattr(
        "agents.tool_runner.inspect_target",
        lambda *_args, **_kwargs: {"tools_called": ["browser_navigate"], "dom_snapshot": "<fake/>"},
    )

    result = AgentToolRunner().run(agent, request, on_phase=phases.append)

    written = result.metadata.get("written_test_path")
    assert isinstance(written, str)
    assert Path(tmp_path / written).is_file()
    assert "import { test, expect }" in Path(tmp_path / written).read_text(encoding="utf-8")
    assert any("file-tools · write" in step for step in phases)
    assert any("playwright-mcp · preflight" in step for step in phases)
