"""Normalize and persist Playwright test artifacts from structured agent output."""

from __future__ import annotations

import re

from agents.contracts import AgentResult

_CODE_FENCE = re.compile(r"```(?:typescript|ts|javascript|js)?\s*\n([\s\S]*?)```", re.IGNORECASE)


def normalize_generated_test(result: AgentResult) -> str | None:
    if result.output is None:
        return None
    raw = result.output.payload.get("generated_test")
    if not isinstance(raw, str) or not raw.strip():
        return None
    text = raw.strip()
    if _looks_like_playwright_source(text):
        return text if text.endswith("\n") else f"{text}\n"
    if text.endswith(".spec.ts") and "\n" not in text and len(text) < 260:
        fenced = _CODE_FENCE.search(result.output.summary)
        if fenced:
            body = fenced.group(1).strip()
            if _looks_like_playwright_source(body):
                return f"{body}\n"
        return None
    fenced = _CODE_FENCE.search(text) or _CODE_FENCE.search(result.output.summary)
    if fenced and _looks_like_playwright_source(fenced.group(1)):
        return f"{fenced.group(1).strip()}\n"
    return None


def _looks_like_playwright_source(text: str) -> bool:
    lowered = text.lower()
    return (
        "import" in lowered
        and ("@playwright/test" in lowered or "playwright" in lowered)
        and "test(" in lowered
    )
