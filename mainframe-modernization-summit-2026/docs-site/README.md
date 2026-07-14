# Mainframe Modernization Summit Handbook 2026 — docs-site

MkDocs Material site for the **Mainframe Modernization Summit 2026 — Specialist Workshop (Brazil)**.

This site is a *living document*: it is meant to be edited and re-deployed during the workshop as new errors surface.

## Run locally

Requires Python 3.11+.

```bash
cd docs-site
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000>.

## Add a troubleshooting entry

1. Pick the right page under [docs/troubleshooting/](docs/troubleshooting/).
2. Append a new section using **this exact format** so search hits the literal error string:

   ```markdown
   ## `<exact error string as it appears in the terminal>`

   **Cause:** one to two sentences.

   **Fix:**
   1. Step one
   2. Step two
   3. Step three

   **Still broken?** Escape hatch — what to try next or who to contact.
   ```

3. Add a one-liner to [docs/changelog.md](docs/changelog.md) at the top.
4. Commit + push to `main`. The GitHub Action will rebuild and redeploy.

## Deploy

Pushes to `main` that touch `docs-site/**` trigger [.github/workflows/deploy-docs.yml](../.github/workflows/deploy-docs.yml):

1. Builds with `mkdocs build --strict`.
2. Uploads the built site as a Pages artifact and deploys via `actions/deploy-pages@v4` (GitHub-native, no `gh-pages` branch).

## Enable GitHub Pages (one-time, before the first deploy)

1. In the repo on GitHub: **Settings → Pages**.
2. **Source:** *GitHub Actions*. Save.
3. Trigger the first deploy: push a change to `docs-site/**` on `main`, or run the workflow manually from the **Actions** tab (*Deploy docs* → **Run workflow**).
4. The published URL appears at the top of **Settings → Pages** once the run finishes (≈ 1–2 min).
5. Optional: configure a **Custom domain** and enable **Enforce HTTPS**.

## Identity

- Working name: **Mainframe Modernization Summit Handbook 2026**
- Palette: bg `#0E1116`, terminal green `#00E37F`, Kyndryl red `#FF462D`
- Type: JetBrains Mono (headings/code) + Inter (body)
- Nav prefixes: `$ setup`, `! troubleshoot`, `# story`, `? reference`

All custom styling lives in [docs/stylesheets/extra.css](docs/stylesheets/extra.css).
The hero typed-text effect uses [typed.js](https://github.com/mattboldt/typed.js/) loaded via CDN from [docs/overrides/main.html](docs/overrides/main.html).
