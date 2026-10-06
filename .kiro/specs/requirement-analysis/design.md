# Requirement Analysis — Design

1. Parse input into a typed `Requirement` request.
2. Normalize explicit statements and acceptance criteria using deterministic code.
3. Ask the reasoning adapter for candidate scenarios when interpretation is needed.
4. Validate every scenario against required fields, stable IDs, and requirement mappings.
5. Emit a planning artifact with assumptions and unresolved questions.

The reasoning adapter is replaceable and defaults to a mock implementation for tests. The analyzer does not access the browser, mark results as passed, or infer application behavior not present in the input. Validation failures become structured analysis issues.
