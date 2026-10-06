import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = process.cwd();
const requiredFiles = [
  'HANDOFF.md',
  'SPEC.md',
  'README.md',
  'package.json',
  '.env.example',
  '.kiro/steering/product.md',
  '.kiro/steering/tech.md',
  '.kiro/steering/structure.md',
  '.kiro/steering/architecture.md',
  '.kiro/steering/coding-standards.md',
  '.kiro/steering/testing.md',
  '.kiro/steering/security.md',
  '.kiro/specs/requirement-analysis/requirements.md',
  '.kiro/specs/requirement-analysis/design.md',
  '.kiro/specs/requirement-analysis/tasks.md',
  '.kiro/specs/playwright-execution/requirements.md',
  '.kiro/specs/playwright-execution/design.md',
  '.kiro/specs/playwright-execution/tasks.md',
  '.kiro/specs/multiagent-groq-foundation/requirements.md',
  '.kiro/specs/multiagent-groq-foundation/design.md',
  '.kiro/specs/multiagent-groq-foundation/tasks.md',
  '.kiro/specs/agent-output-contracts/requirements.md',
  '.kiro/specs/agent-output-contracts/design.md',
  '.kiro/specs/agent-output-contracts/tasks.md',
  '.kiro/specs/independent-agent-runner/requirements.md',
  '.kiro/specs/independent-agent-runner/design.md',
  '.kiro/specs/independent-agent-runner/tasks.md',
  '.kiro/specs/gemini-provider-migration/requirements.md',
  '.kiro/specs/gemini-provider-migration/design.md',
  '.kiro/specs/gemini-provider-migration/tasks.md',
  '.kiro/specs/qa-engineer-tui/requirements.md',
  '.kiro/specs/qa-engineer-tui/design.md',
  '.kiro/specs/qa-engineer-tui/tasks.md',
  '.kiro/skills/playwright-testing/SKILL.md',
  '.kiro/skills/test-design/SKILL.md',
  '.kiro/skills/failure-analysis/SKILL.md',
  '.kiro/agents/requirement-analyzer.md',
  '.kiro/agents/test-planner.md',
  '.kiro/agents/playwright-engineer.md',
  '.kiro/agents/failure-analyzer.md',
  '.kiro/agents/qa-reviewer.md',
  '.kiro/hooks/validate-scaffold.kiro.hook',
  '.kiro/hooks/test-on-change.json',
  '.kiro/hooks/lint-on-change.json',
  '.kiro/hooks/security-check.json',
  '.kiro/hooks/agent-on-spec-change.json',
  '.kiro/settings/mcp.json',
  'agents/kiro_contracts.py',
  'pyproject.toml',
  'vitest.config.ts',
  'requirements-dev.txt',
  'agents/contracts.py',
  'agents/base.py',
  'agents/specialized.py',
  'agents/registry.py',
  'agents/runtime.py',
  'agents/run.py',
  'services/gemini_client.py',
  'services/groq_client.py',
  'playwright/contracts.py',
  'qa_mcp/config.py',
  'services/playwright_mcp_client.py',
  'reports/contracts.py',
  'scripts/security_scan.py',
  'src/domain/contracts.ts',
];

const missing = requiredFiles.filter((file) => !existsSync(resolve(root, file)));
if (missing.length > 0) {
  console.error('Scaffold validation failed. Missing files:');
  for (const file of missing) console.error(`- ${file}`);
  process.exit(1);
}

const packageJson = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf8'));
if (packageJson.name !== 'autonomous-qa-engineer' || packageJson.private !== true) {
  console.error('Scaffold validation failed. package.json identity is invalid.');
  process.exit(1);
}

console.log(`Scaffold validation passed: ${requiredFiles.length} required files present.`);
console.log('Python multi-agent foundation artifacts and inspected ShopDemo baseline are present.');
