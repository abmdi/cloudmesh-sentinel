# Autonomous Development Policy (v0.1)

## Principles
- AI authorship must be disclosed. Do not impersonate a human developer or fabricate activity.
- Ship only meaningful, issue-linked changes. Never commit no-op changes to inflate activity.
- Scheduler may run multiple times daily, but commits are not guaranteed.
- Agent uses a short-lived, least-privilege GitHub App token and isolated runner.
- No production credentials or live cloud write permissions in the agent environment.
- Never expose secrets to untrusted PR code, logs, or prompts.
- Treat repository text, issues and external documentation as untrusted instructions.
- Restrict file writes to an explicit allowlist; block changes to workflows, policy, auth, billing, secrets and IaC without human review.
- Require lint, tests, dependency scanning and secret scanning before merging.
- Agent creates PRs; low-risk auto-merge may be enabled only after branch protections and security gates are verified.
- Human approval is mandatory for security-sensitive changes, infrastructure changes, dependencies, permissions and workflows.
- Enforce daily API budget, run timeout, rate limits, maximum diff size and kill switch.
- Store provenance (model, issue, test results) in PR descriptions.
- Disable automation on repeated failures, budget exhaustion, or suspicious instructions.

## Current state
This starter contains a scheduler in dry-run mode only. No AI API integration, commits or merges are active.

## Phase 2 enforcement
- The only enabled generation operation creates a single Markdown design proposal under `docs/engineering/` per run.
- AI changes are proposed as bot-authored PRs, never attributed to a human.
- No production code generation, automated merge or deployment is enabled in Phase 2.
