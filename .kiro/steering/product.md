# Product Context

## Purpose

Autonomous QA Engineer converts a requirement into traceable test scenarios, executable Playwright tests, observed browser results, evidence-backed failure analysis, and a QA report.

## Users

Primary users are QA engineers, SDETs, developers, and technical leads who need repeatable web-flow validation. The primary interactive surface is the Textual QA engineer TUI; structured JSON CLI dispatch remains for automation. The system supports human review; it does not replace accountable QA decisions.

## MVP boundary

The first vertical slice targets only the fixed local ShopDemo application (`ettaverse/dummy-ecommerce`) and focuses on requirement analysis, test planning, Playwright generation, real execution, evidence capture, failure classification, and reporting. Advanced self-healing, broad application discovery, performance testing, and external issue automation are deferred.

## Non-negotiable behavior

A generated test is not an executed test. A failed test is not automatically an application defect. Reports must preserve lifecycle state, evidence references, uncertainty, and requirement traceability.

## Success criteria

The MVP must accept a structured requirement, produce meaningful scenarios, generate executable tests, execute them against ShopDemo, capture evidence, classify failures conservatively, and map results back to requirements.
