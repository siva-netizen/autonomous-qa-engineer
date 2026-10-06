# Implementation Plan

## Completed baseline

- Read `HANDOFF.md` and `SPEC.md` before implementation.
- Created Kiro steering, feature specs, Skills, agent contracts, hooks, MCP settings, and environment templates.
- Checked out ShopDemo at revision `ac0adf4`, inspected its routes, selectors, MSW handlers, deterministic data, auth, cart, checkout, and failure boundaries.
- Started ShopDemo at `http://localhost:3000` and captured real browser baseline evidence under ignored `artifacts/shopdemo-baseline/`.
- Added and executed `tests/e2e/shopdemo-baseline.spec.ts` with one real Chromium test passing.
- Added Python 3.11+ independent agent foundation with Gemini environment configuration, fake transport tests, selected parallel dispatch, Playwright MCP contracts, and evidence/report contracts.

## Current architecture decision

The five QA agents are independently invokable. A caller selects one or more roles and may dispatch them in parallel. The runtime does not encode a hidden Requirement Analyzer → Test Planner → Playwright Engineer workflow. Any artifact handoff is explicit caller data.

## Next phases

### Phase 1 — live provider and agent output schemas

1. Create a Gemini API key in Google AI Studio.
2. Set the new value locally in `.env` as `GEMINI_API_KEY`.
3. Add structured JSON output validation for each role, preserving `REQ-*`, `TC-*`, assumptions, and evidence constraints.
4. Run one live agent call and store only redacted metadata, not prompts containing secrets.

### Phase 2 — Playwright MCP adapter

1. Validate the pinned Playwright MCP package locally.
2. Implement the MCP stdio/client adapter behind `playwright/contracts.py`.
3. Route all browser navigation, DOM inspection, actions, screenshots, console, and network evidence through that adapter.
4. Keep the existing Playwright Test baseline as independent execution evidence.

### Phase 3 — traceable reporting and review

1. Persist generated agent outputs separately from executed browser records.
2. Implement failure classification with observed/expected behavior, confidence, evidence, and recommended action.
3. Add the independent QA Reviewer report path and requirement coverage calculation.

### Phase 4 — controlled defects and expanded edge cases

After the clean baseline is preserved, add a reproducible defect mechanism and tests for empty/ambiguous requirements, missing selectors, timeouts, auth expiration, network failures, DOM drift, and invalid generated tests.

## Known findings

- ShopDemo production build passed.
- ShopDemo lint has pre-existing React hook errors and image warnings; the target was not modified.
- ShopDemo dependency audit reports findings; no automatic upgrade was applied.
- Git author is configured locally as `siva-netizen <sivasabarivel008@gmail.com>`.
- GitHub CLI account switching remains pending separate authentication for `siva-netizen`.
