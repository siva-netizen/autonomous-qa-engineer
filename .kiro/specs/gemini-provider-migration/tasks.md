# Gemini Provider Migration — Tasks

- [x] Add canonical `services/gemini_client.py` with Gemini config, transport, errors, defaults, and fallback support.
- [x] Update agent imports and CLI construction to use the Gemini adapter.
- [x] Keep and document a deprecated compatibility shim for old Groq imports.
- [x] Update `.env.example`, README, docs, steering, agent contracts, and security scanning names.
- [x] Update deterministic provider tests and run all validation.
- [x] Record that the real `GEMINI_API_KEY` is supplied locally and no live provider call is performed by the implementation task.

## Traceability

- REQ-GEM-001/002/003/004/006 → Gemini client configuration, request, missing-key, fallback, and status tests.
- REQ-GEM-005 → provider-neutral runtime and structured-output regression tests.
- REQ-GEM-007/008 → documentation, scanner, import, and compatibility validation.

## Verification evidence

- `.venv/bin/python -m pytest -q`: 27 passed.
- `.venv/bin/python -m mypy agents services playwright mcp reports`: no issues in 16 source files.
- `.venv/bin/python scripts/security_scan.py`: passed; 333 text files checked.
- `npm run validate:scaffold`: passed; 59 required files present.
- `npm run typecheck`: passed.
- `npm test`: 1 TypeScript unit test passed.
- `npm run test:e2e -- --project=chromium`: 1 real ShopDemo Playwright test passed.
- Kiro JSON validation, compileall, and `git diff --check`: passed.
- Local `.env` audit: `GEMINI_API_KEY` is empty, Gemini model/base URL are configured, `.env` is ignored by Git, and no Groq provider variables remain.

## Local setup required

Enter the Gemini key locally in `.env` without sending it through chat:

```env
GEMINI_API_KEY=<your-gemini-api-key>
GEMINI_MODEL=gemini-3.1-flash-lite
GEMINI_FALLBACK_MODEL=
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
GEMINI_TIMEOUT_SECONDS=60
```

Load it before a live runner call:

```bash
set -a
source .env
set +a
```

No live Gemini request was made during repository validation.
