# Autonomous QA Engineer

## 1. Project Overview

### Project Name

**Autonomous QA Engineer**

### Project Type

Agentic AI-powered web application testing and quality-assurance platform.

### One-Line Description

> An autonomous QA engineering system that converts application requirements into executable Playwright tests, explores web applications, executes tests, analyzes failures, and produces actionable test and defect reports.

---

# 2. Problem Statement

Modern web applications require continuous testing as features, UI components, APIs, and user flows evolve.

Traditional QA workflows often involve:

1. Reading requirements manually.
2. Designing test cases manually.
3. Writing automation scripts.
4. Running tests.
5. Investigating failures.
6. Updating tests when the application changes.
7. Reporting defects manually.

This creates a repetitive and time-consuming workflow.

The **Autonomous QA Engineer** aims to automate significant portions of this workflow through specialized AI agents and browser automation using Playwright.

The goal is **not** to replace human QA engineers completely.

Instead, the system acts as an autonomous QA engineer that can perform repetitive testing activities while keeping humans involved in important validation and decision-making.

---

# 3. Target Users

### Primary Users

- QA engineers
- Software developers
- SDET engineers
- Automation engineers
- Development teams

### Secondary Users

- Technical leads
- Engineering managers
- Product teams

---

# 4. Core Product Capabilities

The MVP should provide the following capabilities.

## 4.1 Requirement Analysis

The system accepts:

- User stories
- Feature descriptions
- Acceptance criteria
- Existing specifications

The Requirement Analysis Agent converts these into structured testing requirements.

Example:

```text
Requirement:

User should be able to log in using
valid email and password.

Acceptance Criteria:

- Valid credentials should authenticate the user.
- Invalid credentials should display an error.
- Empty fields should be rejected.
```

The agent generates:

```text
TC-001: Valid login
TC-002: Invalid password
TC-003: Invalid email
TC-004: Empty email
TC-005: Empty password
TC-006: Empty credentials
```

---

# 5. Test Planning Agent

The Test Planning Agent determines:

- What should be tested.
- Which scenarios are positive.
- Which scenarios are negative.
- Which edge cases should be tested.
- Which flows require browser interaction.
- Which scenarios can be validated through APIs.

The output should be a structured test plan.

```text
Requirement
      ↓
Test Scenarios
      ↓
Test Cases
      ↓
Execution Strategy
```

---

# 6. Playwright Test Generation

The system generates executable Playwright tests.

Example conceptual output:

```text
Test Case
    ↓
Test specification
    ↓
Playwright implementation
    ↓
Browser execution
```

Generated tests should follow project-specific testing conventions defined through Kiro Steering and Skills.

Tests should prioritize robust selectors such as:

- `data-testid`
- Accessible roles
- Labels
- Semantic selectors

The system should avoid unnecessarily fragile selectors such as deeply nested CSS selectors or XPath unless there is a justified reason.

---

# 7. Autonomous Browser Execution

The Playwright Agent should be capable of:

- Opening the application.
- Navigating pages.
- Identifying interactive elements.
- Performing user actions.
- Filling forms.
- Clicking controls.
- Waiting for application state.
- Capturing screenshots.
- Collecting console errors.
- Collecting network failures where applicable.
- Executing generated test scenarios.

The browser should act as the execution environment rather than allowing the LLM to merely claim that a test passed.

---

# 8. Failure Analysis Agent

When a Playwright test fails, the system should automatically collect available evidence.

Potential evidence:

- Test steps
- Error message
- Stack trace
- Screenshot
- DOM state
- Browser console output
- Network information
- Previous test results

The Failure Analysis Agent should classify failures.

Example:

```text
TEST FAILURE

Test: User Login

Classification:
APPLICATION BUG

Evidence:
- Login request returned HTTP 500
- Browser successfully submitted the form
- Backend returned an internal server error

Confidence:
91%
```

Possible classifications:

