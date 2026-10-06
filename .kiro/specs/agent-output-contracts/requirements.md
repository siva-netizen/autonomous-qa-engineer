# Structured Agent Output Contracts — Requirements

## Scope

Make every independently invoked QA agent return a typed, traceable, evidence-aware structured output. The runtime remains caller-selected and may invoke multiple agents sequentially; this feature does not add a mandatory workflow or live-provider requirement.

## Requirements

- **REQ-AOC-001:** A successful agent call MUST parse its reasoning response as a structured JSON output with a request ID, role, summary, lifecycle, traceability IDs, role payload, assumptions, open questions, and evidence references.
- **REQ-AOC-002:** Structured output validation MUST reject malformed JSON, missing required fields, wrong field types, unknown lifecycle values, and role mismatches before returning an `AgentResult`.
- **REQ-AOC-003:** The output request ID and role MUST match the invoking `AgentRequest` and registered agent role. Requirement IDs and scenario IDs MUST remain traceable when supplied by the request or output.
- **REQ-AOC-004:** Each role MUST validate a minimum role-specific payload: requirements for Requirement Analyzer; scenarios for Test Planner; generated test and evidence plan for Playwright Engineer; classification, observed/expected behavior, confidence, and recommended action for Failure Analyzer; and coverage/evidence gaps plus verification recommendation for QA Reviewer.
- **REQ-AOC-005:** Lifecycle values MUST be `generated`, `executed`, or `verified`. `executed` and `verified` outputs MUST include evidence references. A generated output MUST NOT claim a passed execution outcome.
- **REQ-AOC-006:** Evidence references MUST include a supported kind, non-empty path, and description. Structured agent outputs MUST preserve evidence separately from generated text.
- **REQ-AOC-007:** Existing `AgentResult` callers MUST remain compatible while gaining access to the validated structured output, lifecycle, evidence paths, model, and provider metadata.
- **REQ-AOC-008:** The runtime MUST continue to support independent single-agent and caller-selected multi-agent invocation without imposing Analyzer → Planner → Engineer sequencing.
- **REQ-AOC-009:** Tests MUST use deterministic fake Gemini transport and cover valid role outputs, malformed responses, request/role mismatches, traceability, role payload validation, and evidence-gated lifecycle/outcome claims.
- **REQ-AOC-010:** No provider secret may be added to schemas, fixtures, tests, logs, or committed artifacts. Live Gemini validation remains outside this feature.

## Acceptance criteria

1. All five agents parse and validate a valid role-specific structured response.
2. Invalid provider content produces a typed validation error and no `AgentResult`.
3. `AgentResult` exposes the structured output while preserving its existing `content` field.
4. Lifecycle and pass claims cannot bypass evidence requirements.
5. Existing independent multi-agent invocation behavior remains unchanged and all relevant checks pass.
