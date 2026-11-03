# Zhivko Petkov — personal portfolio

A cybersecurity student's portfolio with an original terminal-inspired interface. Internal design codename: **GHOST//SHELL**. Built with Flask, Jinja, CSS, and vanilla JavaScript; no frontend build step, remote fonts, analytics, or database.

## Current checkpoint

The local visual foundation and basic Flask functionality are implemented. Approved identity: Zhivko Petkov, cybersecurity student, [@nvm0r](https://github.com/nvm0r), zhivkop3@gmail.com.

- Responsive hero with original ASCII ghost, about, project toolkit, project dossiers, learning log, status, and contact.
- Each page load selects a different subject: ghost, robot, skull, cat, satellite, moth, or portal. A shuffled deck visits all seven before repeating and prevents consecutive repeats. Only artwork IDs are saved locally in the browser. If browser storage is disabled, selection works but cannot remember earlier visits. The ghost also varies procedurally. No AI API or external service is required.
- Mobile navigation, keyboard focus, skip link, reduced-motion CSS, native expandable project details.
- Real `/health` and `/api/version` responses; the monitor clears stale data and shows UNAVAILABLE on failed requests.
- CV is explicitly unavailable until a reviewed public PDF is supplied.
- Skills are labeled as this project's stack or roadmap. Innovatech details, education dates, and further experience remain unconfirmed.

**Local Docker build/run is verified.** The Portfolio CI workflow runs tests on main pushes and pull requests, then builds a SHA-tagged Docker image only after tests pass. It does not push to a registry. Repository: https://github.com/nvm0r/PortfolioWebsite. ECR and cloud deployment remain later milestones; no cloud resources have been provisioned.

## Run with Docker (PowerShell)

`Dockerfile` uses Python 3.12.14 slim, Gunicorn, two workers, a non-root user, and an application health check. `requirements-docker.txt` adds the Linux server dependency separately from the Windows development requirements.

```powershell
docker build -t ghost-shell-portfolio:v1 .
docker images
docker run -d --name ghost-shell -p 8081:8080 -e APP_VERSION=v1.0.0 -e APP_ENV=local-docker -e APP_PLATFORM=Docker ghost-shell-portfolio:v1
docker ps
docker logs ghost-shell
Invoke-RestMethod http://localhost:8081/health
Invoke-RestMethod http://localhost:8081/api/version
```

Open http://localhost:8081. Host port 8080 was already occupied during verification, so this container uses host port 8081 and container port 8080. The container is left running. Stop/start it with `docker stop ghost-shell` / `docker start ghost-shell`. To replace it after source changes, rebuild the image, stop the old container, run `docker rm ghost-shell`, then repeat the run command. No source files are mounted, so changes require rebuilding.

## Run on this workspace (PowerShell)

The `.venv` created during implementation is ready to use. From this folder:

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
```

Open **http://localhost:5000**. Stop with **Ctrl+C**. The development server is for local use.

Port 8080 returned a Windows socket permission error during implementation; 5000 was verified. If your terminal reports that a port is already in use, stop the existing preview first or select another available port.

## Set up on a fresh machine

Install Python 3.11+ from the official Python distribution, then run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
```

Use the version installed on your machine (for example `py -3.12`). No PowerShell activation or execution-policy change is necessary.

On the implementation machine, `py` selected Python 3.9 and the registered Store Python 3.11 could not launch. The app was instead tested with the bundled Python **3.12.14**. Its reduced runtime lacked `ensurepip`, so pip from the parent runtime installed packages into `.venv` using `pip --python`. This is a machine-specific setup detail, not an application requirement. If this environment is moved or its parent runtime is removed, recreate `.venv` with your regular Python installation.

## Validate

```powershell
.\.venv\Scripts\python.exe -m pytest -v --basetemp=.pytest_cache/tmp
node --check app/static/js/main.js
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod http://localhost:5000/api/version
```

Node is optional and used only for the JavaScript syntax check. The pytest temporary directory stays within the workspace because the automation sandbox's default temporary directory was not writable.

Expected: **13 tests pass**; health is `{"status":"healthy"}`; metadata defaults to `v0.1.0-dev`, `local`, `uncommitted`, and `Local Python / Flask`.

Tests cover owner identity and sections, health, metadata configuration/defaults, CV absent/present behavior, static assets, security headers, and missing routes. The PDF fixture is a synthetic test file in a temporary directory, not a public CV.

## Configuration and editing

| File | Purpose |
| --- | --- |
| `app/content.py` | Approved identity, contact links, project toolkit |
| `app/ascii_art.py` | Procedural ghost generator (35 columns × 20 rows) |
| `app/templates/index.html` | Page sections, copy, project descriptions, original ASCII artwork |
| `app/static/css/style.css` | Color tokens, typography, layout, responsive and reduced-motion rules |
| `app/static/js/main.js` | Mobile menu, current section, live status requests |
| `app/__init__.py` | Flask factory, endpoints, metadata, security headers |
| `tests/test_app.py` | Backend and static resource checks |
| `requirements.txt`, `requirements-dev.txt` | Pinned direct dependencies |
| `.env.example` | Available non-secret settings (not loaded automatically) |
| `docs/architecture.md` | Local request flow and intended next stages |
| `docs/evidence/` | Actual captured screenshots and verification notes |

Set metadata before starting the server, for example:

```powershell
$env:APP_VERSION = 'v0.2.0-dev'
$env:APP_ENV = 'local'
$env:GIT_SHA = 'uncommitted'
$env:APP_PLATFORM = 'Local Python / Flask'
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
```

`APP_VERSION` is the single version source for the page and API. A future CI build should inject the actual full Git SHA and verified runtime labels. A successful health request verifies this application endpoint only; it does not measure uptime or prove the cloud infrastructure or CI pipeline is healthy.

For a CV, review the intended public PDF for private information, create `app/static/docs/`, and place the authorized file at `app/static/docs/cv.pdf`. Both download links then appear automatically on the next page request. Restart Flask after Python/template changes; refresh after CSS/JS edits.

## Review and evidence checklist

1. Review identity and copy; confirm any additional biography before publishing.
2. Open desktop, tablet (768px), and mobile (375px) views; inspect all sections.
3. Tab through links and controls. Check visible focus, Enter on the project dossier, and Escape to close the mobile menu.
4. Enable your OS/browser reduced-motion preference and confirm blinking/boot animation and smooth scrolling stop.
5. Refresh the system monitor; verify local metadata. Stop the server, refresh the monitor without reloading the page, and confirm UNAVAILABLE. Restart and refresh to recover.
6. Capture screenshots and test results. Never substitute mocked infrastructure results for real deployment evidence.

## Next milestones

1. Review the visual foundation and fill confirmed content.
2. Add a lean non-root Docker image using Gunicorn; build and verify locally.
3. Select/create the intended GitHub repository and add automatic PR/main tests and Docker build validation.
4. Check current AWS service eligibility, region, pricing, and IAM requirements; obtain approval before billed resource provisioning.
5. Configure repository-scoped GitHub OIDC, ECR, and the approved container host. Publish immutable SHA tags, explicitly select the new image, wait for rollout, and verify live health/version.
6. Capture successful and intentionally failing CI evidence on a controlled branch. Demonstrate that failed tests prevent publish/deploy.

The remaining cloud milestones require real account/repository configuration and cannot be represented as completed local work. See the [Flask installation documentation](https://flask.palletsprojects.com/en/stable/installation/) for upstream environment guidance.