- Application bug
- Test bug
- Environment failure
- Network failure
- Authentication failure
- Timeout
- Selector failure
- Unknown failure

The agent must avoid presenting an uncertain diagnosis as fact.

---

# 9. Test Reporting

The platform should generate a structured test report containing:

- Total tests
- Passed tests
- Failed tests
- Skipped tests
- Execution duration
- Failure classification
- Evidence
- Suggested remediation
- Requirement coverage

Example:

```text
AUTONOMOUS QA REPORT

Requirements:       12
Test Cases:         38

Passed:             31
Failed:              5
Skipped:             2

Requirement Coverage: 91%

Critical Failures:   1
Environment Issues:  2
Test Issues:         1
Application Issues:  1
```

---

# 10. Kiro Development Strategy

Kiro must be used throughout the development lifecycle rather than being added after implementation.

The intended workflow is:

```text
Problem
   ↓
Kiro Steering
   ↓
Requirements
   ↓
Design
   ↓
Tasks
   ↓
Kiro Agent Implementation
   ↓
MCP / Skills / Agents
   ↓
Hooks
   ↓
Testing
   ↓
Validation
   ↓
Working Product
```

This is a core project requirement.

---

# 11. Kiro Steering Requirements

The repository must contain project context through `.kiro/steering/`.

Recommended files:

```text
.kiro/
└── steering/
    ├── product.md
    ├── tech.md
    ├── structure.md
    ├── architecture.md
    ├── coding-standards.md
    ├── security.md
    └── testing.md
```

These should define:

- Product purpose
- Technology stack
- Repository structure
- Architecture
- Coding conventions
- Security requirements
- Testing conventions
- API conventions

The purpose is for Kiro to understand the project context consistently when implementing features.

---

# 12. Kiro Spec-Driven Development

Every major feature must follow:

```text
Requirements
     ↓
Design
     ↓
Tasks
     ↓
Implementation
     ↓
Testing
```

Recommended specifications:

```text
.kiro/specs/

├── requirement-analysis/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
│
├── test-planning/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
│
├── playwright-execution/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
│
├── failure-analysis/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
│
└── reporting/
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

Requirements should contain user stories and acceptance criteria.

Design documents should describe the technical implementation.

Tasks should map implementation work back to the requirements.

The resulting requirements, design, and tasks should remain committed to Git because they are evidence of the Kiro development process.

---

# 13. Kiro Hooks

Hooks should demonstrate that Kiro participates in the engineering workflow.

Potential hooks:

```text
.kiro/hooks/

├── test-on-change.json
├── lint-on-change.json
├── playwright-validation.json
├── documentation.json
└── security-check.json
```

Potential automation:

```text
Code Change
    ↓
Kiro Hook
    ↓
Lint
    ↓
Unit Tests
    ↓
Playwright Tests
    ↓
Validation
    ↓
Report
```

Hooks may be used for testing, linting, formatting, documentation, security checks, API validation, and other repetitive development activities.

---

# 14. MCP Integration

The project should include at least one meaningful MCP integration.

MCP should solve a real problem rather than existing solely as a submission checkbox.

Potential MCP tools:

### Playwright MCP

Used for:

- Browser interaction
- DOM inspection
- Navigation
- Screenshot capture
- Browser-based validation

### GitHub MCP

Potential capabilities:

- Read repository information
- Inspect issues
- Inspect pull requests
- Inspect changed files
- Create test-related issues
- Create defect reports

### Optional additional MCP

A test-results or documentation MCP server may be considered if it provides meaningful functionality.

The MCP configuration must be documented and API keys or credentials must never be committed. An `.env.example` should be provided.

---

# 15. Kiro Skills

The project should contain domain-specific Skills.

Recommended:

```text
.kiro/skills/

├── playwright-testing/
│   └── SKILL.md
│
├── test-design/
│   └── SKILL.md
│
├── failure-analysis/
│   └── SKILL.md
│
├── accessibility-testing/
│   └── SKILL.md
│
└── security-testing/
    └── SKILL.md
