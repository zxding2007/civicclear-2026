# AI assistance, provenance and testing disclosure (updated Nov 13, 2026)

This disclosure accompanies the source code and hackathon submission. It explicitly separates **curated examples**, **mocked API contract tests**, and **real external AI calls**.

| Workstream | AI role | What was actually tested |
| --- | --- | --- |
| CivicClear source and app | OpenAI ChatGPT (GPT-6) helped author/refine Streamlit, Python source/fixtures, source metadata, Impact Analysis UI and docs | Python unit tests, syntax checks, GitHub Actions, Render live site. Manual review of AI-written code is still advisable. |
| Four public demo cards | ChatGPT drafted concise cards after inspecting official City records | Source-linked curated extracts and independent AI source cross-check. **Not** Claude-generated production API output. No claim of a signed municipal audit. |
| Claude API interface | Optional Anthropic Python SDK client for two-stage structured extraction + cited narrative | Code path and fake-client tests only if present. **No real Claude requests or API charges have been performed** without ANTHROPIC_API_KEY. Do not describe this as live-tested. |
| Stakeholder considerations | ChatGPT authored candidate resident/business/community issues from City planning descriptions | Two Toronto agenda cases with direct primary-source links. Possible effects are not measured outcomes or endorsed policy positions. |
| Documentation / report | ChatGPT generated drafts and presentation narration | Human/team confirmation and final video recording remain the submitter's responsibility. |
| Static website (`site/`), `build_site.py`, `tests/test_site.py`, `.github/workflows/pages.yml` | Anthropic Claude (Claude Code, Claude Opus 5.5) wrote the page, the build script, its tests and the publishing workflow; see the `Co-Authored-By` lines on commits `f54e108` and `0ea892f` | Python tests (30 passing), the build's status-mismatch stop, GitHub Actions publish, manual look at desktop and phone widths. |
| Review and corrections on Nov 13 | Anthropic Claude (Claude Code, Claude Fable 5.2) reviewed the repository against the challenge brief and edited the website wording, `README.md`, this file and `docs/sources.md` | Tests and site build rerun after the edits. |

## Third-party design code

`site/assets/` is the **taste-skill** frontend kit (`system.css`, `system.js`, and the `ui`, `layout`, `motion`, `moments`, `diagrams`, `backgrounds`, `effects` and `icons` folders). It was copied in by Claude Code when the static site was built and is not the team's own code. The page loads only part of it; the rest is unused. The team's own site files are `site/index.html`, `site/page.css`, `site/app.js` and the generated `site/data.js`.

## Sources and licences

- City of Toronto TMMIS (public meeting agenda item histories); City of Toronto planning project/consultation site; enacted tax by-laws. Source URLs listed in `docs/sources.md` and each claim's linked evidence field.
- Third-party tools: Streamlit, Pydantic, Anthropic SDK, pypdf, python-dotenv, pytest, Python standard library. See `requirements.txt` and licences for details.
- Do not reuse private attendee correspondence or speaker personal details. `pipeline/clean.py` removes named sections from pasted agenda text **but is not a full PII guarantee** and does not redact uploaded PDF contents.
- The prototype's human review field is **pending**. A claim matching a curated quote is not proof that the whole official document was read in context.
- No API key is committed or enabled in the public demo. Avoid placing resident data or sensitive PDFs into any third-party model.

## Misrepresentation guardrail

Never tell judges that Claude, or any model, is powering the preloaded examples in real time. The four cards were drafted with ChatGPT; Claude wrote the static website's code, not the card content. The actual live demo uses curated public records, deterministic verification and an optional untested API workflow. Any teammate who uses additional AI tools must disclose them too.
