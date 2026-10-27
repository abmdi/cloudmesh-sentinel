# Phase 2: zero-cost operating guide

## Scope and limitations
The agent generates **engineering design notes only** and opens PRs. It does not autonomously write, test or merge production code. It does not guarantee daily contributions or GitHub profile credit. No fake author attribution or artificial commit padding.

## Setup
1. Publish the repository as public; use standard GitHub-hosted runners.
2. Create a free-tier Gemini API key in Google AI Studio without enabling paid billing. Free access and quotas are subject to change; check current account eligibility.
3. Add `GEMINI_API_KEY` to repository **Actions secrets**. Never commit it.
4. Add repository **Actions variable** `AI_AGENT_ENABLED=true`.
5. Optionally add Actions variable `GEMINI_MODEL=gemini-2.5-flash-lite`; leave unset for the built-in default.
6. Repository Settings > Actions > General: allow GitHub Actions to create pull requests if this setting is available; restrict workflow permissions as appropriate.
7. Enable branch protection / rulesets on `main`: require CI and human review; block force pushes.
8. Run workflow manually once, inspect the resulting PR and check logs. If no PR is created, check quota, Actions settings, and GitHub token permissions.

## Free-tier safeguards
- Only GitHub-hosted standard runners on a public repository.
- One API call per scheduled run; six scheduled runs per day maximum.
- Request bounded to 1,800 output tokens and 45 seconds network timeout.
- On missing key, quota errors or provider outages, skip safely.
- Do not enable paid API billing or paid GitHub runner types.
- Stop switch: set `AI_AGENT_ENABLED=false` or disable the workflow.
- Github may disable scheduled workflows after 60 days of inactivity, and scheduled events may be delayed or dropped.
- API free-tier input may be used for provider product improvement; do not send private customer data.

## Security notes
- AI is limited to creating a new file under `docs/engineering/`.
- Generated Markdown is untrusted; never execute its instructions.
- The workflow does not merge, deploy, alter dependencies, change secrets or modify IaC.
- The default GITHUB_TOKEN may require manual approval for checks on automation-created PRs. A separate tightly scoped GitHub App can be added later after review.
- Scheduled workflow definitions and policy files must be protected by CODEOWNERS and rulesets.

## Future milestone
A production-code agent needs sandbox isolation, prompt-injection defenses, independent test/security gates, an approved file allowlist, and a trustworthy review/merge mechanism. It is **not** implemented in Phase 2.
