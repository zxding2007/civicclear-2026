# AI provider smoke test — no paid request executed

The four public examples are pre-generated saved records. Browsing them does not call Claude or DeepSeek. The earlier multi-page revision passed **57 Python tests** and targeted local browser checks; provider support uses mocked tests. Run `python -m pytest -q` for the current revision's result. A passing mocked test is not a successful paid inference or a provider-account access check. No new deployment was performed for provider support.

## Provider configuration

Set a provider and the matching key, plus `CIVICCLEAR_ANALYST_PASSWORD`, in a private `.env` or host environment. `server.py` and the cache CLI load `.env`; the legacy Streamlit interface can use environment variables or Streamlit Secrets. Keys are never sent to browser code.

| Setting | DeepSeek | Claude |
| --- | --- | --- |
| `CIVICCLEAR_PROVIDER` | `deepseek` | `anthropic` |
| Required provider key | `DEEPSEEK_API_KEY` | `ANTHROPIC_API_KEY` |
| Default model when no override is set | `deepseek-flash` | Existing `claude-opus-5-5` |
| Optional override | `CIVICCLEAR_MODEL` | `CIVICCLEAR_MODEL` |

Remove or replace a model override when switching provider. If `CIVICCLEAR_PROVIDER` is absent, DeepSeek is selected only when its key exists and the Anthropic key does not; otherwise Anthropic is selected. Explicit selection avoids ambiguity if both keys are configured. The defaults are not proof that an account has access.

The [DeepSeek API documentation](https://api-docs.deepseek.com/) lists its current model names and API endpoint; its [JSON output guide](https://api-docs.deepseek.com/guides/json_mode/) describes the output mode used here. Check current provider documentation and account access before running a paid test.

## What the paths do

- The connected API requires the selected provider's configured key and the correct analyst password, checks the exact official agenda URL and item identifier, and accepts substantive text plus an optional PDF up to 20 MB. The cache CLI is an explicit operator action and does not require the web password.
- Claude retains the existing two-pass Anthropic flow: a structured `DecisionCard`, then a native document-cited explanation.
- DeepSeek makes two JSON requests. The first is validated as a `DecisionCard`; the second supplies explanation segments and model-provided quotation references. Those references are checked against the supplied sources. They are **not** native Anthropic citation objects or proof of correct interpretation.
- For DeepSeek, PDF text is extracted locally before the request. Scanned or otherwise unreadable PDFs are rejected; no OCR or native PDF-input workflow is provided by this integration. Supply readable official text instead.
- Local source checks exclude unmatched stages from the status rule and flag unmatched explanation quotations. They do not discard every unsupported narrative or establish that a statement is correct in context.
- A successful connected analysis returns an `ai_unreviewed` preview with human review pending. It does not save or publish the result. The cache CLI can write explicitly requested unreviewed files. GitHub Pages has no analysis endpoint.

## Remaining authorized live test

1. Review the official text and report for personal or sensitive information. Removing named Communications/Speakers sections is not comprehensive redaction, and does not redact uploaded PDFs.
2. Install the Python 3.12 requirements, choose one provider in the private environment, fill its API key and analyst password, and remove any stale model override. `.env.example` intentionally has blank secrets so copying it does not enable analysis.
3. Run `python build_site.py`, then `python -m uvicorn server:app --reload`. Open `http://localhost:8000/analyse.html` and confirm the displayed provider before submitting.
4. Enter the password, exact official Toronto agenda URL, and at least 100 characters of substantive sanitized source text. Optionally attach a reviewed readable PDF. Submitting sends the supplied source material to the selected provider through two requests and can incur charges.
5. Compare the item ID, decision stages, quotation references, wards, participation facts and uncertainties against the complete official sources. Record the date, provider, actual model, outcome, observed cost and human reviewer findings without recording credentials.
6. Treat incomplete, unsupported or unverifiable results as a failed smoke test. Keep the curated records as the default and do not publish unreviewed output. The curated examples still need independent human sign-off too.

**Paid API execution record: NOT EXECUTED.** No real Claude or DeepSeek inference request has been performed in this work. A real request and its reviewer record are required before changing this status to passed.
