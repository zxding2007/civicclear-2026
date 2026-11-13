# Data, API and code sources

**Data review date:** 2026-11-12 (Toronto time). Links point to original records rather than reproducing complete copyrighted reports.

## Official municipal source pages

- [2026.DM41.4 — Cummer Station, received for information](https://secure.toronto.ca/council/agenda-item.do?item=2026.DM41.4). City Council tracking text includes "No further action"; Ward 18.
- [2026.PH29.2 — Little Jamaica and Oakwood Vaughan](https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.2). Planning and Housing Committee, April 14, 2026; wards 5, 8, 9, 12.
- [2026.PH29.1 — Meanwhile Uses, McCleary District](https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.1). City Council, April 22–23, 2026; Ward 14.
- [2026.CC38.1 — 2026 Budget Implementation](https://secure.toronto.ca/council/agenda-item.do?item=2026.CC38.1). Residential municipal rate including City Building Fund 0.614311%, Column VI.
- [2025.CC27.1 — 2025 Budget Implementation](https://secure.toronto.ca/council/agenda-item.do?item=2025.CC27.1). Residential municipal rate including City Building Fund 0.601087%, Column VI.
- [City of Toronto property tax rates](https://www.toronto.ca/services-payments/property-taxes-utilities/property-tax/property-tax-rates-and-fees/). Lists separate municipal, education and City Building Fund components.
- [Toronto: Have Your Say](https://www.toronto.ca/city-government/council/council-committee-meetings/have-your-say/). Confirm deadlines here and on the item notice; do not infer them.
- [Toronto open data licence](https://open.toronto.ca/open-data-licence/). Confirm applicable conditions/attribution before deployment.

## Hackathon

- [CIVIC Hack 2026 official schedule](https://fciprojects.ca/hackathons/2026-civic-hack/).
- [Devpost rules](https://civic-hack-2026.devpost.com/rules).
- [Devpost event submission description](https://civic-hack-2026.devpost.com/).

## Developer APIs and libraries

- [Anthropic model list](https://platform.claude.com/docs/en/models/overview): `claude-opus-5-5`, list pricing $4/input million tokens, $20/output million tokens as reviewed 2026-11-12. Actual consumption, billing and product availability can change.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): `client.messages.parse`, Pydantic models.
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations): PDF/text source citations; mutually incompatible with a single strict JSON output request.
- [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support): request and PDF limitations.
- [Streamlit documentation](https://docs.streamlit.io/); [Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud).
- [Pydantic](https://docs.pydantic.dev/); [pypdf](https://pypdf.readthedocs.io/); [pytest](https://docs.pytest.org/); [python-dotenv](https://github.com/theskumar/python-dotenv).

Versions are deliberately version-ranged in `requirements.txt` for Python 3.12. Obtain installed package versions with `pip freeze` for a release lock file and review each licence before redistributing dependencies.
