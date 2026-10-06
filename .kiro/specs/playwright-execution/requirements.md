# Playwright Execution — Requirements

## Scope

Execute generated scenarios against the inspected local ShopDemo target and persist evidence-backed results.

## Requirements

- **PE-001:** Refuse execution when the target has not been inspected or the base URL is unavailable.
- **PE-002:** Execute generated Playwright tests against the real browser/application, not a simulated pass path.
- **PE-003:** Capture the result, duration, screenshot/trace where configured, console output, and relevant network failures.
- **PE-004:** Keep generated, executed, and verified lifecycle states distinct.
- **PE-005:** Preserve requirement and scenario IDs in test names and result artifacts.
- **PE-006:** Classify unavailable target, timeout, selector, and assertion failures without automatically calling them application defects.

## Acceptance criteria

A passing result requires an execution record from Playwright. A report must include evidence paths or state why evidence was unavailable. Any target-specific locator must be based on inspection, not guessed from the specification.
