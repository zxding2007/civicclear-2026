# CIVIC Hack 2026 — checkpoint history and current submission draft

**Current release status:** the six-page redesign and Python connection are implemented in this local checkout; the earlier multi-page revision passed **57 tests**. Provider support uses mocked tests; rerun the full suite for the current result. These documentation changes do not establish a push, public deployment, video upload or Devpost submission. The existing public URLs may still serve the older website/Streamlit version. Confirm each external result before describing it as complete.

**Historical drafts below:** the checkpoint wording is retained as it was drafted, including its references to the earlier Streamlit demo. It is not a current deployment report or proof that anything was posted. Do not repost it unchanged. The original event plan listed a November 14, 2026, 10:00 AM ET deadline; verify the organizer's applicable rules and announcements.

## Historical Checkpoint 1 — Friday Nov 13, 08:00 ET (draft; posting unverified)

**Problem / user:** Toronto residents often mistake recommendations and committee steps for final Council decisions, and struggle to find current ways to participate.  
**Idea:** CivicClear is a source-linked municipal decision explorer with ward clues, transparent status, stakeholder considerations and verified participation links.

## Historical Checkpoint 2 — Friday Nov 13, 15:00 ET (draft; posting unverified)

We have a public Streamlit demo at https://civicclear-2026.onrender.com/ with four Toronto agenda records, stage-by-stage Council Decoder, linked evidence, a stakeholder impact section, and 2025/2026 municipal tax comparison. The deterministic tests pass. The live Claude API has **not** been tested and a complete team review is pending.

## Historical Checkpoint 3 — Friday Nov 13, 18:00 ET (draft; posting unverified)

CivicClear now distinguishes a committee decision from final Council adoption, shows a sourced Nov 30 feedback mapping opportunity for Little Jamaica, and separates documented priorities from possible effects for residents and local businesses. GitHub and the deployed app are public. We are finalizing the 2–3 minute video and one-page readiness report before submission.

## Earlier final-checkpoint draft — Saturday Nov 14, 08:00 ET (posting unverified)

Repository, functioning app, and one-page Municipal Readiness Report are ready. Check demo video upload, source audit disclaimer, AI credits, and all Devpost fields before the 10:00 AM ET code freeze. **Do not post 'submitted' unless Devpost confirms.**


## Current progress update — review before posting

CivicClear now has separate Overview, Decisions, Decision details, Tax calculator, Sources & method, and Analyse a record pages in the local checkout. FastAPI connects them to the existing Python verification pipeline and tax calculator. The public Pages build can use the same pages with saved data. The earlier multi-page revision passed 57 local tests; the provider-support revision uses mocked tests and needs its current full-suite result recorded. The four demo records are pre-generated, browsing does not call AI, independent human source/report review remains pending, and the optional Claude and DeepSeek workflows have only been tested with mocks. The redesigned version still needs the intended GitHub push and verified public deployment before we describe it as live. Video upload and final submission must be confirmed separately.

---

# Devpost project description — current draft

Review deployment wording, teammates, video URL and the report before copying this into Devpost. Replace the release-status sentence only after the new public version has been verified.

## CivicClear — City Decisions, Decoded

**Inspiration.** Toronto residents have access to municipal records, but official procedural terms can hide an essential distinction: a councillor's proposal, a committee direction, and an adopted City Council item do not mean the same thing. Confusion can also cause residents to miss public participation opportunities.

**What it does.** CivicClear presents four curated City of Toronto agenda examples in an app with separate pages for Overview, Decisions, Decision details, Tax calculator, Sources & method, and authorised record analysis. It separates staff recommendations, committee actions and Council decisions; identifies wards named in the record without treating them as an individual-impact boundary; defines procedural language; and links supporting evidence. A stakeholder view distinguishes documented priorities from possible effects and open questions for residents, businesses and community organizations. Little Jamaica's detail page prominently shows the City's advertised November 30, 2026 feedback deadline and a **Give feedback** action to the official interactive map; users are told to confirm the form remains open. The separate calculator compares 2025 and 2026 residential municipal property tax at a constant MPAC assessment, including the City Building Fund and excluding education tax. It is an illustrative comparison, not a personal bill forecast.