```

Skills should encode reusable testing knowledge and project-specific instructions.

For example, the Playwright Skill can define:

- Selector strategy
- Waiting strategy
- Test organization
- Page object conventions
- Screenshot requirements
- Error handling
- Browser cleanup
- Test isolation

The project should demonstrate when each Skill is actually used.

---

# 16. Specialized Agents

The project should use multiple specialized agents where appropriate.

Recommended agents:

```text
agents/

├── requirement-analyzer.md
├── test-planner.md
├── playwright-engineer.md
├── failure-analyzer.md
├── security-reviewer.md
└── qa-reviewer.md
```

Example workflow:

```text
                 Requirement
                      │
                      ▼
             Requirement Agent
                      │
                      ▼
                Test Planner
                      │
                      ▼
             ┌────────────────┐
             │ Playwright     │
             │ Agent          │
             └───────┬────────┘
                     │
                     ▼
                 Execution
                     │
               ┌─────┴─────┐
               │           │
             PASS         FAIL
               │           │
               │           ▼
               │     Failure Agent
               │           │
               └─────┬─────┘
                     ▼
                QA Reviewer
```

Parallel sub-agents may be used where tasks can be independently investigated. The project should demonstrate why parallelization provides value rather than using multiple agents merely for visual effect.

---

# 17. Testing Requirements

The project itself must be thoroughly tested.

Required categories:

### Unit Tests

Test individual components and services.

### Integration Tests

Validate interaction between:

- Agents
- Backend
- Playwright
- MCP
- Database

### API Tests

Validate backend APIs independently.

### End-to-End Tests

Use Playwright to test the actual application.

### Edge Cases

Examples:

- Empty requirements
- Ambiguous requirements
- Missing selectors
- Application unavailable
- Browser timeout
- Authentication expiration
- Network failure
- Unexpected DOM changes
- Invalid generated tests

### Security Testing

Validate:

- Credential handling
- Prompt injection resistance where applicable
- Sensitive information handling
- Authentication boundaries
- MCP permissions

### Performance Testing

Measure:

- Test generation latency
- Browser execution time
- Agent response time
- Concurrent test execution

The source specifically expects validation beyond simply demonstrating that the application works, including unit, integration, API, edge-case, security, performance and user-acceptance testing.

---

# 18. Requirement-to-Test Traceability

Every major requirement should map to tests.

```text
REQ-001
   ↓
TC-001
TC-002
TC-003
   ↓
Playwright
   ↓
Execution Result
```

The final report should make it possible to answer:

> "Which tests prove that this requirement works?"

This provides concrete evidence rather than relying on screenshots of a functioning UI.

---

# 19. Submission Requirements

The project must explicitly demonstrate the Kiro capabilities expected by the submission.

## Mandatory Kiro Evidence

### 1. Problem Definition

Demonstrate:

- Real problem
- Target users
- Major use cases
- MVP
- Differentiator
- Success criteria

These should be documented before implementation.

### 2. Steering

Repository should contain committed Steering files.

### 3. Specs

Repository should contain:

- Requirements
- Design
- Tasks

for major features.

### 4. Hooks

At least meaningful automated development workflows should be demonstrated.

### 5. MCP

Document:

- MCP server
- Tools
- Purpose
- Configuration
- Security considerations

### 6. Skills

At least one meaningful domain Skill should be implemented.

Preferably multiple Skills where justified.

### 7. Custom Agents

Demonstrate specialized agents and explain their responsibilities.

### 8. Sub-agents / Parallel Work

If used, demonstrate a meaningful parallel workflow.

### 9. Testing

Provide evidence of:

- Unit tests
- Integration tests
- API tests
- E2E tests
- Edge cases
- Security validation
- Performance validation

The source's master checklist explicitly calls for these Kiro artifacts and final evidence.

---

# 20. Final Demonstration Requirements

The final submission should contain:

- Working application
- Clean UI
- README
- Architecture diagram
- Demo video
- Screenshots
- Test evidence
- Kiro configuration
- Steering files
- Specs
- Hooks
- MCP documentation
- Skills
- Agent configurations
- Explanation of Kiro-assisted development

The final presentation must answer two questions:

### Question 1

> What does Autonomous QA Engineer do?

### Question 2

> What did Kiro enable us to do that would have been significantly harder or less structured otherwise?

The second question is critical.

The project should demonstrate **Kiro as an engineering system**, not merely as an AI autocomplete tool.

---

# 21. Important Things to Be Careful About

## 21.1 Do NOT bolt Kiro onto the project at the end

The project should be developed through Kiro from Day 1.

This is explicitly emphasized in the source material.

---

## 21.2 Do NOT add features only to tick submission boxes

Bad:

```text
"We need MCP."

