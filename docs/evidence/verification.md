# Verification — 2026-11-02

- Python 3.12.14, Flask 3.1.3, pytest 8.4.2.
- `python -m pytest -v --basetemp=.pytest_cache/tmp`: **11 passed**.
- `node --check app/static/js/main.js`: passed.
- Real HTTP GET `/`: 200. `/health`: healthy. `/api/version`: local runtime metadata.
- Browser: live HEALTHY status, local environment, uncommitted build, v0.1.0-dev.
- Desktop screenshot: `desktop.png` (full page).
- Desktop hero: `desktop-hero.png` (1280px viewport); no horizontal page overflow.
- Mobile screenshot: `mobile.png` (375px viewport, hero).
- No page horizontal overflow at 375px and 768px.
- Mobile menu opens, closes after navigation; project dossier expands; refresh retrieves live status.
- Browser console: no warnings/errors observed on successful load.
- Stopped the actual Flask server, activated refresh by keyboard: UNAVAILABLE with cleared metadata. Restarted the server and refreshed: HEALTHY recovered.

Reduced-motion behavior is implemented in CSS; OS preference switching is left for manual review. Cloud, Docker, and GitHub Actions evidence does not exist at this milestone.
