import { describe, expect, it } from 'vitest';
import type { TestResult } from '../../src/domain/contracts.js';

describe('TestResult lifecycle contract', () => {
  it('keeps generated results distinct from verified results', () => {
    const generated: TestResult = {
      scenarioId: 'TC-001',
      lifecycle: 'generated',
      outcome: 'unknown',
      evidence: [],
    };

    expect(generated.lifecycle).toBe('generated');
    expect(generated.outcome).not.toBe('passed');
  });
});
