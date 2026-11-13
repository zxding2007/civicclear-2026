# Operator checklist (required human tasks)

## Friday Nov 13 — before 08:00 ET

- [ ] Open `data/items/*/meta.json` item URLs and compare every statement and quote to the **full official** item page.
- [ ] Read each relevant staff report PDF, review contextual nuance, and add any required conditions.
- [ ] Confirm all 4 `golden.json` records independently; replace `checked_by` with the reviewing person's identifier and date. Do not merely copy the model output.
- [ ] Read [Toronto Have Your Say](https://www.toronto.ca/city-government/council/council-committee-meetings/have-your-say/) plus the actual meeting calendar to confirm whether any participation window is open.
- [ ] Run `python -m pytest -q` and `streamlit run app.py` locally.
- [ ] Publish a public GitHub repository and preserve legitimate chronological commits; check `.gitignore` before any commits.
- [ ] Submit Checkpoint 1 in the organizer's requested Discord channel. Location is not established by the plan; use participant announcements.

## Friday Nov 13 — before 15:00 / 18:00 ET

- [ ] Post Checkpoint 2 and 3 in the announced organizer channels.
- [ ] If testing live AI, create API credentials under the team's Anthropic account and a strong admin password. Test 1 item, log total cost, and compare each output with independent source records.
- [ ] Validate actual API library versions (`pip freeze`); check rate limits, data handling and consent implications for uploads.
- [ ] Deploy via Streamlit Community Cloud (optional but useful); open the live URL in a private browser session to verify.
- [ ] Recheck resident-facing copy, citation links, phone screen dimensions, print view and accessibility.
- [ ] Get teammate review of `docs/readiness_report.pdf` and cite the correct model/cost numbers.

## Saturday Nov 14 — 07:00–09:30 ET

- [ ] Record 2–3 minute **actual working** demo; verify audio and legibility, especially source links.
- [ ] Copy/update the Devpost draft, with real GitHub URL, optional app URL, video URL and report attachment.
- [ ] Attach `docs/readiness_report.pdf`; confirm 1 page.
- [ ] Publish and independently re-open all links; wake the hosted app.
- [ ] Submit **before 10:00 ET** (hard stop). No code or artifact edits after the official cutoff.

## Security and accuracy risks to decide before launch

- [ ] Review the full PDF for email addresses, correspondents or other citizen identifiers before uploading to an external LLM. A headings-based scrubber of page text does **not** scrub the PDF itself.
- [ ] Current calendar and comment deadlines were not established by this build. Preserve the explicit uncertainty message unless manually confirmed.
- [ ] Curated demo source snippets are extracts, **not** official full transcripts.
- [ ] A quote's presence in a document does not prove the AI interpretation is accurate.
- [ ] If there is no paid API access, keep the admin page disabled and demonstrate the fully functional source-linked static app.
