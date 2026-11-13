# Claude API smoke test — not yet executed with paid credentials

**Reason for this file:** The judge should be able to see exactly what has and has not run. The public CivicClear demonstration uses cached curated records. No Anthropic key has been provided; an actual Claude request has **not** been executed.

## What is ready

- `pipeline/extract.py`: strict `DecisionCard` structure and conservative system instructions.
- `pipeline/explain.py`: separate source-citation pass.
- `pipeline/verify.py`: compare returned quotations against supplied text/PDF; discard unsupported cited statements.
- `tests/test_ai_contract.py`: local fake-SDK API contract tests, **not** real inference.

## How an authorized administrator could test in a private environment

1. Review the original item page and any supporting PDF for personal/sensitive information. Public correspondence and speaker names should **not** be sent to a third-party AI account by default.
2. Store `ANTHROPIC_API_KEY` and `CIVICCLEAR_ANALYST_PASSWORD` in a secure, uncommitted environment or provider secret manager; never post either value in GitHub, ChatGPT messages or the video.
3. Use a *current, known-supported* model in `CIVICCLEAR_MODEL`, checked against Anthropic's documentation, and set appropriate rate/budget caps.
4. Open the admin screen; paste *sanitized* official text and optionally a cleaned PDF; run the two-call process.
5. Compare resulting decision status, individual verbatim citations, ward and participation facts to primary source; record precise deviations and API cost. Do not publish any unreviewed output.
6. If an unsupported or unverified result appears, label the test failed and keep cached curated demo as the public default.

**Execution record:** NOT EXECUTED (no real Anthropic API key available in this workflow). Do not replace this statement with a claimed pass unless a real run and reviewer record exist.