**How we built it.** Python 3.12, FastAPI, Pydantic, plain HTML/CSS/JavaScript, and pytest. Six HTML documents are generated from a shared template; ordinary links load the pages. The connected app serves those pages and an API from one Python service. It loads saved records through the existing verification pipeline and calculates tax with the existing Python calculator. The static Pages build packages the records into a JavaScript data file and performs the tax comparison locally; it has no Python server or analysis endpoint. Separate code rules use matched source quotations to determine decision status. Optional administrator analysis selects Claude or DeepSeek, makes separate extraction and explanation requests, and returns an unreviewed preview without saving or publishing it. DeepSeek uses JSON output, Pydantic validation and locally checked quotation references; PDF text is extracted locally, and unreadable scans are rejected. It does not claim native Anthropic citation equivalence. Claude retains its existing document-citation flow. Provider keys remain on the server. The earlier Streamlit interface remains in the repository.

**What has been verified.** The earlier multi-page revision passed 57 tests, including API tests with mocked responses. Provider support uses mocks; the final current test count should be recorded after a full-suite run. The four examples disclose that they are pre-generated and browsing does not call AI. Automated quote checks do not prove a correct interpretation or complete-document review. Independent human review of the full official records and staff reports remains pending, and neither optional provider has been tested with a real paid API call.

**Release status.** The redesigned app is implemented locally. The repository and earlier public demos already exist, but this description does not claim the new version has been pushed or deployed. We will verify the actual public pages and connected service before updating that claim in the submission.

**Challenges and lessons.** We learned that “received for information” is not project approval and that a committee's amended direction to consult is not final adoption. A consultation deadline in an older agenda item can differ from the City's newer project portal, so the two sources must be checked separately. Causal and economic effects cannot safely be inferred from planning priorities. The interface keeps source evidence, uncertainty, pending human review and the distinction between saved examples and optional live analysis visible.

**Potential impact and next steps.** CivicClear offers residents a way to navigate complex public records and gives municipal staff a source-linked prototype to evaluate. Next steps include full-report human review, real selected-provider end-to-end testing, accessibility and language testing, monitoring for source and consultation updates, and community usability trials.

**Links to verify for submission.** [GitHub repository](https://github.com/zxding2007/civicclear-2026) · [Existing Pages demo](https://zxding2007.github.io/civicclear-2026/) · [Existing Render address, previously Streamlit](https://civicclear-2026.onrender.com/) · [Municipal Readiness Report (PDF; review against the current app)](https://github.com/zxding2007/civicclear-2026/blob/main/docs/readiness_report.pdf) · **Demo video: [INSERT VERIFIED REAL VIDEO URL]**. Public links can continue to show an older version until the new deployment succeeds.

**AI / libraries / data credits.** OpenAI ChatGPT assisted with Python and app code, curated content, documentation, checks and report drafts. Claude Code assisted with the earlier static website; the detailed provenance is in the disclosure. The bundled cards are curated examples, not evidence of live Claude or DeepSeek API execution. Data comes from City of Toronto TMMIS agenda records, City planning/project consultation pages, and official 2025/2026 property-tax sources. Libraries include FastAPI, Uvicorn, python-multipart, HTTPX, Streamlit, Pydantic, pypdf, pytest, python-dotenv and the Anthropic Python SDK. See the [complete disclosure](https://github.com/zxding2007/civicclear-2026/blob/main/docs/ai_usage.md), [source list](https://github.com/zxding2007/civicclear-2026/blob/main/docs/sources.md) and [AI-assisted official-source cross-check](https://github.com/zxding2007/civicclear-2026/blob/main/docs/official_source_audit_2026-11-12.md). Add any further teammate tools before submission; an AI cross-check is not independent human sign-off.
