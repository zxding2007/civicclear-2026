# Operator checklist — current app and release preparation

**Current checkout:** the redesigned app has six separate pages: Overview, Decisions, Decision details, Tax calculator, Sources & method, and Analyse a record. The earlier multi-page revision passed **57 tests**; rerun the full suite for the provider-support revision. The redesign and documentation updates are local changes; this checklist does not establish that they have been pushed or deployed.

The existing public addresses are the [GitHub Pages demo](https://zxding2007.github.io/civicclear-2026/) and the [earlier Render/Streamlit demo](https://civicclear-2026.onrender.com/). They may still show the older interface until the new code is published. Follow [publish_guide.md](publish_guide.md) for deployment; use the same existing repository and checkout.

## Before the next push

With Python 3.12 and the project dependencies installed, run from the repository root:

```bash
python build_site.py
python -m pytest -q
python -m uvicorn server:app --reload
```

Open `http://localhost:8000`. The first command regenerates all six HTML pages and the saved decision bundle. The server connects the pages to the existing Python verification pipeline and calculator. The earlier Streamlit interface is still available with `streamlit run app.py`, but it is not the redesigned app.

- [ ] Confirm the local app opens and the navigation loads separate pages.
- [ ] Confirm Overview, Decisions and saved record details disclose **pre-generated demo data**, no AI calls on browsing, and independent human review pending.
- [ ] Check all four records and their original evidence. `DM41.4` is received for information, `PH29.2` is committee-only, `PH29.1` is Council-adopted, and `CC38.1` is adopted with amendments.
- [ ] Select a ward and check the record wording. A match means the official record names the ward or is citywide; a missing ward does not rule out indirect effects.
- [ ] Open `PH29.2`: verify the advertised **November 30, 2026** feedback deadline and **Give feedback** action against the current [official City portal](https://haveyoursay.toronto.ca/LJOV-Planning-Framework-CHRA). Check the form is still available; do not infer availability from the April meeting date.
- [ ] Open the separate **Tax calculator** page. CAD 700,000 should show 2025 CAD 4,207.61, 2026 CAD 4,300.18, and CAD 92.57 difference. Confirm the City Building Fund is included, education tax excluded, and both official tax sources are linked.
- [ ] Clear or invalidate the assessed value and confirm old results disappear. Confirm the currency prefix does not overlap the amount.
- [ ] Check 375px width, keyboard navigation, visible focus, mobile-menu closing, and reduced-motion behavior.
- [ ] Check **Analyse a record** stays disabled when credentials are absent. Browsing examples and using the calculator must not call an AI service.
- [ ] Review `git status` and the intended diff before staging. Exclude credentials, environment folders, caches, and local browser artifacts. Do not create a new repository or rewrite commit history.

## After publishing

- [ ] Confirm the GitHub test and Pages workflows succeed for the intended commit.
- [ ] Open the public Pages URL and verify the new six-page navigation. Pages uses saved demo data and has no Python analysis endpoint.
- [ ] If publishing the connected app on Render, confirm its service starts `uvicorn server:app --host 0.0.0.0 --port $PORT`; merely pushing this repository does not establish that an existing Streamlit service has changed its start command.
- [ ] Open the connected app and check data loading, the Python calculator, and the analysis availability state. Let a sleeping free instance wake before recording.
- [ ] Update submission links only after verifying what each public address actually serves.

## Human review still required

- [ ] Open the item URLs in `data/items/*/meta.json` and compare every statement and quote with the **full official** item page.
- [ ] Read the relevant full staff-report PDFs and attachments, including conditions and contextual nuance. The bundled excerpts are not complete transcripts.
- [ ] Independently confirm all four `golden.json` records. Record the reviewing person's identifier and date only after the review is complete; do not copy a model's output as sign-off.
- [ ] Recheck current participation notices, including the Little Jamaica portal. Saved dates and passing tests do not prove a live form is open.
- [ ] Review the one-page readiness report and AI disclosure for consistency with the version being submitted.

## Optional live AI test

The optional Claude and DeepSeek workflows use mocked tests; no real paid request to either provider has been performed in this work. Keep that distinction in the demo and submission.

- [ ] If the team chooses to test it, set `CIVICCLEAR_PROVIDER=deepseek` plus `DEEPSEEK_API_KEY`, or `CIVICCLEAR_PROVIDER=anthropic` plus `ANTHROPIC_API_KEY`, and a strong `CIVICCLEAR_ANALYST_PASSWORD` in private environment settings. Never commit secrets. `CIVICCLEAR_MODEL` is optional; remove or replace any old override when switching providers.
- [ ] Review uploaded PDFs for personal information first. The page-text headings scrubber does **not** redact PDF content. DeepSeek receives locally extracted PDF text and rejects scans without readable text; its JSON quotation references are not native Anthropic citations.
- [ ] Submit one official record, record the actual model and cost, and compare every output and citation with the full source before reuse. An analysis preview is not saved or published automatically.
- [ ] Preserve human review as pending until a person actually completes it. A quotation match alone does not establish a correct interpretation.

## Event and submission tasks

The original event plan listed Nov 13 checkpoints at 08:00, 15:00 and 18:00 ET, and a Nov 14, 2026 final submission at 10:00 ET. Confirm the organizer's current announcements and rules; this checklist is not evidence that a checkpoint or submission occurred.

- [ ] Check which organizer checkpoints have actually been posted. Historical drafts are labelled in [checkpoints_and_devpost.md](checkpoints_and_devpost.md).
- [ ] Record and review a 2–3 minute working demo using [demo_video_script.md](demo_video_script.md).
- [ ] Verify the video, repository, app and report links without being signed in.
- [ ] Complete the Devpost fields and confirm the submission status, not just a saved draft. Observe the organizer's final cutoff for code and artifact changes.