→ Add random MCP server.
```

Good:

```text
"We need browser interaction."

→ Playwright MCP provides browser capabilities.
```

Every Kiro capability should have a legitimate engineering purpose.

---

## 21.3 Do NOT make the project just an LLM wrapper

The core system must contain actual engineering logic.

The LLM should assist with:

- Planning
- Reasoning
- Test generation
- Failure analysis

while Playwright should perform the actual browser execution.

---

## 21.4 Do NOT trust the agent's claims

This is particularly important.

Bad:

```text
Agent:
"Login test passed."
```

without actually running the browser.

Good:

```text
Agent
 ↓
Playwright
 ↓
Browser
 ↓
Observed result
 ↓
Evidence
 ↓
PASS
```

The system should distinguish **generated reasoning** from **observed execution evidence**.

---

## 21.5 Do NOT over-engineer the MVP

The MVP should probably focus on:

```text
Requirements
     ↓
Test Generation
     ↓
Playwright Execution
     ↓
Failure Analysis
     ↓
Report
```

Self-healing selectors, visual regression, API testing, accessibility testing, GitHub automation and advanced multi-agent orchestration can come afterward.

Do not build six products and finish none of them.

---

## 21.6 Keep evidence throughout development

Capture:

- Kiro specs
- Kiro Steering
- Agent configurations
- Skills
- Hooks
- MCP setup
- Test results
- Screenshots
- Git history
- Demo scenarios

Do not attempt to reconstruct your entire Kiro development process the night before submission.

---

# 22. Success Criteria

The MVP will be considered successful if it can:

1. Accept a structured requirement.
2. Generate meaningful test scenarios.
3. Convert scenarios into Playwright tests.
4. Execute those tests against a real web application.
5. Capture execution evidence.
6. Detect failures.
7. Classify failures.
8. Produce a useful QA report.
9. Map tests back to requirements.
10. Demonstrate meaningful usage of Kiro Steering, Specs, Hooks, MCP, Skills and Agents.

---

# 23. Final Project Narrative

The final project should communicate the following story:

```text
Traditional QA
     ↓
Manual requirement analysis
     ↓
Manual test design
     ↓
Manual automation
     ↓
Manual execution
     ↓
Manual failure investigation
     ↓
Manual reporting


              ↓
        Autonomous QA Engineer
              ↓

Requirement
      ↓
AI Test Planning
      ↓
Playwright Test Generation
      ↓
Autonomous Browser Execution
      ↓
Failure Detection
      ↓
Failure Analysis
      ↓
Evidence Collection
      ↓
QA Report
```

And the development story should be:

```text
Problem
   ↓
Kiro Steering
   ↓
Kiro Specs
   ↓
Design
   ↓
Tasks
   ↓
Kiro Agents
   ↓
Skills
   ↓
MCP
   ↓
Hooks
   ↓
Testing
   ↓
Validation
   ↓
Working Product
```

This structure intentionally follows the Kiro-first development philosophy and the submission checklist established in the source material.
