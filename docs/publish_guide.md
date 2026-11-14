# Publishing CivicClear

**Preparation status: November 13, 2026.** The repository already exists at [zxding2007/civicclear-2026](https://github.com/zxding2007/civicclear-2026). The latest six-page interface, Python API and documentation revision are being prepared as a local review-branch commit. They have **not yet been pushed or deployed** by this preparation work.

The existing public addresses are the [GitHub Pages snapshot](https://zxding2007.github.io/civicclear-2026/) and the [earlier Streamlit service on Render](https://civicclear-2026.onrender.com/). An existing address does not establish that it serves the latest local revision.

## Build and review locally

Use Python 3.12 explicitly and Node.js 22 for the JavaScript syntax check (no npm install is needed):

```bash
# macOS/Linux
python3.12 -m venv .venv
source .venv/bin/activate
# Windows PowerShell alternatives:
# py -3.12 -m venv .venv
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python -m compileall -q app.py server.py pipeline calculator.py build_cache.py build_site.py
node --check site/app.js
python build_site.py
python -m uvicorn server:app --reload
```

Open `http://localhost:8000`. The six documents are `index.html`, `decisions.html`, `decision.html?id=...`, `calculator.html`, `sources.html` and `analyse.html`. Navigation follows ordinary links and loads a new HTML document. Edit shared HTML in `templates/app.html`; `build_site.py` verifies the data, writes `site/data.js`, then generates all six pages. Commit the source template and generated pages together.

The connected application serves the website and `/api/bootstrap`, `/api/tax`, `/api/analyse` and `/api/health` from one origin. The four saved decisions and tax calculator require no credentials.

## Push the reviewed branch

Keep the existing `origin`; do not initialize another repository or create a duplicate GitHub project. Before a push, inspect the prepared commit and confirm that secrets, local environments and unrelated files are excluded:

```bash
git status --short
git log -1 --oneline
git show --stat HEAD
```

After the reviewed local commit is approved for publication, push its current branch:

```bash
git push -u origin HEAD
```

Open a pull request to `main` and inspect the **Application checks** result. A review-branch push does not trigger the Pages workflow; merging to `main` does. These commands are instructions for the subsequent publication step, not a record that a push or merge has occurred.

## GitHub Pages: static snapshot

`.github/workflows/pages.yml` runs on pushes to `main` and manual workflow dispatch. It installs the Python dependencies, runs the tests and JavaScript syntax check, executes `python build_site.py` and publishes the `site/` folder. The build rejects a computed decision status that differs from its stored or golden expectation.

In the repository's Pages settings, use **GitHub Actions** as the publication source. After the workflow succeeds, check the published address and its separate page links. The static version loads the saved data bundle and calculates tax in the browser. It does not run Python, hold API credentials or analyse new records.

## Render: connected application

`render.yaml` describes a Python web service with these settings:

| Setting | Value |
| --- | --- |
| Python | 3.12, also recorded in `.python-version` |
| Build command | `pip install -r requirements.txt && python build_site.py` |
| Start command | `uvicorn server:app --host 0.0.0.0 --port $PORT` |
| HTTP health-check path | `/api/health` |

The committed generated pages are served directly. Run and commit `python build_site.py` output before deploying template or data changes. To move the existing Render service from Streamlit to this application, explicitly update its start command and health-check setting, or create a separate service from the configuration. A GitHub Pages publication does not perform this migration. Review the Render service's branch and automatic deployment settings before publishing a branch it tracks.

Only enable analysis when wanted: configure `ANTHROPIC_API_KEY`, `CIVICCLEAR_ANALYST_PASSWORD` and a verified supported `CIVICCLEAR_MODEL` in the host environment. Locally, `server.py` loads these from uncommitted `.env`. No paid API call has been tested, and **no new Render deployment has been performed** during this preparation.

## Retaining the legacy Streamlit interface

`streamlit run app.py` remains available separately. For [Streamlit Community Cloud](https://share.streamlit.io/), use this repository, `app.py` and Python 3.12. Its optional analyst settings use environment variables or Streamlit Secrets. Streamlit does not serve the new HTML pages or `/api/` endpoints.

## Validation and publication checks

The latest local suite passed **57 Python tests**, including 27 API tests with mocked AI responses. Local browser checks covered desktop and **375-pixel mobile** layouts, normal page navigation, keyboard interaction and invalid calculator inputs. These checks do not establish formal accessibility conformance or paid model availability.

After an actual deployment, verify the new destination separately:

- All six document URLs open, including a direct decision URL and browser back/forward navigation.
- The four agenda examples retain their distinct statuses: DM41.4 received; PH29.2 committee only; PH29.1 Council adopted; CC38.1 Council adopted with amendments.
- PH29.2 identifies the separate cited feedback window through November 30, 2026, and stops advertising that window as open after its stated end date. The City portal must still be checked for current availability.
- CAD 700,000 produces CAD 4,207.61 for 2025, CAD 4,300.18 for 2026 and a CAD 92.57 difference. The direct [2025](https://www.toronto.ca/legdocs/bylaws/2025/law0105.pdf#page=6) and [2026 levy bylaws](https://www.toronto.ca/legdocs/bylaws/2026/law0133.pdf#page=6) support the municipal rates on page 6, Column 5; education tax is excluded.
- The connected app reports `Python connected`, and `/api/health` returns `{"status":"ok"}`. Pages reports `Saved demo`, and new-record analysis is unavailable there.
- Source links, keyboard controls, mobile navigation and invalid-input feedback work at the deployed address.

Independent human sign-off on the four curated records remains **pending**. Automated quotation matches and passing UI tests are not a completed municipal review. See [`live_ai_smoke_test.md`](live_ai_smoke_test.md) for the separate, still-unexecuted paid AI check.
