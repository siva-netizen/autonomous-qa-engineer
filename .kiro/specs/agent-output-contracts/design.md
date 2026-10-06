# Structured Agent Output Contracts — Design

## Boundary

`BaseAgent.run()` remains the single-agent boundary. It sends the caller request to the Gemini adapter, parses the returned content, validates it against the registered role, and returns the existing `AgentResult` enriched with a `StructuredAgentOutput`. `MultiAgentRuntime` and `AgentRegistry` remain unchanged in their dispatch semantics.

## Structured output

`agents/contracts.py` will define:

- `StructuredAgentOutput`: immutable typed envelope containing request ID, role, summary, lifecycle, requirement IDs, scenario IDs, role payload, assumptions, open questions, evidence references, optional execution outcome, and metadata.
- `StructuredOutputError`: explicit validation error for malformed or contradictory provider output.
- `StructuredAgentOutput.from_json(...)`: strict JSON parsing with expected request/role checks.
- `StructuredAgentOutput.to_dict()`: safe serialization for later report persistence.

Role payloads remain JSON-compatible mappings so each specialist can evolve without forcing a shared workflow. The validator applies minimum required keys and primitive/container types per role.

## Evidence policy

The structured lifecycle is authoritative. `generated` means reasoning/design only. `executed` and `verified` require at least one evidence reference. An optional `outcome` of `passed` is invalid for `generated` output and requires evidence for every lifecycle. Browser evidence is only a reference; the output contract never fabricates it.

`AgentResult` retains raw `content` for compatibility and adds `output`. Its lifecycle and evidence paths are derived from the validated output, not inferred from prose.

## Role payload minimums

| Role | Required payload fields |
|---|---|
| Requirement Analyzer | `requirements` list |
| Test Planner | `scenarios` list |
| Playwright Engineer | `generated_test` string, `evidence_plan` list |
| Failure Analyzer | `classification`, `observed_behavior`, `expected_behavior`, `confidence`, `recommended_action` |
| QA Reviewer | `coverage_gaps` list, `evidence_gaps` list, `verification_recommendation` string |

## Error handling

Malformed JSON, JSON arrays, missing fields, wrong types, invalid IDs, role mismatch, lifecycle/evidence contradictions, and invalid confidence values raise `StructuredOutputError`. Provider failures remain `GeminiRequestError`; they are not converted into QA results.

## Testing

Use a fake `ChatTransport` and deterministic JSON fixtures. Test every role's valid minimum payload, malformed JSON, missing role payload fields, mismatched request/role, traceability IDs, executed-without-evidence, and generated-passed rejection. No live Gemini call or browser result is needed.
