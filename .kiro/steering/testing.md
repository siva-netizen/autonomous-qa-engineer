# Testing Strategy

1. Unit-test contracts, environment parsing, prompt/spec validation, role lookup, TUI orchestrator parsing, QA chat session history, and lifecycle invariants.
2. Integration-test independent agent calls and sequential multi-agent selection using a deterministic fake Gemini transport.
3. Security-test source/config paths for embedded keys, unsafe auth logging, and prompt-injection markers in untrusted inputs.
4. Test the Playwright MCP boundary with protocol/adapter fakes; never turn a fake browser result into a pass claim.
5. Run real Playwright tests against the inspected ShopDemo target with screenshots/traces on failure.
6. Cover empty/ambiguous requirements, missing selectors, target timeouts, auth expiry, network errors, DOM drift, and invalid generated tests.
7. Measure agent dispatch latency and browser execution duration in result metadata where implemented.

Every `REQ-*` requirement maps to tests and evidence. A passing report requires an actual execution record. Failure classification must include observed behavior, expected behavior, evidence, confidence, and recommended action.
