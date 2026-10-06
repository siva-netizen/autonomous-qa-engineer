# Structured Agent Output Contracts — Tasks

- [x] Add `StructuredAgentOutput`, evidence parsing, role payload rules, and typed validation errors to `agents/contracts.py`.
- [x] Enrich `AgentResult` with the validated structured output while preserving raw content compatibility.
- [x] Parse and validate Groq JSON in `BaseAgent.run()` and derive lifecycle/evidence from the structured output.
- [x] Add deterministic fixtures/tests for all five roles, malformed responses, mismatches, traceability, and evidence gates.
- [x] Run targeted and full validation, then record commands, results, and any deferred live-provider work here.

## Traceability

- REQ-AOC-001/002/003 → `StructuredAgentOutput.from_json()` and malformed/mismatch tests.
- REQ-AOC-004 → role-specific payload tests for Requirement Analyzer, Test Planner, Playwright Engineer, Failure Analyzer, and QA Reviewer.
- REQ-AOC-005/006 → lifecycle, passed-outcome, evidence-reference, and evidence-gate tests.
- REQ-AOC-007/008 → `AgentResult.output`, raw-content compatibility, and independent multi-agent runtime tests.
- REQ-AOC-009/010 → fake transport, security scan, and no-live-provider validation.

## Verification evidence

- `.venv/bin/python -m pytest -q`: 21 passed.
- Targeted structured-output/runtime tests: 16 passed.
- `.venv/bin/python -m mypy agents services playwright mcp reports`: no issues in 14 source files.
- `.venv/bin/python scripts/security_scan.py`: passed; 318 text files checked.
- `npm run validate:scaffold`: passed; 51 required files present.
- `npm run typecheck`: passed.
- `npm test`: 1 TypeScript unit test passed.
- `npm run test:e2e -- --project=chromium`: 1 real ShopDemo Playwright test passed.
- Kiro JSON parsing and `git diff --check`: passed.

## Deviations and setup notes

- No provider live call was made. The feature is validated with deterministic fake provider responses; live testing remains gated on a local `GEMINI_API_KEY`.
- The structured output contract deliberately does not introduce an agent workflow. Callers still select one agent or an explicit subset in order.
- Browser evidence remains external to reasoning outputs and must reference real Playwright/MCP artifacts before an execution result can claim `passed`.
