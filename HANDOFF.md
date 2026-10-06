# Kiro Agent Handoff
## Autonomous QA Engineer

### 1. Mission

You are the primary engineering agent responsible for building the **Autonomous QA Engineer** project.

The project is not intended to be a simple Playwright test generator or an LLM wrapper.

The goal is to build an engineering system that can take application requirements, reason about what should be tested, generate executable Playwright tests, execute those tests against a real application, collect evidence, analyze failures, and produce an actionable QA report.

The development process itself must demonstrate meaningful use of **Kiro's engineering capabilities**.

The project must therefore be built through Kiro rather than having Kiro artifacts added after the implementation is already complete.

The required development narrative is:

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
Agent Implementation
   ↓
Skills
   ↓
MCP
   ↓
Hooks / Automation
   ↓
Testing
   ↓
Validation
   ↓
Working Product
```

This follows the project-development expectations defined in the supplied Kiro preparation material.

---

# 2. Important: Project Specification Is Separate

A separate **Project Specification document will be provided to you**.

That specification is the authoritative source for:

- Functional requirements
- Product behavior
- MVP scope
- Agent responsibilities
- Expected workflows
- Technical constraints
- Acceptance criteria
- Features
- Non-functional requirements

Do **not** invent conflicting requirements.

Do **not** silently expand the product scope.

Do **not** implement features merely because they seem technically interesting.

If the specification and your assumptions conflict:

> Follow the specification.

If something is genuinely ambiguous:

> Document the ambiguity and make the smallest reasonable implementation decision.

Do not turn ambiguity into unnecessary architecture.

---

# 3. Target Application

The QA system will test the open-source application:

**ShopDemo**

Repository:

`ettaverse/dummy-ecommerce`

Repository:

`https://github.com/ettaverse/dummy-ecommerce`

ShopDemo is a local dummy e-commerce application designed for QA testing with Playwright.

It uses:

- Next.js
- TypeScript
- MSW
- Deterministic mock data
- Local execution
- No real backend dependency

The application runs locally on:

```text
http://localhost:3000
```

The repository provides deterministic product IDs, seeded users, test-oriented `data-testid` selectors, mocked APIs, and multiple user workflows.

The application includes:

- Product listing
- Search
- Category filtering
- Price sorting
- Product details
- Cart
- Quantity management
- Checkout
- Checkout validation
- Order confirmation
- Login
- Signup
- Authentication

The repository also contains a deliberately useful out-of-stock product and deterministic data, making it suitable for repeatable QA demonstrations.

Do not replace ShopDemo with another target application unless explicitly instructed.

---

# 4. First Task: Inspect Before Modifying

Before implementing the Autonomous QA Engineer, inspect the ShopDemo repository thoroughly.

You must understand:

### Application structure

Identify:

- Next.js structure
- Components
- Pages/routes
- Data sources
- MSW handlers
- Mock API behavior
- Authentication implementation
- Cart behavior
- Checkout behavior
- Validation behavior

### User workflows

Identify the important end-to-end flows.

At minimum investigate:

```text
Browse products
    ↓
Search/filter products
    ↓
Open product
    ↓
Add to cart
    ↓
Modify cart
    ↓
Checkout
    ↓
Order confirmation
```

Also investigate:

```text
Login
Signup
Logout
Invalid authentication
```

### Testability

Identify:

- Existing `data-testid` selectors
- Stable routes
- Deterministic data
- Seeded accounts
- API endpoints
- Existing test hooks
- Failure-prone boundaries

Do not immediately start coding after cloning the repository.

First establish an accurate understanding of the target application.

---

# 5. Create Kiro Steering Before Feature Implementation

Create the appropriate files under:

```text
.kiro/steering/
```

The steering layer should establish the persistent project context.

At minimum consider:

```text
.kiro/
└── steering/
    ├── product.md
    ├── tech.md
    ├── structure.md
    ├── architecture.md
    ├── coding-standards.md
    ├── testing.md
    └── security.md
```

Only create files that provide meaningful project context.

Do not create empty files simply to satisfy a checklist.

Steering should clearly establish:

### product.md

- What Autonomous QA Engineer is
- Who uses it
- Problem being solved
- Core workflow
- MVP boundaries
- Success criteria

### tech.md

Document the actual technology stack selected for the project.

Include:

- Runtime
- Programming language
- Agent framework
- Playwright
- MCP
- LLM strategy
- Storage
- Testing framework
- Build tooling

