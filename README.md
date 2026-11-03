# CodeReviewOracle — Decentralized AI Code Review

A GenLayer Intelligent Contract that reviews GitHub pull requests using AI
consensus. Fetches the PR page, LLM analyses for bugs/security/style, and
validators must agree on score + findings before committing.

## How it works

1. Caller submits a PR URL + focus area
2. Contract fetches the PR page
3. LLM reviews for bugs, security, performance, style, missing tests
4. Validators must agree (prompt_non_comparative) on score + findings
5. Result committed: score (1-10), risk level, findings, recommendation

## Interface

- `review_pr(pr_url, focus)` → JSON review
- `get_review(pr_url)` → retrieve last review
- `list_reviews()` → list all reviewed PRs
- `contract_info()` → metadata

## Evidence

- Contract: deployed on Studio Network
- Tests: direct-mode
- App: live
