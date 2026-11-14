# Claude API smoke test — no paid request executed

**Status: November 13, 2026.** The four public examples are curated saved records, not real-time model responses. The latest local suite passed **57 Python tests**, including fake-SDK and mocked HTTP analysis tests. Desktop, 375-pixel mobile, keyboard and invalid-input browser checks also ran locally. None of these checks establishes successful paid inference. The latest revision has not yet been pushed or deployed by this preparation work.

## What the local tests establish

- `server.py` serves the six-page website and API together. `POST /api/analyse` requires configured credentials and the correct analyst password, validates an exact official agenda URL and item identifier, and accepts substantive text plus an optional PDF up to 20 MB.
- `pipeline/extract.py` requests a `DecisionCard`; `pipeline/explain.py` makes a separate request for a cited explanation. Returned item identifiers must match the requested item.
- `pipeline/verify.py` flags quotations that do not occur in the submitted text/PDF. It does **not** discard all unsupported narrative or judge interpretation. Unverified stages are excluded from the status rule; citation flags remain visible for review.
- `tests/test_ai_contract.py` checks the SDK request/response contract with a fake client. `tests/test_server.py` checks API access, input validation and mocked output handling without contacting Anthropic.
- Successful analysis returns an `ai_unreviewed` preview with human review pending. The server does not save or publish it. GitHub Pages cannot run this analysis endpoint.

## How an authorized administrator can perform the remaining test

1. Review the official agenda text and any report for personal or sensitive information. The cleaner removes named Communications/Speakers sections from pasted text; it does not comprehensively redact text or uploaded PDF contents.
2. Use Python 3.12 and install `requirements.txt`. Put `ANTHROPIC_API_KEY`, `CIVICCLEAR_ANALYST_PASSWORD` and `CIVICCLEAR_MODEL` in an uncommitted `.env` file or the host environment. Verify the chosen model against current Anthropic documentation before paying for a request. The configured default is not proof of account access or model availability.
3. Run `python build_site.py`, then `python -m uvicorn server:app --reload`. Open `http://localhost:8000/analyse.html`; the server reads `.env` automatically. The legacy `streamlit run app.py` path remains separate and uses shell variables or Streamlit Secrets.
4. Enter the analyst password, the exact official Toronto agenda URL, at least 100 characters of substantive sanitized source text, and optionally a reviewed PDF. Submitting the form sends the inputs through two Claude requests and can incur charges.
5. Compare the returned item ID, decision status, quotations, wards, participation facts and uncertainties against the complete official sources. Record the date, model, outcome, observed cost and reviewer findings without recording credentials. A quotation match alone is not evidence that an interpretation is correct.
6. Treat incomplete, unsupported or unverifiable results as a failed smoke test. Keep the curated records as the public default and do not publish unreviewed output. The curated examples also still require independent human sign-off.

**Paid API execution record: NOT EXECUTED.** No real Anthropic request has been performed in this workflow. A real run and its reviewer record are required before changing this status to passed.
