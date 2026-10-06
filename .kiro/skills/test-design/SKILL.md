# Skill: Test Design

## Use when

Designing scenarios from requirements or reviewing an agent-produced test plan.

## Rules

- Preserve explicit requirement IDs and map every scenario to at least one requirement.
- Cover positive, negative, boundary, empty, ambiguous, authentication, network, timeout, selector, and DOM-drift cases when supported by the input.
- Separate expected behavior from execution results; planning cannot produce PASS/FAIL.
- State assumptions and unresolved questions instead of inventing product behavior.
- Prefer the smallest scenario that proves one behavior and identify whether it needs Playwright MCP or deterministic code.
- Keep generated test titles and artifacts traceable with `REQ-*` and `TC-*` identifiers.
