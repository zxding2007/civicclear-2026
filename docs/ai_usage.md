# AI assistance, provenance and testing disclosure (updated Nov 13, 2026)

This disclosure accompanies the source code and hackathon submission. It explicitly separates **curated examples**, **mocked API contract tests**, and **real external AI calls**.

| Workstream | AI role | What was actually tested |
| --- | --- | --- |
| CivicClear source and app | OpenAI ChatGPT (GPT-6) helped author/refine Streamlit, Python source/fixtures, source metadata, Impact Analysis UI and docs | Python unit tests, syntax checks, GitHub Actions, Render live site. Manual review of AI-written code is still advisable. |
| Four public demo cards | ChatGPT drafted concise cards after inspecting official City records | Source-linked curated extracts and independent AI source cross-check. **Not** Claude-generated production API output. No claim of a signed municipal audit. |
| Claude API interface | Optional Anthropic Python SDK client for two-stage structured extraction + cited narrative | Code path and fake-client tests only if present. **No real Claude requests or API charges have been performed** without ANTHROPIC_API_KEY. Do not describe this as live-tested. |
| Stakeholder considerations | ChatGPT authored candidate resident/business/community issues from City planning descriptions | Two Toronto agenda cases with direct primary-source links. Possible effects are not measured outcomes or endorsed policy positions. |
| Documentation / report | ChatGPT generated drafts and presentation narration | Human/team confirmation and final video recording remain the submitter's responsibility. |
| Original static website (`site/`), `build_site.py`, `tests/test_site.py`, `.github/workflows/pages.yml` | Anthropic Claude (Claude Code, Claude Opus 5.5) wrote the original landing page, the build script, its tests and the publishing workflow; see the `Co-Authored-By` lines on commits `f54e108` and `0ea892f` | At that revision: Python tests (30 passing), the build's status-mismatch stop, GitHub Actions publish, manual look at desktop and phone widths. |
| Review and corrections on Nov 13 | Anthropic Claude (Claude Code, Claude Fable 5.2) reviewed the repository against the challenge brief and edited the website wording, `README.md`, this file and `docs/sources.md` | Tests and site build rerun after the edits. |
| Latest multi-page application and Python API revision, Nov 13 | OpenAI Codex assisted with replacing the landing page with six separate HTML pages, adding `server.py` and API tests, correcting calculator input spacing/validation and provenance/ward/feedback wording, and updating deployment configuration and documentation | **57 Python tests passed**, including mocked analysis requests. Browser checks covered separate page navigation, search, ward filtering, connected tax calculations, invalid-input result clearing, keyboard navigation, a 375px mobile layout, and the saved-data fallback. These are targeted checks, not a full accessibility audit. No real Claude API request or deployment of this revision is established by these tests. |

## Third-party design code

`site/assets/` is the **taste-skill** frontend kit (`system.css`, `system.js`, and the `ui`, `layout`, `motion`, `moments`, `diagrams`, `backgrounds`, `effects` and `icons` folders). It was copied in by Claude Code for the original static site and is not the team's own code. The folder remains for provenance, but the current application does not load the kit. `templates/app.html` generates `site/index.html`, `decisions.html`, `decision.html`, `calculator.html`, `sources.html` and `analyse.html`. They share `site/page.css`, `site/app.js` and the generated `site/data.js`.

## Sources and licences

- City of Toronto TMMIS (public meeting agenda item histories); City of Toronto planning project/consultation site; enacted tax by-laws. Source URLs listed in `docs/sources.md` and each claim's linked evidence field.
- Third-party tools: FastAPI, Uvicorn, python-multipart, HTTPX, Streamlit, Pydantic, Anthropic SDK, pypdf, python-dotenv, pytest, Python standard library. See `requirements.txt` and licences for details.
- Do not reuse private attendee correspondence or speaker personal details. `pipeline/clean.py` removes named sections from pasted agenda text **but is not a full PII guarantee** and does not redact uploaded PDF contents.
- The prototype's human review field is **pending**. A claim matching a curated quote is not proof that the whole official document was read in context.
- No API key is committed or enabled in the public demo. Avoid placing resident data or sensitive PDFs into any third-party model.

## Misrepresentation guardrail

Never tell judges that Claude, or any model, is powering the preloaded examples in real time. The four cards were drafted with ChatGPT; Claude wrote the original static website, while the latest application shell and Python API revision were OpenAI Codex-assisted. The examples use curated public records and deterministic verification. The optional model workflow has only been tested with mocked responses. Any teammate who uses additional AI tools must disclose them too.
