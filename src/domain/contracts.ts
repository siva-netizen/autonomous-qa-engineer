export type LifecycleState = 'generated' | 'executed' | 'verified';

export type ExecutionOutcome = 'passed' | 'failed' | 'skipped' | 'blocked' | 'unknown';

export type FailureClassification =
  | 'application-bug'
  | 'test-bug'
  | 'environment-failure'
  | 'network-failure'
  | 'authentication-failure'
  | 'timeout'
  | 'selector-failure'
  | 'unknown';

export interface Requirement {
  id: string;
  statement: string;
  acceptanceCriteria: string[];
}

export interface TestScenario {
  id: string;
  requirementIds: string[];
  title: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  preconditions: string[];
  steps: string[];
  expectedResults: string[];
}

export interface EvidenceReference {
  kind: 'screenshot' | 'trace' | 'console' | 'network' | 'dom' | 'stdout';
  path: string;
  description: string;
}

export interface TestResult {
  scenarioId: string;
  lifecycle: LifecycleState;
  outcome: ExecutionOutcome;
  durationMs?: number;
  evidence: EvidenceReference[];
  failure?: {
    classification: FailureClassification;
    observed: string;
    expected: string;
    confidence: number;
    recommendedAction: string;
  };
}
