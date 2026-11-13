# AI assistance, provenance and testing disclosure (Nov 12, 2026)

This disclosure accompanies the source code and hackathon submission. It explicitly separates **curated examples**, **mocked API contract tests**, and **real external AI calls**.

| Workstream | AI role | What was actually tested |
| --- | --- | --- |
| CivicClear source and app | OpenAI ChatGPT (GPT-6) helped author/refine Streamlit, Python source/fixtures, source metadata, Impact Analysis UI and docs | Python unit tests, syntax checks, GitHub Actions, Render live site. Manual review of AI-written code is still advisable. |
| Four public demo cards | ChatGPT drafted concise cards after inspecting official City records | Source-linked curated extracts and independent AI source cross-check. **Not** Claude-generated production API output. No claim of a signed municipal audit. |
| Claude API interface | Optional Anthropic Python SDK client for two-stage structured extraction + cited narrative | Code path and fake-client tests only if present. **No real Claude requests or API charges have been performed** without ANTHROPIC_API_KEY. Do not describe this as live-tested. |
| Stakeholder considerations | ChatGPT authored candidate resident/business/community issues from City planning descriptions | Two Toronto agenda cases with direct primary-source links. Possible effects are not measured outcomes or endorsed policy positions. |
| Documentation / report | ChatGPT generated drafts and presentation narration | Human/team confirmation and final video recording remain the submitter's responsibility. |

## Sources and licences

- City of Toronto TMMIS (public meeting agenda item histories); City of Toronto planning project/consultation site; enacted tax by-laws. Source URLs listed in `docs/sources.md` and each claim's linked evidence field.
- Third-party tools: Streamlit, Pydantic, Anthropic SDK, pypdf, python-dotenv, pytest, Python standard library. See `requirements.txt` and licences for details.
- Do not reuse private attendee correspondence or speaker personal details. `pipeline/clean.py` removes named sections from pasted agenda text **but is not a full PII guarantee** and does not redact uploaded PDF contents.
- The prototype's human review field is **pending**. A claim matching a curated quote is not proof that the whole official document was read in context.
- No API key is committed or enabled in the public demo. Avoid placing resident data or sensitive PDFs into any third-party model.

## Misrepresentation guardrail

Never tell judges that Claude is powering the preloaded examples in real time. The actual live demo uses curated public records, deterministic verification and an optional untested API workflow. Any teammate who uses additional AI tools must disclose them too.
