# Skill: Failure Analysis

## Use when

A real execution has failed or produced incomplete evidence.

## Required input

Use the test title, requirement/scenario IDs, assertion or runtime error, stack, observed URL/state, screenshot/trace, console output, network information, and environment metadata when available.

## Classification rules

- **Application bug:** evidence shows the product violated an explicit expected behavior after the test and environment were validated.
- **Test bug:** generated steps, assertion, fixture, or locator is invalid for the inspected product.
- **Environment failure:** target, browser, dependency, or service was unavailable or misconfigured.
- **Network/authentication/timeout/selector:** use the specific category when evidence supports it; these are not automatically product defects.
- **Unknown:** use when evidence is insufficient.

Always report observed behavior separately from expected behavior. Include confidence from 0 to 1, evidence paths, missing evidence, and a recommended next action. Never invent stack traces, screenshots, requests, or root causes.