Do not claim technologies are used before they actually are.

### structure.md

Define the expected repository organization.

### architecture.md

Explain the major components and how information moves between them.

### coding-standards.md

Define:

- Naming
- Error handling
- Type safety
- Logging
- Async behavior
- Test conventions
- Agent conventions

### testing.md

Define the testing philosophy.

Include:

- Unit tests
- Integration tests
- Agent tests
- Playwright tests
- Failure analysis tests
- Regression tests
- Requirement-to-test traceability

### security.md

Document:

- Secrets management
- MCP credentials
- Environment variables
- Browser credentials
- Sensitive test data
- Logging restrictions

The source material explicitly expects Steering to establish product purpose, technology, structure, coding conventions, architecture, and team practices.

---

# 6. Use Spec-Driven Development

Do not implement the entire system in one large agent session.

Break the system into meaningful specifications.

The expected lifecycle is:

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

Maintain these artifacts in Git.

The source guidance specifically expects requirements, design, and task artifacts to remain part of the engineering history.

Potential specification boundaries include:

```text
.kiro/specs/

requirement-analysis/
    requirements.md
    design.md
    tasks.md

test-planning/
    requirements.md
    design.md
    tasks.md

playwright-generation/
    requirements.md
    design.md
    tasks.md

test-execution/
    requirements.md
    design.md
    tasks.md

failure-analysis/
    requirements.md
    design.md
    tasks.md

qa-reporting/
    requirements.md
    design.md
    tasks.md
```

The exact breakdown must follow the provided project specification.

Do not create unnecessary specs simply to increase the number of Kiro artifacts.

---

# 7. Core Autonomous QA Flow

The intended system architecture should revolve around a real QA pipeline.

Conceptually:

```text
User Requirement
       │
       ▼
Requirement Analyzer
       │
       ▼
Test Planner
       │
       ▼
Playwright Test Generator
       │
       ▼
Playwright Execution
       │
       ▼
Evidence Collector
       │
       ▼
Failure Analyzer
       │
       ▼
QA Reviewer
       │
       ▼
QA Report
```

The final implementation may differ based on the specification, but the system must preserve the separation of responsibilities.

Do not create one giant agent that performs everything.

---

# 8. Agent Responsibilities

Where appropriate, use specialized agents/sub-agents.

Potential responsibilities:

### Requirement Analyzer

Input:

```text
User story
Acceptance criteria
Product requirements
```

Output:

```text
Structured requirements
Expected behaviors
Preconditions
Validation rules
Potential edge cases
```

---

### Test Planner

Input:

```text
Structured requirements
```

Output:

```text
Test scenarios
Positive cases
Negative cases
Boundary cases
Edge cases
Priority
Requirement mapping
```

---

### Playwright Engineer

Input:

```text
Test scenarios
```

Output:

```text
Executable Playwright tests
```

The generated tests must actually execute.

The agent must not claim that a test passed merely because it generated syntactically valid code.

---

### Test Executor

Responsible for:

- Launching the browser
- Executing tests
- Capturing results
- Capturing screenshots
- Capturing traces where appropriate
- Capturing console/network information where useful

Execution must be grounded in real Playwright results.

---

### Failure Analyzer

Input may include:

```text
Test failure
Stack trace
Screenshot
DOM/state
Console output
Network information
Playwright trace
```

Output:

```text
Failure classification
Observed behavior
Expected behavior
Likely root cause
Evidence
Severity
Recommended action
```

Failure analysis must distinguish between:

```text
Test failure
Application defect
Test defect
Environment/infrastructure failure
```

Do not automatically classify every red test as an application bug.

---

### QA Reviewer

The reviewer should validate:

- Requirement coverage
- Test quality
- Test usefulness
- Evidence quality
- Failure analysis
- False-positive risk
- Missing scenarios

Where useful, use a separate reviewer/sub-agent rather than allowing the generator to grade itself.

---

# 9. MCP Usage

MCP must provide a genuine engineering capability.

Do not add MCP merely because the project needs to demonstrate MCP.

The primary MCP integration should support browser interaction / Playwright-based execution where appropriate.

The system should clearly demonstrate:

```text
Agent
   ↓
MCP
   ↓
Browser / External capability
   ↓
Real result
   ↓
Agent reasoning
```

Document:

- MCP server
- Why it exists
- What tools it exposes
- Which agents use it
- What information flows through it
- Configuration
- Security considerations

Never commit:

```text
API keys
tokens
passwords
private credentials
```

Use:

```text
.env.example
```

where required.

The supplied Kiro material explicitly says MCP should be meaningful rather than included just to tick a box.

---

# 10. Skills

Create reusable Skills where domain knowledge genuinely repeats.

Potential Skills:

```text
.kiro/skills/

playwright-testing/
test-design/
failure-analysis/
qa-reporting/
accessibility-testing/
security-testing/
```

Each Skill should contain useful domain instructions, not generic filler.

For example:

### Playwright Testing Skill

Could encode:

- Locator strategy
- `data-testid` preference
- Waiting strategy
- Assertion conventions
- Test isolation
- Trace/screenshot collection
- Retry philosophy
- Anti-flakiness rules

### Failure Analysis Skill

Could encode:

- How to classify failures
- Evidence requirements
- Root-cause reasoning
- Distinguishing environment failures from product failures
- Severity rules

Skills should be reused by agents rather than duplicated across prompts.

The Kiro material explicitly identifies Skills as reusable domain-specific capabilities and encourages demonstrating their actual use.

---

# 11. Hooks and Automation

Use Kiro Hooks where automation provides real value.

Potential hooks:

```text
test-on-change
lint-on-change
playwright-validation
spec-task-validation
documentation-update
security-check
```

Examples:

### Test Hook

When relevant source files change:

```text
Source changed
    ↓
Run relevant tests
    ↓
Report result
```

### Playwright Validation Hook

When generated Playwright tests change:

```text
Generated test changed
    ↓
Validate syntax
    ↓
Run selected test
    ↓
Store result
```

### Security Hook

Check for:

```text
Hardcoded secrets
API keys
Tokens
Credentials
```

Do not create hooks that run unnecessarily expensive operations on every file change.

The source material explicitly expects Hooks to automate useful validation such as tests, linting, formatting, documentation, API validation, and security checks.

---

# 12. Testing Philosophy

This project is itself a QA engineering system.

Therefore, testing quality is a first-class requirement.

The implementation should include appropriate levels of testing:

```text
Unit
  ↓
Integration
  ↓
Agent/component
  ↓
API
  ↓
Playwright E2E
  ↓
Failure/edge cases
```

Important:

The Autonomous QA Engineer must be tested against the ShopDemo application.

Do not only test the internal Python/TypeScript functions.

We need evidence that:

```text
Requirement
    ↓
Generated scenario
    ↓
Generated Playwright test
    ↓
Real browser execution
    ↓
Observed result
    ↓
QA conclusion
```

The source material specifically calls for unit, integration, API, edge/error, security, performance/UAT where appropriate, and requirement-to-test mapping.

---

# 13. Requirement-to-Test Traceability

A major quality feature should be traceability.

Every important requirement should be traceable through:

```text
Requirement
    ↓
Test Scenario
    ↓
Playwright Test
    ↓
Execution
    ↓
Result
    ↓
Evidence
```

A QA report should make it possible to answer:

> "Which test proves that this requirement works?"

and:

> "Which requirement is affected by this failure?"

This is important both for the product and for demonstrating engineering maturity.

---

# 14. Controlled Defect Strategy

The target application should be kept reproducible.

Do not rely entirely on random failures.

Create a controlled mechanism for demonstrating defects.

For example:

```text
Clean ShopDemo
       │
       ├── baseline
       │
       └── controlled defect scenario
```

Potential demonstration defects can include:

```text
Search returns incorrect result
Cart quantity does not update correctly
Checkout validation accepts invalid input
Out-of-stock product can be purchased
Order confirmation fails to display expected information
```

Do not introduce defects until the clean baseline has been established.

The final demo should show that the QA system can distinguish:

```text
PASS
FAIL
DEFECT
TEST ISSUE
ENVIRONMENT ISSUE
```

rather than simply producing a red/green status.

---

# 15. Evidence Is Mandatory

The system should produce real evidence.

Depending on the test:

```text
Screenshot
Trace
Test output
Console logs
Network information
DOM/state
Error stack
Requirement mapping
```

A report saying:

> "The login test failed."

is insufficient.

A useful report should say approximately:

