# CIVIC Hack 2026 — ready-to-review checkpoints and Devpost content

**Status:** Content prepared. Do not claim the Discord posts, the demo video or final Devpost submission has happened until verified in those accounts. Deadline is November 14, 2026 at 10:00 AM ET.

## Checkpoint 1 — Friday Nov 13, 08:00 ET (draft)

**Problem / user:** Toronto residents often mistake recommendations and committee steps for final Council decisions, and struggle to find current ways to participate.  
**Idea:** CivicClear is a source-linked municipal decision explorer with ward clues, transparent status, stakeholder considerations and verified participation links.

## Checkpoint 2 — Friday Nov 13, 15:00 ET (draft; verify facts before posting)

We have a public Streamlit demo at https://civicclear-2026.onrender.com/ with four Toronto agenda records, stage-by-stage Council Decoder, linked evidence, a stakeholder impact section, and 2025/2026 municipal tax comparison. The deterministic tests pass. The live Claude API has **not** been tested and a complete team review is pending.

## Checkpoint 3 — Friday Nov 13, 18:00 ET (draft; verify facts before posting)

CivicClear now distinguishes a committee decision from final Council adoption, shows a sourced Nov 30 feedback mapping opportunity for Little Jamaica, and separates documented priorities from possible effects for residents and local businesses. GitHub and the deployed app are public. We are finalizing the 2–3 minute video and one-page readiness report before submission.

## Final checkpoint — Saturday Nov 14, 08:00 ET (draft; verify status first)

Repository, functioning app, and one-page Municipal Readiness Report are ready. Check demo video upload, source audit disclaimer, AI credits, and all Devpost fields before the 10:00 AM ET code freeze. **Do not post 'submitted' unless Devpost confirms.**

---

# Devpost project description (copy-ready, update teammates and video URL)

## CivicClear — City Decisions, Decoded

**Inspiration.** Toronto residents have access to municipal records, but official procedural terms can hide an essential distinction: a councillor's proposal, a committee direction, and an adopted City Council item do not mean the same thing. Confusion can also cause residents to miss real public participation opportunities.

**What it does.** CivicClear turns real City of Toronto TMMIS agenda items into source-linked, plain-language cards. It separates staff recommendations, committee actions and City Council decisions; identifies the wards named in the record; defines procedural language; and provides explicit evidence links. A stakeholder view distinguishes documented planning priorities from possible effects and open questions for residents, businesses and organizations. Its Have Your Say panel is conservative: no current deadline is invented. For the Little Jamaica and Oakwood Vaughan case it links the City's specific interactive feedback map and its November 30, 2026 advertised deadline. A second example compares Toronto's 2025 and 2026 residential municipal property-tax rates at an unchanged MPAC assessment, **not** a personal bill forecast.

**How we built it.** Python 3.12, Streamlit, Pydantic and pytest. The public website (https://zxding2007.github.io/civicclear-2026/) is a static HTML page published to GitHub Pages: a build script reruns the quote and status checks and bundles the four records, and the page needs no server or model call. The Streamlit app deploys the same code from GitHub to Render on its free service and loads four curated public-source examples without model costs. Separate Python rules use source-matched excerpts to determine the decision stage. Source-specific links and evidence boundaries are explicit; a code test does not prove the City's full record was manually signed off. The optional Anthropic Claude API extraction/citation integration is implemented and protected behind an administrator password, but has **not** been executed with a real API key for this submission.

**Challenges and lessons.** We learned that 'received for information' is not project approval and that a committee's amended direction to consult is not final adoption. A consultation deadline in an older agenda item can differ from the City's newer project portal, so we cross-checked both separately. We also learned that causal and economic effects cannot safely be invented from planning priorities. We use cautious language, link each substantive claim to City evidence, and require a human review before any municipal production use.

**Potential impact and next steps.** CivicClear offers a resident-friendly, low-cost way to navigate complex public records and an auditable workflow a municipal clerk or engagement team could adapt. Next steps are municipal staff review of complete reports/attachments, real Claude API end-to-end testing, accessibility and language testing, monitoring for status updates and consultation deadlines, and community usability trials.

**Links.** [Live website](https://zxding2007.github.io/civicclear-2026/) · [GitHub repository](https://github.com/zxding2007/civicclear-2026) · [Streamlit demo](https://civicclear-2026.onrender.com/) · [One-page Municipal Readiness Report (PDF)](https://github.com/zxding2007/civicclear-2026/blob/main/docs/readiness_report.pdf) · **Demo video: [INSERT VERIFIED REAL VIDEO URL]**.

**AI / libraries / data credits.** OpenAI ChatGPT (GPT-6) assisted with code, content, documentation, quality checks and report drafts. The bundled source-linked cards are curated, not evidence of Claude API execution. Optional Anthropic SDK/Claude code is provided but no live paid model inference is claimed. Data: City of Toronto TMMIS agenda records, City planning/project consultation pages, and official 2025/2026 property-tax by-laws. Libraries include Streamlit, Pydantic, pypdf, pytest, python-dotenv and the Anthropic Python SDK. [Complete disclosure](https://github.com/zxding2007/civicclear-2026/blob/main/docs/ai_usage.md), [source list](https://github.com/zxding2007/civicclear-2026/blob/main/docs/sources.md) and [official-source audit](https://github.com/zxding2007/civicclear-2026/blob/main/docs/official_source_audit_2026-11-12.md) are in the repository. Add any further AI tools used by other teammates before submission.
