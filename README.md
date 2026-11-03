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

- Contract address: 0x2d9F945E665F4d3af6Cc7F23ce49C0A3107b2DA2
- Deploy tx: 0xa743fa4551c9b39b099195a59dfe31797b30af58ad993e2bca1e5a3b8b57898d
- E2E tx: 0x95909b5f5a9e60fb4c5de7079aa60ee9e8d5a317901411785ac9bed7899c669a
- Test result: reviewed PR → findings (2), score, recommendation
- Tests: direct-mode + Studio Network
- App: live
