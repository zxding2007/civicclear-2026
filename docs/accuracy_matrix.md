# Decision correctness matrix (initial source-linked checks)

This is **not** an independent human accuracy audit. Source text was checked against TMMIS published pages and short demo excerpts; full official staff report PDFs still require team review.

| Item | Official source status | Programmatic output | Stage quote matched curated source text? | Review status |
| --- | --- | --- | --- | --- |
| [DM41.4](https://secure.toronto.ca/council/agenda-item.do?item=2026.DM41.4) | Council received for information, no further action | `received` | Yes | Human pending |
| [PH29.2](https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.2) | Planning and Housing Committee adopted with amendments | `committee_only` | Yes | Human pending |
| [PH29.1](https://secure.toronto.ca/council/agenda-item.do?item=2026.PH29.1) | Committee action then City Council adopted without amendments | `final_adopted` | Yes (3 stages) | Human pending |
| [CC38.1](https://secure.toronto.ca/council/agenda-item.do?item=2026.CC38.1) | City Council adopted with amendments | `final_amended` | Yes | Human pending |

## Numerical check

2025 Toronto residential municipal tax rate incl. City Building Fund is **0.601087%** ([2025.CC27.1, Column VI](https://secure.toronto.ca/council/agenda-item.do?item=2025.CC27.1)). 2026 is **0.614311%** ([2026.CC38.1, Column VI](https://secure.toronto.ca/council/agenda-item.do?item=2026.CC38.1)). At an illustrative unchanged $700,000 assessment:

- 2025: $4,207.61
- 2026: $4,300.18
- Difference: +$92.57

The test suite checks these outputs using decimal half-up rounding. Education tax is excluded. This should never be described as a property owner's actual increase.

## Unit test coverage

`python -m pytest -q` -> **14 passed** on 2026-11-12 (offline container environment). Tests cover status precedence, an unverified Council quote that must not count as adoption, privacy section removal, fabricated quote rejection, four embedded source-backed examples, and tax comparisons. No Streamlit browser launch or paid API test ran in the current environment.
