# Structured Agent Output Contracts — Correctness (property-based)

Kiro Spec Correctness properties for IDE property-based testing. Executable checks live in `tests/unit/test_agent_output_contracts_pbt.py` (pytest + Hypothesis, marker `property`).

## Properties

### PROP-AOC-001 — Valid minimum payloads always parse

**Requirement:** REQ-AOC-001, REQ-AOC-004  
**Statement:** For any agent role and any non-empty summary string, a minimum valid structured JSON document for that role MUST parse and validate when request ID and role match the caller.

### PROP-AOC-002 — Invalid traceability IDs are rejected

**Requirement:** REQ-AOC-003  
**Statement:** For any requirement ID string that does not match `REQ-*` traceability format, validation MUST reject the document.

### PROP-AOC-003 — Generated output cannot claim PASS

**Requirement:** REQ-AOC-005  
**Statement:** For any role, when lifecycle is `generated` and outcome is `passed`, validation MUST reject the document.

### PROP-AOC-004 — Executed lifecycle requires evidence

**Requirement:** REQ-AOC-005, REQ-AOC-006  
**Statement:** For any role, when lifecycle is `executed` or `verified` and evidence is empty, validation MUST reject the document.

## Running (IDE)

```bash
python -m pip install hypothesis
python -m pytest tests/unit/test_agent_output_contracts_pbt.py -m property -v
```

Default `pytest` (hooks, CI) excludes `@pytest.mark.property` tests; run the command above in Kiro IDE when demonstrating correctness.
