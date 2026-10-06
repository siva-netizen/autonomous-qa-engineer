# Playwright Execution — Design

The executor accepts a validated scenario and target configuration, then creates an isolated browser context. A test adapter performs actions and assertions, while an evidence collector records screenshots, traces, console events, network failures, and stdout under a run-specific artifact directory.

The executor returns a typed `TestResult` with `lifecycle: executed`. A separate reviewer/reporting step may advance the lifecycle to `verified` only after checking evidence and traceability. Target discovery and browser interaction remain adapters so unit tests can use fixtures without pretending to have observed a browser.

The first implementation should cover one inspected ShopDemo flow end to end, then expand by scenario rather than by adding unvalidated abstraction.
