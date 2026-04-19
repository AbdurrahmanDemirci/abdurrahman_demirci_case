# InsiderOne Senior QA Engineer Assessment

A production-grade test automation framework covering **UI** testing.

> This project was developed collaboratively with [Claude Code](https://claude.ai/code) by Anthropic. The engineering standards, architectural decisions, and code quality applied throughout this framework reflect my professional approach to QA automation. I believe in transparent human–AI collaboration as a force multiplier for engineering excellence.

---

## CI/CD

The pipeline runs on every push and pull request via GitHub Actions (`.github/workflows/tests.yml`).

| Job | Trigger |
|-----|---------|
| UI Tests — Chrome | push / pull_request → main, develop |
| UI Tests — Firefox | push / pull_request → main, develop |

Each browser runs as a separate matrix job. Allure results are uploaded as artifacts on every run.

---

## Architecture

### Five-Layer Design

```
ui_tests/
├── locators/   ← WHAT to find      CSS/XPath only — zero logic
├── pages/      ← HOW to interact   imports locators — zero selectors
├── flows/      ← WHICH sequence    cross-page business flows
├── data/       ← WHAT to expect    assertion constants — zero inline strings
└── tests/      ← WHAT to verify    imports everything above — zero locators
```

A selector change touches exactly **one** locator file. Pages, flows, and test assertions are untouched.

### Key Decisions

| Decision | Rationale |
|----------|-----------|
| Custom `Locator` class | Wraps `(By, value)` tuple with an auto-assigned `.name` for readable logs |
| `flows/` layer | Extracts repeated multi-page sequences (cookie handling, QA job navigation) |
| `data/` layer | Central assertion constants — changing site copy requires a one-line edit |
| `BasePage.open()` | URL navigation + `wait_for_document_ready()` in one call — no partially-loaded DOM |
| `pytest_generate_tests` | Parametrizes `driver` at collection time — one command runs Chrome + Firefox |
| `implicitly_wait(0)` | Prevents implicit/explicit wait interference; all waits are explicit |
| Selenium Manager | Built into Selenium 4.6+ — no third-party driver manager, parallel-safe |
| Allure reporting | Screenshot-on-failure attached inline with test name + browser + timestamp |

---

## Project Structure

```
insiderone2/
│
├── .github/
│   └── workflows/
│       └── tests.yml              # CI: Chrome + Firefox matrix jobs
│
├── utils/
│   └── logger.py                  # Shared structured logger (colorlog)
│
├── ui_tests/
│   ├── conftest.py                # pytest_generate_tests, driver fixture, screenshot hook
│   ├── config.py                  # Env-driven config (BASE_URL, HEADLESS, EXPLICIT_WAIT …)
│   ├── data/
│   │   └── expected_content.py   # Assertion constants (EXPECTED_JOB_DEPARTMENT, …)
│   ├── flows/
│   │   └── site_flow.py          # SiteFlow: handle_cookie_banner, navigate_to_qa_jobs
│   ├── locators/
│   │   ├── locator.py            # Custom Locator class (auto-named tuple)
│   │   ├── home_page_locators.py
│   │   ├── careers_page_locators.py
│   │   └── job_listing_page_locators.py
│   ├── pages/
│   │   ├── base_page.py          # Explicit waits, scroll-into-view, JS fallback click, document-ready
│   │   ├── home_page.py
│   │   ├── careers_page.py
│   │   └── job_listing_page.py
│   ├── tests/
│   │   ├── test_home_page.py
│   │   └── test_insider_careers.py
│   └── utils/
│       └── driver_factory.py     # Chrome/Firefox factory, headless support, Selenium Manager
│
├── .pre-commit-config.yaml       # flake8 + trailing-whitespace + debug-statement checks
├── Makefile                      # Short commands for every run scenario
├── pytest.ini                    # testpaths, addopts (allure, reruns), markers, log config
├── requirements.txt
├── setup.cfg
└── .env.example
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Google Chrome and/or Firefox installed
- `pip` package manager

### Installation

```bash
git clone <repo-url> && cd insiderone2

python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
cp .env.example .env
```

### Optional: Enable pre-commit hooks

```bash
pip install pre-commit
pre-commit install
```

---

## Make Commands

```bash
# UI — single browser
make ui-chrome                 # Chrome
make ui-firefox                # Firefox

# UI — cross-browser (auto-parametrized, single pytest run)
make ui-all                    # Chrome + Firefox sequential
make ui-all-headless           # Chrome + Firefox headless (CI mode)

# UI — parallel execution (pytest-xdist)
make ui-parallel               # Chrome, -n auto workers
make ui-all-parallel           # Chrome + Firefox, -n auto workers

# Reports
make report                    # Generate Allure HTML report
make report-open               # Generate + open in browser

# Cleanup
make clean                     # Delete automation-test-results/
```

> Run `make help` to see the full list at any time.

---

## Cross-Browser Strategy

The `driver` fixture is parametrized at **collection time** via `pytest_generate_tests`:

```python
def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        browser_opt = metafunc.config.getoption("--browser")
        browsers = [browser_opt] if browser_opt else ["chrome", "firefox"]
        metafunc.parametrize("driver", browsers, indirect=True)
```

| Command | Browsers |
|---------|----------|
| `pytest --browser=chrome` | Chrome only |
| `pytest --browser=firefox` | Firefox only |
| `pytest` (no flag) | Chrome **and** Firefox |

In CI, each browser runs as a separate matrix job — failures are isolated per browser.

---

## Flaky Test Handling

All tests retry automatically on failure (configured in `pytest.ini`):

```ini
--reruns=2
--reruns-delay=1
```

A test is marked as failed only if it fails on **all 3 attempts**. Retry count and attempts are visible in the Allure report.

---

## Test Coverage

### UI Automation (InsiderOne Careers)

| File | Test | Markers | What is verified |
|------|------|---------|-----------------|
| `test_home_page.py` | `test_01_home_page_is_opened_and_loaded` | `smoke` `regression` | Homepage URL, title keyword, main blocks visible |
| `test_insider_careers.py` | `test_02_careers_page_is_opened_and_loaded` | `regression` | Careers page URL, department section visible |
| `test_insider_careers.py` | `test_03_qa_jobs_listed` | `smoke` `regression` | QA job board present on Lever |
| `test_insider_careers.py` | `test_04_first_qa_job_details_are_correct` | `regression` | Position, department, location match expected values |

**Technologies**: Python · Selenium 4 · pytest · Selenium Manager · POM

---

## Test Markers

```bash
pytest -m smoke       # test_01, test_03 — fast critical-path check
pytest -m regression  # all 4 tests — full suite
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://insiderone.com` | Homepage URL |
| `BROWSER` | `chrome` | Default browser when `--browser` not set |
| `HEADLESS` | `false` | Run browser in headless mode |
| `EXPLICIT_WAIT` | `30` | Selenium explicit wait timeout (seconds) |

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.10+ |
| UI Automation | Selenium | 4.18.x |
| Driver Management | Selenium Manager (built-in) | — |
| Test Runner | pytest | 8.1.x |
| Parallel Execution | pytest-xdist | 3.5.x |
| Flaky Test Retry | pytest-rerunfailures | 14.0.x |
| Reporting | allure-pytest | 2.13.x |
| Logging | colorlog | 6.8.x |
| CI/CD | GitHub Actions | — |
| Code Quality | flake8 + pre-commit | — |
