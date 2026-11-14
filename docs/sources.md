# Data, API and code sources

**Data review date:** 2026-11-12 (Toronto time). Links point to original records rather than reproducing complete copyrighted reports.

## Official municipal source pages

- [2026.DM41.4 — Cummer Station, received for information](https://secure.toronto.ca/council/agenda-item.do?item=2026.DM41.4). City Council tracking text includes "No further action"; Ward 18.
- [2026.PH29.2 — Little Jamaica and Oakwood Vaughan](https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.2). Planning and Housing Committee, April 14, 2026; wards 5, 8, 9, 12.
- [2026.PH29.1 — Meanwhile Uses, McCleary District](https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.1). City Council, April 22–23, 2026; Ward 14.
- [2026.CC38.1 — 2026 Budget Implementation](https://secure.toronto.ca/council/agenda-item.do?item=2026.CC38.1). Residential municipal rate including City Building Fund 0.614311%, Column VI.
- [2025.CC27.1 — 2025 Budget Implementation](https://secure.toronto.ca/council/agenda-item.do?item=2025.CC27.1). Residential municipal rate including City Building Fund 0.601087%, Column VI.
- [City of Toronto property tax rates](https://www.toronto.ca/services-payments/property-taxes-utilities/property-tax/property-tax-rates-and-fees/). Lists separate municipal, education and City Building Fund components.
- [Little Jamaica/Oakwood Vaughan project updates](https://www.toronto.ca/city-government/planning-development/planning-studies-initiatives/little-jamaica-oakwood-vaughan-planning-framework/). City project page, checked 2026-11-12, announces Q1 2027 final report and Nov 30, 2026 mapping deadline; separate from the April agenda record.
- [Official Little Jamaica/Oakwood Vaughan interactive feedback map](https://haveyoursay.toronto.ca/LJOV-Planning-Framework-CHRA). Portal states April 24–November 30, 2026 feedback window; does not establish any other active meeting registration.
- [2025 Tax Levy By-law 105-2025](https://www.toronto.ca/legdocs/bylaws/2025/law0105.pdf). Municipal residential end rate, Column 5: 0.601087%.
- [2026 Tax Levy By-law 133-2026](https://www.toronto.ca/legdocs/bylaws/2026/law0133.pdf). Municipal residential end rate, Column 5: 0.614311%.
- [Toronto: Have Your Say](https://www.toronto.ca/city-government/council/council-committee-meetings/have-your-say/). Confirm deadlines here and on the item notice; do not infer them.
- [Toronto open data licence](https://open.toronto.ca/open-data-licence/). Confirm applicable conditions/attribution before deployment.

## Hackathon

- [CIVIC Hack 2026 official schedule](https://fciprojects.ca/hackathons/2026-civic-hack/).
- [Devpost rules](https://civic-hack-2026.devpost.com/rules).
- [Devpost event submission description](https://civic-hack-2026.devpost.com/).

## Developer APIs and libraries

- [DeepSeek API quickstart](https://api-docs.deepseek.com/): `deepseek-flash` is the default used by this integration, with the selected key held only in the Python environment. Verify current account access before a live test.
- [DeepSeek JSON output](https://api-docs.deepseek.com/guides/json_mode/): used for separate decision-card and explanation responses. CivicClear validates the card and checks model-provided quotation references locally; it does not claim equivalence to Anthropic's native citation feature. PDF text is extracted locally, and PDFs without readable text are rejected by this integration.
- [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/), [HTTPX](https://www.python-httpx.org/) and [python-multipart](https://multipart.fastapiexpert.com/): connected app, HTTP requests and uploads.

- [Anthropic model list](https://platform.claude.com/docs/en/models/overview): `claude-opus-5-5`, list pricing $4/input million tokens, $20/output million tokens as reviewed 2026-11-12. Actual consumption, billing and product availability can change.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): `client.messages.parse`, Pydantic models.
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations): PDF/text source citations; mutually incompatible with a single strict JSON output request.
- [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support): request and PDF limitations.
- [Streamlit documentation](https://docs.streamlit.io/); [Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud).
- [Pydantic](https://docs.pydantic.dev/); [pypdf](https://pypdf.readthedocs.io/); [pytest](https://docs.pytest.org/); [python-dotenv](https://github.com/theskumar/python-dotenv).

## Website design kit and AI coding tools

- **taste-skill** frontend kit, bundled under `site/assets/` (CSS system, layout, motion, diagram and icon files). Third-party code used by the original landing page. The folder is retained, but none of the current six application pages loads it.
- **Claude Code** (Anthropic) built the original static website and its build script; **ChatGPT** (OpenAI) drafted the Python app, the four cards and the documents. **OpenAI Codex** assisted with the latest multi-page application, FastAPI server, API tests, calculator and accessibility corrections, and related documentation. The earlier multi-page revision had 57 passing Python tests and targeted browser checks of navigation, filters, calculations, invalid input, mobile/keyboard use, and the saved-data fallback. Those results do not establish a deployment or full accessibility audit. The subsequent provider-support revision uses mocked tests; neither Claude nor DeepSeek has received a real paid inference request in this work. Details in [`ai_usage.md`](ai_usage.md).

Versions are deliberately version-ranged in `requirements.txt` for Python 3.12. Obtain installed package versions with `pip freeze` for a release lock file and review each licence before redistributing dependencies.