```text
Requirement:
User should be able to log in using valid credentials.

Test:
AUTH-001

Result:
FAIL

Observed:
Application remained on /login after valid credentials were submitted.

Expected:
User should be redirected to the product listing.

Evidence:
Screenshot
Playwright trace
Console output

Classification:
Application defect

Severity:
High

Likely cause:
Authentication/session handling failed to persist the returned token.
```

The exact report format should follow the project specification.

---

# 16. Do Not Hallucinate Test Results

This is one of the most important constraints.

An agent must never claim:

```text
PASS
```

unless the test actually executed and passed.

Likewise, it must not claim:

```text
Application bug
```

without sufficient evidence.

The system must separate:

```text
Generated
```

from:

```text
Executed
```

and:

```text
Verified
```

For example:

```text
Generated:
✓ Playwright test created

Executed:
✓ Browser test executed

Result:
✗ Assertion failed

Analyzed:
✓ Failure classified

Evidence:
✓ Screenshot + trace
```

This distinction should be visible in the architecture and reporting.

---

# 17. Engineering Quality

Do not optimize for the number of AI agents.

Optimize for:

- Correctness
- Reproducibility
- Traceability
- Explainability
- Test reliability
- Maintainability
- Evidence
- Clean architecture

Avoid:

```text
Agent → Agent → Agent → Agent → Agent
```

when a simple function would work.

Similarly, do not use an LLM for deterministic work that can be performed reliably with normal code.

Use AI where reasoning is actually valuable:

```text
Requirement interpretation
Test scenario generation
Edge-case reasoning
Failure classification
Root-cause analysis
QA review
```

Use deterministic code for:

```text
Process execution
File handling
Result parsing
Test launching
Artifact collection
Schema validation
Report serialization
```

---

# 18. Kiro Submission Evidence

Throughout development, preserve evidence that Kiro genuinely contributed to the project.

The final repository/demo should make it possible to show:

### Steering

```text
.kiro/steering/
```

### Specs

```text
.kiro/specs/
```

with:

```text
requirements.md
design.md
tasks.md
```

### Hooks

```text
.kiro/hooks/
```

### Skills

```text
.kiro/skills/
```

### Agents

```text
.kiro/agents/
```

where appropriate.

### MCP

Document the configuration and actual usage.

### Testing

Show:

- Test execution
- Results
- Evidence
- Requirement mapping

### Git history

Keep meaningful commits that demonstrate the evolution of the system.

Do not squash everything into one final commit simply to make the repository look clean.

The supplied material specifically identifies Steering, Specs, Hooks, MCP, Skills, custom agents, testing, and evidence as important parts of the Kiro-oriented development story.

---

# 19. Recommended Repository Structure

The final structure should roughly follow:

```text
autonomous-qa-engineer/
│
├── .kiro/
│   ├── steering/
│   │   ├── product.md
│   │   ├── tech.md
│   │   ├── structure.md
│   │   ├── architecture.md
│   │   ├── coding-standards.md
│   │   ├── testing.md
│   │   └── security.md
│   │
│   ├── specs/
│   │   ├── requirement-analysis/
│   │   ├── test-planning/
│   │   ├── playwright-generation/
│   │   ├── test-execution/
│   │   ├── failure-analysis/
│   │   └── reporting/
│   │
│   ├── hooks/
│   ├── skills/
│   ├── agents/
│   └── settings/
│
├── src/
│   ├── agents/
│   ├── orchestration/
│   ├── playwright/
│   ├── analysis/
│   ├── reporting/
│   ├── evidence/
│   └── shared/
│
├── tests/
│
├── docs/
│
├── examples/
│
├── .env.example
├── README.md
└── ...
```

This is a starting point, not a mandate to create every directory immediately.

The supplied project guidance similarly recommends a `.kiro` structure containing Steering, Specs, Hooks, Skills, settings/MCP, and Agents alongside application/test/documentation code.

---

# 20. README Requirements

The final README must explain:

### What

What Autonomous QA Engineer does.

### Why

What real QA problem it solves.

### How

How the agent pipeline works.

### Architecture

Show the major components.

### Kiro

Explain how Kiro was used during development.

Include:

```text
Steering
Specs
Hooks
MCP
Skills
Agents
Testing
```

### Running the system

Provide exact commands.

### Running ShopDemo

Explain how to start the target application.

### Running QA

Explain how to provide a requirement and execute the QA pipeline.

### Evidence

Show where reports, screenshots, traces, and test results are stored.

### Demo

Provide a clear end-to-end example.

---

