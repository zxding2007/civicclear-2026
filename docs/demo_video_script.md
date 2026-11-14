# CivicClear — 2:42 working-app recording script

**Length goal:** 2 minutes 42 seconds; keep the final cut between 2 and 3 minutes. Show the real running app, not slides or fabricated outputs.

**Version to record:** this checkout's six-page app. From the repository root run `python build_site.py`, `python -m pytest -q`, then `python -m uvicorn server:app --reload`; open `http://localhost:8000`. The current local suite passes 57 tests. A recording of this local app is valid evidence of local behavior, not evidence of a public deployment. The existing [Pages URL](https://zxding2007.github.io/civicclear-2026/) and [Render URL](https://civicclear-2026.onrender.com/) may still show older code until the redesign is pushed and deployed. If recording a hosted version, verify it shows the pages below first.

| Time | Demonstrate on screen | Spoken English narration |
| --- | --- | --- |
| 0:00–0:17 | Open **Overview**, show sidebar and pre-generated-data disclosure | “City decisions are public, but their wording can be hard to follow. CivicClear is a workspace for understanding Toronto decisions. These four examples are pre-generated; browsing does not call AI, and independent human review is pending.” |
| 0:17–0:44 | Open **Decisions**, then **DM41.4**. Expand the Council timeline wording | “This motion asked about reinstating Cummer Station. Council received it for information. That is not approval, funding, or a promise to build. The status comes from rules applied to source-matched decision wording.” |
| 0:44–1:19 | Open **PH29.2**, show Committee-only status, then **Who it affects** and a claim source | “For Little Jamaica and Oakwood Vaughan, the committee advanced consultation on a draft framework. That is not final Council adoption. The stakeholder view separates documented priorities from possible effects and questions. A ward listed in a record is a geographic clue, not a prediction of anyone’s individual impact.” |
| 1:19–1:46 | Show the prominent feedback deadline and **Give feedback** action on PH29.2. Open the official portal, then return | “A separate City portal advertises an interactive feedback map through November 30, 2026. This button goes to that official tool. Residents should confirm the form is still open. This feedback opportunity is separate from the historical committee decision.” |
| 1:46–2:06 | Open **PH29.1**, show its three-stage timeline and **Unknowns** tab | “This record shows staff recommendation, committee action, and Council adoption as separate steps. Conditions and uncertainties stay visible, including approvals that may be needed before implementing the by-laws.” |
| 2:06–2:30 | Open the separate **Tax calculator** page, enter CAD 700,000, calculate, and show rate-source links | “The calculator compares the same MPAC assessment using the 2025 and 2026 residential municipal rates. It includes the City Building Fund and excludes education tax. The estimated difference is ninety-two dollars and fifty-seven cents, not a forecast of a household’s actual bill.” |
| 2:30–2:42 | Open **Sources & method**; briefly point to **Analyse a record** in navigation | “The connected app uses Python for checks and calculations. Optional analyst AI is separate and has only been tested with mocks. Full-source human review remains our next step.” |

## Before recording

1. Build and test the same checkout you will record. Rehearse the separate-page navigation, detail tabs and source links. Keep text legible at 1080p.
2. Verify the current official Little Jamaica participation page. If the advertised date has changed or the form is no longer open, update the source data and narration; do not stage an open opportunity that the City no longer offers.
3. Use OBS, QuickTime, Windows Game Bar or another screen recorder to capture the actual browser and interactions. If showing the local app, do not call it the newly deployed public version.
4. Avoid showing credentials, cookies, private browser tabs or personal correspondence. No real AI request is required for this recording.
5. Export MP4/H.264, replay it fully, check sound and legibility, and verify the duration is under 3 minutes. Upload a public or unlisted accessible link and test it without signing in.
6. Do not claim real Claude API execution, a complete Council feed, measured economic impacts, or independent municipal sign-off. The saved demo and 57 passing tests do not establish those claims.

## Optional one-sentence judge summary

“CivicClear helps Toronto residents follow what the City actually decided, inspect the original evidence, and find advertised feedback opportunities without confusing proposals, committee actions and Council decisions.”
