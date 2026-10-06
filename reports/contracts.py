"""Evidence and report contracts for later execution/reporting services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ExecutionOutcome = Literal["passed", "failed", "skipped", "blocked", "unknown"]


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    kind: Literal["screenshot", "trace", "console", "network", "dom", "stdout"]
    path: str
    description: str


@dataclass(frozen=True, slots=True)
class ExecutionRecord:
    requirement_ids: tuple[str, ...]
    scenario_id: str
    lifecycle: Literal["executed", "verified"]
    outcome: ExecutionOutcome
    duration_ms: int
    evidence: tuple[EvidenceReference, ...]

    def can_claim_pass(self) -> bool:
        return self.outcome == "passed" and bool(self.evidence)
