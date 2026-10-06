# Multi-Agent Groq Foundation — Tasks

- [x] Update Python-first steering, repository structure, security, and testing guidance.
- [x] Add `.env.example` Groq variables and document key rotation/no-secret policy.
- [x] Update the five `.kiro/agents/*.md` contracts with tools, inputs, outputs, evidence, and prohibited claims.
- [x] Add `agents/` typed contracts, base agent, five independent specialized agents, registry, and explicit selected-agent runtime.
- [x] Add `services/groq_client.py` with environment configuration, bounded HTTP transport, model defaults, fallback support, and safe errors.
- [x] Add Playwright MCP and report contracts without simulating browser execution.
- [x] Add required JSON hooks for tests, lint/type checks, and security scanning.
- [x] Add unit/integration/security tests for configuration, dispatch, fake transport, empty inputs, evidence invariants, and secret absence.
- [x] Run Python checks and update this task file with completed items and deviations.
- [ ] Run a live Groq invocation after the user supplies a newly rotated local `GROQ_API_KEY`.

## Verification evidence

- `.venv/bin/python -m pytest -q`: 9 passed.
- `.venv/bin/python -m mypy agents services playwright mcp reports`: no issues in 14 source files.
- `.venv/bin/python scripts/security_scan.py`: passed; no committed secret-shaped values or relevant prompt-injection markers.
- `npm run validate:scaffold`: passed; 48 required files present.
- `npm run typecheck`: passed.
- `npm test`: 1 TypeScript unit test passed after Vitest was restricted to `tests/**/*.test.ts`.
- `npm run test:e2e -- --project=chromium`: 1 real ShopDemo Playwright test passed.

## Deviations and setup notes

- The supplied Groq key was not stored or used because it was exposed in chat; revoke/rotate it before local live testing.
- The primary model is configured as `llama-3.3-70b-versatile`; the optional fallback is `openai/gpt-oss-120b`.
- Local Git identity is set to `siva-netizen <sivasabarivel008@gmail.com>`.
- `gh` remains authenticated as `sivasabarivel-aivar`; switching to `siva-netizen` requires a separate interactive GitHub login/token and is not performed with a Groq key.
- The runtime supports independent and caller-selected multi-agent invocation; no mandatory agent workflow was implemented. Parallel dispatch was removed in a later MVP revision.
