# Final operator checklist — video and Devpost

**The real screen recording, uploads and authenticated Devpost submission are not completed by this repository.** Do not claim those actions occurred until a person verifies them.

## Prepare the version to record

The current checkout contains a six-page app: Overview, Decisions, Decision details, Tax calculator, Sources & method, and Analyse a record. It uses FastAPI to connect the browser to the existing Python pipeline and calculator. GitHub Pages can serve the same pages with saved data, without a Python backend.

Run from the repository root with Python 3.12 and dependencies installed:

```bash
python build_site.py
python -m pytest -q
python -m uvicorn server:app --reload
```

Open `http://localhost:8000`. The latest local suite passed **57 tests**, including mocked API tests. No real paid AI call or full-source human sign-off is implied.

The redesigned code has not been pushed or deployed as part of these preparation steps. The existing public [Pages demo](https://zxding2007.github.io/civicclear-2026/) and [earlier Render/Streamlit demo](https://civicclear-2026.onrender.com/) may still show the older interface. Follow [publish_guide.md](publish_guide.md) and verify the intended public version before describing it as deployed.

## Record and validate the video

- [ ] Use [demo_video_script.md](demo_video_script.md), targeting 2–3 minutes of the actual working app.
- [ ] State the project name and intended users. Show the **pre-generated demo data** notice and human-review status; explain that browsing does not call AI.
- [ ] Rehearse all four record selections and the separate Tax calculator page. If recording a hosted instance, wake it first and verify it is the updated version.
- [ ] Demonstrate PH29.2's committee-only status, stakeholder evidence, and prominent **Give feedback** action. Recheck the official portal's advertised Nov 30, 2026 deadline and current availability before narrating it.
- [ ] Show municipal tax source links and explain City Building Fund included / education tax excluded at a constant MPAC assessment.
- [ ] Record only the relevant browser window or tab, with legible text and clear audio. Keep private tabs and credentials out of the capture.
- [ ] Replay the final MP4, verify the 2–3 minute runtime, and test the uploaded link without being signed in.

## Submission fields to verify

- **Project:** CivicClear — City Decisions, Decoded
- **Code repository:** https://github.com/zxding2007/civicclear-2026 — confirm the intended commit is pushed and visible.
- **Public saved-data demo:** https://zxding2007.github.io/civicclear-2026/ — verify the new six-page version after Pages deployment.
- **Connected Python app:** use the verified deployed URL after updating the service. The existing https://civicclear-2026.onrender.com/ address previously served Streamlit; the local redesign alone does not update it.
- **Local recording address:** `http://localhost:8000` is for recording/testing only and is not a public submission URL.
- **One-page Municipal Readiness Report:** https://github.com/zxding2007/civicclear-2026/blob/main/docs/readiness_report.pdf — review its contents against the current app and confirm it is one page before attaching it.
- **2–3 minute demo video:** **[TO BE RECORDED AND PUBLISHED — add a verified URL]**
- **Project description:** review the current draft in [checkpoints_and_devpost.md](checkpoints_and_devpost.md), especially the deployment status and teammate credits.
- **AI disclosures:** [ai_usage.md](ai_usage.md); include all teammate tools actually used. Optional Claude analysis has only been tested with mocks; source/report human review is pending.

## External completion items

- [ ] Confirm the organizer's final-time announcements and [official rules](https://civic-hack-2026.devpost.com/rules). The original plan listed **Nov 14, 2026 at 10:00 AM ET**; observe the applicable cutoff for code and artifact changes.
- [ ] Verify which organizer checkpoints were actually posted. The earlier drafts in [checkpoints_and_devpost.md](checkpoints_and_devpost.md) are historical text, not proof of posting.
- [ ] Assign a real teammate to review full official records and attachments. Do not mark human review complete based on automated or AI-assisted checks.
- [ ] Verify all public links and attachments, complete Devpost, and confirm the account shows **Submitted**, not Draft.
