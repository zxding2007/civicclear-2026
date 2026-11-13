# Publishing CivicClear — exact remaining steps

Repository owner expected: `zxding2007`. Proposed repository name: `civicclear-2026`.

## 1. GitHub

1. Sign in at https://github.com/ with `zxding2007`.
2. Create a **Public** repository called `civicclear-2026` at https://github.com/new. **Do not** initialize with a README, `.gitignore`, or licence (these files are included here).
3. From the unzipped project folder run:

```bash
git init -b main
git add .
git status --short  # verify .env and .streamlit/secrets.toml are not staged
git commit -m "Build CivicClear council decision explainer MVP"
git remote add origin https://github.com/zxding2007/civicclear-2026.git
git push -u origin main
```

GitHub may ask for browser authentication or a credential manager. Do not type an API key in place of GitHub credentials. If the team has already created a repository, use its existing URL instead of creating a second one.

## 2. Streamlit Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app** → **Deploy a public app from GitHub**.
3. Select repository `zxding2007/civicclear-2026`, branch `main`, entrypoint `app.py`, Python 3.12.
4. Deploy and open the new URL. The four curated demo items do **not** need secrets.
5. Only if enabling the administrator analyser, add `ANTHROPIC_API_KEY`, `CIVICCLEAR_ANALYST_PASSWORD` and verified `CIVICCLEAR_MODEL` via Streamlit's private Secrets panel. Never paste keys into GitHub.

## 3. Real browser smoke test

- [ ] The homepage opens with no Python exception.
- [ ] The sidebar lists exactly four agenda cases: `2026.CC38.1`, `2026.DM41.4`, `2026.PH29.1`, `2026.PH29.2`.
- [ ] `2026.DM41.4`: **Received for information** and not 'adopted'.
- [ ] `2026.PH29.2`: **Committee only** and consultation is not claimed open now.
- [ ] `2026.PH29.1`: the separate Council action appears.
- [ ] `2026.CC38.1`: entering CAD 700,000 shows 2025 CAD 4,207.61; 2026 CAD 4,300.18; difference CAD 92.57.
- [ ] Source evidence expanders link to official `secure.toronto.ca` URLs.
- [ ] `Admin: new item` says analysis is disabled if no secrets are configured.
- [ ] Review on a phone-sized browser width and inspect page readability.
- [ ] Check the GitHub Actions **Python tests** workflow passes.
- [ ] A second human has verified each agenda card against the full official record and staff report before claims of municipal readiness.

## Status at preparation

Local Python tests: 14 passed; syntax compile passed. A complete Streamlit start was **not** possible in the file execution environment because Streamlit was unavailable and external Python package installation was blocked. GitHub repository creation via the web browser was blocked because the browser was not signed in. No public deployment has been verified. Do not portray this checklist as completed until each box is checked on the real website.
