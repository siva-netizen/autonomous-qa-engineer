from __future__ import annotations

import json
from collections.abc import Sequence
from typing import Any

from agents.contracts import AgentRole
from agents.kiro_contracts import role_from_kiro_system_prompt
from services.gemini_client import ChatCompletion, ChatMessage


def _role_payload(role: AgentRole) -> dict[str, Any]:
    if role is AgentRole.REQUIREMENT_ANALYZER:
        return {"requirements": [{"id": "REQ-RA-001"}]}
    if role is AgentRole.TEST_PLANNER:
        return {"scenarios": [{"id": "TC-001"}]}
    if role is AgentRole.PLAYWRIGHT_ENGINEER:
        return {
            "generated_test": (
                "import { test, expect } from '@playwright/test';\n"
                "test('generated smoke', async ({ page }) => {\n"
                "  await page.goto('/');\n"
                "  await expect(page).toHaveTitle(/.+/);\n"
                "});\n"
            ),
            "evidence_plan": ["trace", "screenshot"],
        }
    if role is AgentRole.FAILURE_ANALYZER:
        return {
            "classification": "unknown",
            "observed_behavior": "No execution was supplied.",
            "expected_behavior": "The request should be analyzed.",
            "confidence": 0.2,
            "recommended_action": "Collect execution evidence.",
        }
    return {
        "coverage_gaps": [],
        "evidence_gaps": [],
        "verification_recommendation": "Run the selected test.",
    }


class FakeGeminiClient:
    """Deterministic Gemini stand-in keyed off the Kiro markdown system prompt."""

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        model: str | None = None,
    ) -> ChatCompletion:
        request_data = json.loads(messages[1].content.split("\n\n", 1)[1])
        role = role_from_kiro_system_prompt(messages[0].content)
        document = {
            "request_id": request_data["request_id"],
            "role": role.value,
            "summary": f"Fake result for {role.value}",
            "lifecycle": "generated",
            "requirement_ids": list(request_data["requirement_ids"]),
            "scenario_ids": ["TC-001"],
            "payload": _role_payload(role),
            "assumptions": [],
            "open_questions": [],
            "evidence": [],
            "metadata": {"transport": "fake"},
        }
        return ChatCompletion(
            content=json.dumps(document),
            model=model or "fake-model",
            usage={"total_tokens": 1},
        )
