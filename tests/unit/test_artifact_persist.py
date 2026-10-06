from __future__ import annotations

from agents.contracts import AgentRole, AgentResult, Lifecycle, StructuredAgentOutput


def test_normalize_generated_test_from_payload_source() -> None:
    output = StructuredAgentOutput(
        request_id="REQ-1",
        role=AgentRole.PLAYWRIGHT_ENGINEER,
        summary="done",
        lifecycle=Lifecycle.GENERATED,
        requirement_ids=("REQ-RA-001",),
        scenario_ids=("TC-001",),
        payload={
            "generated_test": (
                "import { test, expect } from '@playwright/test';\n"
                "test('x', async ({ page }) => { await page.goto('/'); });\n"
            ),
            "evidence_plan": ["trace"],
        },
    )
    result = AgentResult(
        request_id="REQ-1",
        role=AgentRole.PLAYWRIGHT_ENGINEER,
        content="{}",
        output=output,
    )
    from services.artifact_persist import normalize_generated_test

    normalized = normalize_generated_test(result)
    assert normalized is not None
    assert "@playwright/test" in normalized
