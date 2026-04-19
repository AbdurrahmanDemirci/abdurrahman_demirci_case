# InsiderOne Senior QA Engineer Assessment

[![Test Suite](https://github.com/AbdurrahmanDemirci/abdurrahman_demirci_case/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/AbdurrahmanDemirci/abdurrahman_demirci_case/actions/workflows/tests.yml)

A production-grade test automation framework covering **UI** and **Load** testing.

> This project was developed collaboratively with [Claude Code](https://claude.ai/code) by Anthropic. The engineering standards, architectural decisions, and code quality applied throughout this framework reflect my professional approach to QA automation. I believe in transparent human–AI collaboration as a force multiplier for engineering excellence.

---

## CI/CD

The pipeline runs on every push and pull request via GitHub Actions (`.github/workflows/tests.yml`).

| Job | Trigger |
|-----|---------|
| UI Tests — Chrome | push / pull_request → master, main, develop |
| UI Tests — Firefox | push / pull_request → master, main, develop |
| Load Tests | push / pull_request → master, main, develop |

Each browser runs as a separate matrix job. Allure and Locust results are uploaded as artifacts on every run.

---

## Architecture

### Five-Layer UI Design

```
ui_tests/
├── locators/   ← WHAT to find      CSS/XPath only — zero logic
├── pages/      ← HOW to interact   imports locators — zero selectors
├── flows/      ← WHICH sequence    cross-page business flows
├── data/       ← WHAT to expect    assertion constants — zero inline strings
└── tests/      ← WHAT to verify    imports everything above — zero locators
```

A selector change touches exactly **one** locator file. Pages, flows, and test assertions are untouched.

### Load Modular Locust Design

```
load_tests/
├── locustfile.py   ← thin entry point — no scenario logic
├── config.py       ← env-driven: base URL, thresholds, think time
├── data/           ← all test data and assertion constants
├── utils/          ← centralized response validation + logger
└── scenarios/      ← one file per user type, plugged in via __init__.py
```

Adding a new load scenario = one new file + one import line. Nothing else changes.

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
| Self-contained `load_tests/utils/` | Avoids sys.path collision when Locust adds its locustfile dir to the front of sys.path |

---

## Project Structure

```
insiderone2/
│
├── .github/
│   └── workflows/
│       └── tests.yml              # CI: Chrome + Firefox matrix + Load Tests
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
│       ├── driver_factory.py     # Chrome/Firefox factory, headless support, Selenium Manager
│       └── logger.py             # Structured logger (colorlog); pytest-aware, no duplicate handlers
│
├── load_tests/
│   ├── locustfile.py             # Thin entry point — imports all scenario users
│   ├── config.py                 # Env-driven: BASE_URL, CATEGORY_SLUGS, thresholds
│   ├── data/
│   │   └── search_data.py        # Query lists + assertion constants (NO_RESULTS_TEXT)
│   ├── utils/
│   │   ├── logger.py             # Self-contained logger (no project-root dependency)
│   │   └── response_validator.py # Centralized HTTP validation + P95 threshold checks
│   └── scenarios/
│       ├── __init__.py           # Registers all HttpUser classes
│       ├── category_search.py    # Scenario A: homepage → category page   [smoke]
│       ├── product_search.py     # Scenario B: keyword search → /arama    [smoke+regression]
│       └── user_journey.py       # Scenario C: sequential homepage→search journey
│
├── locust.conf                   # Default CLI params (users=1, run-time=60s, locustfile=…)
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
git clone https://github.com/AbdurrahmanDemirci/abdurrahman_demirci_case.git && cd abdurrahman_demirci_case

python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
cp .env.example .env
```

### Optional: Enable pre-commit hooks

```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Troubleshooting

| Hata | Çözüm |
|------|-------|
| `allure: command not found` | `brew install allure` (macOS) veya [Allure docs](https://allurereport.org/docs/) |
| `ModuleNotFoundError: load_tests` | Proje kökünden çalıştır (`setup.cfg pythonpath = .` ile çözülmüş) |
| Chrome/Firefox bulunamadı | Selenium Manager otomatik indirir; sürüm uyumsuzluğunda Chrome'u güncelle |
| n11.com istekleri fail | Rate limiting / bot protection devreye girmiş olabilir; `THINK_TIME_MAX` artır |

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

# Load Tests
make load-test                 # 1 user, 60s — assessment default (locust.conf)
make load-test-smoke           # smoke-tagged tasks only
make load-test-scale           # 10 users, 120s — scale test

# All Tests
make test-all                  # UI (Chrome) + Load Tests

# Reports
make report                    # Generate Allure HTML report
make report-open               # Generate + open in browser

# Cleanup
make clean                     # Delete automation-test-results/ and locust artifacts
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

### Load Testing (n11.com Search Module)

| Scenario | User Class | Weight | Tags | What is verified |
|----------|-----------|--------|------|-----------------|
| `category_search.py` | `CategorySearchUser` | 1 | `smoke` | Homepage → category page HTTP 200, response body size |
| `product_search.py` | `ProductSearchUser` | 3 | `smoke` `regression` | Keyword search 200, no-results detection, P95 threshold |
| `user_journey.py` | `UserJourneyUser` | 1 | — | Sequential homepage → search flow, interrupt + reschedule |

**Technologies**: Python · Locust · locust.conf · HttpUser · SequentialTaskSet

---

## Test Markers

### pytest (UI)

```bash
pytest -m smoke       # test_01, test_03 — fast critical-path check
pytest -m regression  # all 4 tests — full suite
```

### Locust (Load)

```bash
locust --headless --tags smoke       # CategorySearchUser + ProductSearchUser popular search
locust --headless --tags regression  # ProductSearchUser all tasks
locust --headless                    # all scenarios, all tasks (default)
```

---

## Environment Variables

### UI Tests

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://insiderone.com` | Homepage URL |
| `BROWSER` | `chrome` | Default browser when `--browser` not set |
| `HEADLESS` | `false` | Run browser in headless mode |
| `EXPLICIT_WAIT` | `30` | Selenium explicit wait timeout (seconds) |

### Load Tests

| Variable | Default | Description |
|----------|---------|-------------|
| `LOAD_TEST_ENV` | `production` | Target environment (`production` \| `staging`) |
| `P95_THRESHOLD_MS` | `3000` | P95 response time warning threshold (ms) |
| `THINK_TIME_MIN` | `2` | Minimum wait between tasks (seconds) |
| `THINK_TIME_MAX` | `5` | Maximum wait between tasks (seconds) |

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
| Load Testing | Locust | 2.x |
| Logging | colorlog | 6.8.x |
| CI/CD | GitHub Actions | — |
| Code Quality | flake8 + pre-commit | — |
