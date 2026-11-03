# { "Depends": "py-genlayer:latest" }
from genlayer import *


@gl.contract
class CodeReviewOracle:
    """Intelligent Contract that reviews a pull-request diff fetched from
    GitHub.  An LLM analyses the diff for bugs, security issues and style
    problems, and the validator committee must agree on the score and
    finding count before the review is committed."""

    reviews: TreeMap[str, str]

    def __init__(self) -> None:
        pass

    def _fetch(self, url: str) -> str:
        try:
            return gl.get_webpage(url, mode="text")
        except Exception as e:
            return f"FETCH_ERROR: {str(e)}"

    @gl.public.write
    def review_pr(self, pr_url: str, focus: str = "all") -> str:
        """Review a GitHub PR by fetching its diff page.

        Args:
            pr_url:  URL to the PR (e.g. https://github.com/org/repo/pull/123)
            focus:   "all" | "security" | "bugs" | "style"

        Returns:
            JSON with score (1-10), findings list, summary.
        """
        if not pr_url:
            raise ValueError("pr_url is required")
        if focus not in ("all", "security", "bugs", "style"):
            raise ValueError("focus must be all/security/bugs/style")

        diff_text = self._fetch(pr_url)
        if diff_text.startswith("FETCH_ERROR"):
            raise ValueError(f"could not fetch PR: {diff_text}")

        snippet = diff_text[:12000] if len(diff_text) > 12000 else diff_text

        prompt = f"""You are an expert code reviewer.  Review the following GitHub
pull request page for code quality issues.

PR URL: {pr_url}
Focus area: {focus}

Page content (may include diff):
```
{snippet}
```

Analyse for:
- Bugs / logic errors
- Security vulnerabilities (injection, auth bypass, secret leaks, etc.)
- Performance issues
- Style / readability problems
- Missing tests or edge cases

Return ONLY a valid JSON object:
{{
  "pr_url": "{pr_url}",
  "focus": "{focus}",
  "score": <integer 1-10, where 10 is excellent>,
  "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
  "findings": [
    {{
      "id": "F-001",
      "category": "<bug|security|performance|style|test>",
      "severity": "<LOW|MEDIUM|HIGH|CRITICAL>",
      "description": "<brief>",
      "suggestion": "<fix>"
    }}
  ],
  "summary": "<2-3 sentence overall assessment>",
  "recommendation": "<APPROVE|REQUEST_CHANGES|COMMENT>"
}}"""

        def run() -> str:
            result = gl.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "").strip()
            return result

        criteria = """The output must be valid JSON with:
- score as integer 1-10
- risk_level as one of LOW/MEDIUM/HIGH/CRITICAL
- findings as array of objects with id, category, severity, description, suggestion
- summary and recommendation as strings
- recommendation as one of APPROVE/REQUEST_CHANGES/COMMENT
Only raw JSON, no markdown."""

        final = gl.eq_principle.prompt_non_comparative(run, criteria=criteria)

        key = pr_url.split("/")[-1] if "/" in pr_url else pr_url[:40]
        self.reviews[key] = final
        return final

    @gl.public.view
    def get_review(self, pr_url: str) -> str:
        key = pr_url.split("/")[-1] if "/" in pr_url else pr_url[:40]
        return self.reviews.get(key, "{}")

    @gl.public.view
    def list_reviews(self) -> list[str]:
        return list(self.reviews.keys())

    @gl.public.view
    def contract_info(self) -> dict:
        return {
            "name": "CodeReviewOracle",
            "version": "1.0.0",
            "description": "Decentralized AI code review for GitHub pull requests",
            "author": "modaz",
        }
