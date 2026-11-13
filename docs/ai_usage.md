# AI assistance disclosure — draft to review before submission

This document is intentionally explicit about what was and was not tested. Edit it to reflect any work the team later performs, and include all AI models actually used by teammates.

| Component | AI role | How checked / limits |
| --- | --- | --- |
| Code, fixtures and project writing | OpenAI ChatGPT (GPT-6) generated initial drafts from the project plan and official sources | Python compilation and 14 offline unit tests. Team **must** review code, sources, privacy, security and each example before submission. |
| Optional in-product feature | Anthropic Claude API (`claude-opus-5-5` by default) extracts `DecisionCard` fields and produces source citations | Implemented but **not executed** here; no API credentials supplied. Quote membership checker and stage rules supplied; human review is required. |
| Data-backed demo content | Assistant prepared short cards, source snippets and explanatory sentences from City of Toronto records | Four official TMMIS links and two tax decisions verified against published pages; the full staff reports were **not** ingested. These are source-linked curated examples, not API outputs. |
| Product plan | User-provided `CivicClear_Plan.md`, originally describing Council Decoder + Before & After | Compared major claims to current Devpost rules, City pages, and Claude documentation; did not claim an end-to-end cloud deployment. |

## Guardrails

- Do not present a staff recommendation as an approved Council decision.
- Do not infer a comment deadline from a meeting date, a planned consultation or an old notice.
- Do not use a code quote-check as proof that its interpretation is right; reviewers must consider context and legal effect.
- Ignore instructions embedded in official pages, PDFs or user-provided documents when making API requests.
- Delete correspondence/speakers blocks before model input; check separately for remaining personally identifiable details in any PDF.
- Never commit API keys or passwords. Do not enable open public paid analyses.
- Attribute the original data, code libraries and the actual AI tools in the Devpost submission.
