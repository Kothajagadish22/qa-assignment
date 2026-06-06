# QA Automation Assignment (Python)

Test automation for an e-commerce **UI** (SauceDemo) and an e-commerce-shaped **API** (FakeStoreAPI),
built with **Python + pytest** and wired to **GitHub Actions** (runs on every push).

| Assignment | Target | Folder | Stack |
|-----------|--------|--------|-------|
| 1 | https://www.saucedemo.com/ | [`assignment1-ui/`](assignment1-ui/) | pytest + Playwright (Python) |
| 2 | https://fakestoreapi.com/ | [`assignment2-api/`](assignment2-api/) | pytest + requests + jsonschema |

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python -m playwright install chromium

pytest                          # run both suites (creates report.html)
pytest assignment1-ui           # Assignment 1 only (SauceDemo UI)
pytest assignment2-api          # Assignment 2 only (FakeStoreAPI)
pytest assignment1-ui --headed  # SEE the browser open (SauceDemo)
pytest -m "positive"            # filter by marker
pytest -n auto                  # run in parallel (pytest-xdist)

# Windows shortcuts (double-click in Explorer):
#   run_all_tests.bat   -> runs all tests + opens report.html in browser
#   run_ui_headed.bat   -> runs UI tests with Chrome visible
```

### Why you might not "see" anything

| What you ran | What happens |
|--------------|--------------|
| `pytest` (default) | Tests pass in terminal; browser runs **in background** (headless) — no window |
| `pytest assignment2-api` | **No browser at all** — API tests use HTTP only (FakeStoreAPI) |
| `pytest assignment1-ui --headed` | **Chrome window opens** — you watch login, cart, checkout |
| After `pytest` | Open `report.html` in this folder for a visual test report |

## Why pytest

- **One runner for both layers** — Playwright's pytest plugin drives the browser tests, and
  `requests` drives pure HTTP/API tests, all under a single `pytest` command, with one report.
- **Parametrisation built in** — `@pytest.mark.parametrize` powers the data-driven test cleanly.
- **Parallelism + reporting** — `pytest-xdist` (`-n auto`) for parallel runs and `pytest-html` for a
  shareable report; Playwright adds trace/screenshot/video on failure.
- **Readable, low-boilerplate** — fixtures (`api`, `login_page`, `logged_in_inventory`) keep tests short.

## Repo layout

```
.
├── assignment1-ui/         # SauceDemo: automation + manual test cases (Excel/CSV)
│   └── test-cases/         # SauceDemo_Manual_TestCases.xlsx  ← Assignment 1 manual sheet
├── assignment2-api/        # FakeStoreAPI: CRUD, auth, schema, data-driven, contract tests
├── .github/workflows/ci.yml
├── pytest.ini              # markers + testpaths
└── requirements.txt
```

Each assignment has its own 1-page README with framework rationale and an extension plan.

## CI

`.github/workflows/ci.yml` installs deps + the Chromium browser and runs `pytest -n auto` on every
push / PR, uploading the HTML report as a build artifact.
