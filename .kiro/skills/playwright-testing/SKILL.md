# Skill: Playwright Testing

## Use when

Generating, reviewing, or executing browser tests against ShopDemo. State explicitly: **Applying the Playwright Testing Skill.**

## Rules

1. Use Playwright MCP for navigation, DOM inspection, user actions, screenshots, console errors, and relevant network evidence.
2. Inspect target routes and DOM before writing locators.
3. Prefer `data-testid`, accessible roles, labels, and stable semantic text in that order when the target supports them.
4. Use web-first assertions and explicit state waits; do not add arbitrary sleeps.
5. Isolate browser contexts and test data.
6. Capture traces on retry/failure and screenshots at the failure point.
7. Keep requirement/scenario IDs in titles and artifact metadata.
8. A generated file is not evidence. Only real browser execution can produce pass/fail.

## Anti-patterns

Do not guess selectors, call syntax validation a pass, swallow timeouts, bypass MCP for hidden browser state, or classify every assertion failure as an application defect.
