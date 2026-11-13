# Organizer checkpoints and Devpost submission draft

These are **drafts to review and post** in the organizers' specified Discord channels and Devpost. Nothing has been posted or submitted.

## Checkpoint 1 — Friday Nov 13, 08:00 ET

**Problem and user:** Toronto residents struggle to distinguish municipal staff proposals, committee actions and final Council decisions—and to know if they can still comment.

**Idea:** CivicClear translates official Toronto agenda records into stage-aware, ward-aware, source-linked explainers, with clear uncertainty about participation deadlines.

## Checkpoint 2 — Friday Nov 13, 15:00 ET

We built a Streamlit prototype displaying four verified-item-status examples, source-linked evidence excerpts, ward filtering and a municipal residential tax comparison; 14 offline tests passed. Next: independent human review of complete records and optional API/deployment smoke tests.

## Checkpoint 3 — Friday Nov 13, 18:00 ET

CivicClear separates recommendations from decisions, checks source quotes before applying decision rules, and avoids inventing engagement deadlines. We are preparing the 1-page readiness report, demo video and Devpost entry. [Before posting, replace this with the actual state of work at 18:00.]

## Devpost project description (English)

**Project title:** CivicClear — City Decisions, Decoded

**Inspiration.** Public council records contain important decisions, but procedural words like “received for information” and “adopted with amendments” can obscure what was truly approved. A resident may mistake an unapproved motion for a new public project or treat a committee step as the end of a policy process.

**What it does.** CivicClear presents actual Toronto agenda items as plain-language decision cards. It distinguishes staff recommendations, committee actions and City Council decisions; identifies affected wards; provides verbatim source links; explains relevant procedural phrases; and clearly indicates when current public-participation details are unverified. A residential property-tax comparison demonstrates a numeric “Before & After” view using the City's adopted municipal rates.

**How we built it.** Python, Streamlit, Pydantic and pytest power a source-linked public demo. Optional admin-only Claude API calls separately perform structured extraction and cited explanation. A code-based status classifier considers only verified stage quotes. The source-backed fixtures cover four council decision patterns, and 14 offline tests check core logic. [Update with full report reviews and actual API tests completed, if any.]

**Challenges and lessons.** A recommendation in a staff report is not the same thing as the final Council decision. A mention of future consultation does not establish that registration is open. Exact quote matching is useful but cannot replace contextual or legal review. Reliable municipal AI requires transparent uncertainty and a human sign-off step.

**Impact and next steps.** Clerks, outreach teams and council offices could use a moderated workflow to produce resident-facing explainers more quickly. Future work includes more agenda types, checked meeting calendars, multilingual and accessible output, geocoded ward lookup and municipal staff approval controls.

**Required final links (replace before submission):** GitHub: `[ADD PUBLIC REPO URL]`; prototype (optional): `[ADD URL]`; 2–3 min demo: `[ADD VIDEO URL]`; one-page report: `docs/readiness_report.pdf`.

**AI and open-source disclosure:** See `docs/ai_usage.md` and `docs/sources.md` and update with the tools used by *every* teammate.
