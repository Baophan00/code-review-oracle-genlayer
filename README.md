# CodeReviewOracle — Decentralized AI Code Review for GitHub PRs

A GenLayer Intelligent Contract that reviews GitHub pull requests using AI
consensus. Unlike a simple "AI decides X" wrapper, this contract fetches
the actual PR page, analyzes it across multiple categories (bugs, security,
performance, style, tests), and requires validator agreement on the
recommendation and score before committing.

## Why this matters

Code review is a critical bottleneck for open-source and enterprise teams.
By putting it on-chain with GenLayer consensus, any builder can call
`review_pr(url, focus)` and trust that the review was validated by
multiple independent LLM runs, not just one.

## How consensus is used

1. Caller submits a PR URL + focus area (all/security/bugs/style).
2. Leader fetches the PR page via `gl.nondet.web.render(pr_url, mode="text")`.
3. Leader runs `gl.nondet.exec_prompt` with a structured prompt that asks
   the LLM to analyze the code for bugs, security, performance, style,
   and missing tests, producing a JSON review with score (1-10), risk
   level, findings list, summary, and recommendation.
4. Validators re-run the same function independently.
5. `gl.eq_principle.prompt_comparative` requires validators to agree on
   the **recommendation** (APPROVE / REQUEST_CHANGES / COMMENT) and the
   **score within 2 points**. Findings may be worded differently.
6. On agreement, the result is committed to on-chain state (`TreeMap`).

## State design

- `reviews: TreeMap[str, str]` — maps a PR identifier (last path segment)
  to a JSON review string. Allows retrieval via `get_review(pr_url)`.

## Interface

| Method | Type | Description |
|--------|------|-------------|
| `review_pr(pr_url, focus)` | write | Review a PR with given focus |
| `get_review(pr_url)` | view | Retrieve last review for a PR |
| `list_reviews()` | view | List all reviewed PR keys |
| `contract_info()` | view | Contract metadata |

## Focus areas

- `all` — comprehensive review
- `security` — security-focused
- `bugs` — logic errors and bugs
- `style` — readability and conventions

## Example

```python
# Review a PR
result = contract.review_pr(
    "https://github.com/org/repo/pull/42",
    "all"
)
# → {"score": 7, "risk_level": "MEDIUM", "recommendation": "REQUEST_CHANGES", ...}
```

## Evidence

- Contract address (Studio Network): `0x2d9F945E665F4d3af6Cc7F23ce49C0A3107b2DA2`
- Deploy tx: `0xa743fa4551c9b39b099195a59dfe31797b30af58ad993e2bca1e5a3b8b57898d`
- E2E tx: `0x95909b5f5a9e60fb4c5de7079aa60ee9e8d5a317901411785ac9bed7899c669a`
- E2E result: reviewed PR → findings (2), score, recommendation
- Tests: direct-mode + Studio Network consensus

## Author

modaz