# 21. Demo Scenario

The final demonstration should not simply show code.

Show an actual workflow.

Example:

```text
STEP 1
Provide requirement:

"Users should be able to search for products by name
and add an available product to the shopping cart."
```

↓

```text
STEP 2
Requirement Analyzer
```

Produces structured requirements.

↓

```text
STEP 3
Test Planner
```

Produces scenarios.

↓

```text
STEP 4
Playwright Engineer
```

Generates executable Playwright test.

↓

```text
STEP 5
Playwright/MCP
```

Runs the browser against ShopDemo.

↓

```text
STEP 6
Evidence Collector
```

Collects:

- Screenshot
- Trace
- Logs
- Result

↓

```text
STEP 7
Failure Analyzer
```

If something fails:

```text
Observed behavior
Expected behavior
Root cause
Severity
Evidence
```

↓

```text
STEP 8
QA Report
```

Final result:

```text
Requirement
    ↓
Tests
    ↓
Execution
    ↓
Evidence
    ↓
QA verdict
```

---

# 22. What NOT To Do

### Do not bolt Kiro on at the end

The project must be developed through Kiro from the beginning.

### Do not create fake Kiro artifacts

Do not create meaningless Steering, Skills, Agents, or Hooks just for submission screenshots.

### Do not over-engineer

Do not build a distributed multi-agent platform if the MVP can be implemented cleanly without one.

### Do not build another e-commerce application

ShopDemo is the target application.

Our product is the **Autonomous QA Engineer**.

### Do not trust generated tests without execution

Generated code is not evidence.

### Do not trust an LLM's PASS/FAIL claim

Use actual Playwright execution results.

### Do not classify every failure as a product defect

Investigate the failure.

### Do not hardcode secrets

Use environment configuration.

### Do not introduce unnecessary external dependencies

Every dependency should have a reason.

### Do not add features solely to increase the Kiro checklist

The source guidance explicitly warns against adding capabilities just to tick boxes.

---

# 23. Definition of Done

The project is not complete merely because the application starts.

The MVP is complete when:

```text
[ ] ShopDemo can run locally

[ ] Autonomous QA Engineer can accept a structured requirement

[ ] Requirement can be analyzed

[ ] Test scenarios can be generated

[ ] Playwright tests can be generated

[ ] Generated tests can actually execute

[ ] Execution produces real evidence

[ ] Failures can be analyzed

[ ] QA report can be generated

[ ] Requirements map to tests

[ ] Kiro Steering exists and is meaningful

[ ] Kiro Specs exist and reflect implementation

[ ] Kiro Hooks provide useful automation

[ ] MCP provides meaningful external/browser capability

[ ] Skills encode reusable QA knowledge

[ ] Specialized agents are used where justified

[ ] Unit/integration/E2E testing exists

[ ] Controlled defect scenario can be demonstrated

[ ] README documents the complete workflow

[ ] Architecture is documented

[ ] No secrets are committed

[ ] Demo evidence exists
```

---

# 24. Development Order

Follow this order unless the separate specification requires otherwise.

```text
1. Inspect ShopDemo
        ↓
2. Establish clean baseline
        ↓
3. Create Kiro Steering
        ↓
4. Define architecture
        ↓
5. Create first Spec
        ↓
6. Implement smallest vertical slice
        ↓
7. Add tests
        ↓
8. Add agent specialization
        ↓
9. Add Playwright execution
        ↓
10. Add MCP
        ↓
11. Add Skills
        ↓
12. Add Hooks
        ↓
13. Add failure analysis
        ↓
14. Add reporting
        ↓
15. Introduce controlled defects
        ↓
16. Validate complete workflow
        ↓
17. Polish README/demo/evidence
```

Do not implement everything before testing the first vertical slice.

---

# 25. Final Principle

The strongest version of this project is not:

> "We built an AI that writes Playwright tests."

It is:

> **"We built an autonomous QA engineering workflow that turns requirements into executable tests, runs them against a real application, gathers evidence, reasons about failures, and produces traceable QA results, while the entire system itself was developed using Kiro's Steering, Specs, Agents, Skills, MCP, Hooks, and testing workflow."**

The Kiro usage must therefore be visible in both:

1. **The development process**
2. **The resulting product**

Build the project so that the final demonstration proves both.

Do not optimize for the number of Kiro features used.

Optimize for a coherent engineering story where every Kiro capability has a reason to exist.
