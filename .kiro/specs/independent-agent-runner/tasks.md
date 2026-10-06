# Independent Agent Runner — Tasks

- [x] Implement parser and explicit role normalization in `agents/run.py`.
- [x] Implement sequential dispatch and safe JSON serialization.
- [x] Add production Gemini client construction and injectable fake-client helper boundary.
- [x] Add CLI tests for valid selection, sequential multi-agent dispatch, malformed options, duplicates, and missing credentials.
- [x] Update README/scaffold artifacts with the correct `python -m` and `uv run --no-sync python -m` commands.
- [x] Run all validation and record evidence here.

## Traceability

- REQ-RUN-001/002/009 → explicit role parser and sequential dispatch tests.
- REQ-RUN-003/007 → argument/context/duplicate validation tests.
- REQ-RUN-004/005/006 → environment boundary, JSON serialization, and secret-safe error tests.
- REQ-RUN-008 → fake reasoning client smoke tests.

## Verification evidence

- `.venv/bin/python -m pytest -q`: 25 passed.
- `tests/unit/test_agent_run.py`: 4 passed.
- `.venv/bin/python -m mypy agents services playwright mcp reports`: no issues in 15 source files.
- `.venv/bin/python scripts/security_scan.py`: passed; 327 text files checked.
- `npm run validate:scaffold`: passed; 55 required files present.
- `npm run typecheck`: passed.
- `npm test`: 1 TypeScript unit test passed.
- `npm run test:e2e -- --project=chromium`: 1 real ShopDemo Playwright test passed.
- `uv run --no-sync python -m agents.run --help`: passed.
- Kiro JSON validation and `git diff --check`: passed.

## Usage correction

`uv agents.run` is invalid because `agents.run` is a Python module, not a uv subcommand. Use:

```bash
python -m agents.run --agents requirement-analyzer,qa-reviewer --request-id REQ-RUN-001 --prompt "Review the ShopDemo checkout requirement." --requirement-ids REQ-RA-001
```

Or, preserving the existing environment:

```bash
uv run --no-sync python -m agents.run --agents requirement-analyzer,qa-reviewer --request-id REQ-RUN-001 --prompt "Review the ShopDemo checkout requirement." --requirement-ids REQ-RA-001
```

For interactive QA chat, use `python -m agents.tui` (see `.kiro/specs/qa-engineer-tui/`).

## Deferred live validation

No live Gemini call was made. A local `GEMINI_API_KEY` is required before invoking the runner without an injected fake client.
