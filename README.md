# InsiderOne Senior QA Engineer Assessment

[![Test Suite](https://github.com/AbdurrahmanDemirci/abdurrahman_demirci_case/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/AbdurrahmanDemirci/abdurrahman_demirci_case/actions/workflows/tests.yml)

A production-grade, three-layer test automation framework covering **UI automation** (InsiderOne Careers), **API testing** (Petstore CRUD), and **load testing** (n11.com Search) — built with Python, Selenium, pytest, and Locust.

> This project was developed collaboratively with [Claude Code](https://claude.ai/code) by Anthropic. The engineering standards, architectural decisions, and code quality applied throughout this framework reflect my professional approach to QA automation. I believe in transparent human–AI collaboration as a force multiplier for engineering excellence.

---

## 🚀 Features

**UI Automation**
- 5-layer Page Object Model: Locators → Pages → Flows → Data → Tests
- Cross-browser execution (Chrome + Firefox) via a single pytest run
- Automatic screenshot capture on test failure, attached inline to Allure report
- Explicit-wait-only strategy — no implicit/explicit interference
- Selenium Manager built-in driver management (no third-party driver manager)

**API Testing**
- Full CRUD coverage for Petstore `/pet` endpoint — 18 test methods across 6 operation files
- `BaseAPI` base class: shared session, headers, and automatic request/response logging
- `PetBuilder` builder pattern for clean, variant-specific test payloads
- JSON Schema validation (`jsonschema`) on every positive response
- REST contract assertions: Content-Type header, idempotent DELETE, BVA negative ID
- Lifecycle test: Create → Read → Update → Verify Persistence → Delete → Verify 404

**Load Testing**
- Modular Locust design: add a scenario by creating one file + one import line
- 3 weighted user types (ProductSearch 60%, Category 20%, Journey 20%)
- P95 response time threshold check per request, configurable via env var
- `smoke` / `regression` task tags for selective execution
- Multi-environment support via `LOAD_TEST_ENV` (production / staging / local)

**DevOps**
- GitHub Actions CI: Chrome + Firefox matrix + API + Load test jobs run in parallel
- Allure and Locust HTML reports uploaded as artifacts on every run
- 30+ `make` targets covering every test combination, report generation, and cleanup
- `--reruns=2` automatic retry with configurable delay for flaky tests

---

## 🧱 Tech Stack

**Testing Tools**

| Technology | Purpose | Version |
|-----------|---------|---------|
| Python | Language | 3.10+ |
| Selenium | UI automation | 4.18.1 |
| pytest | Test runner | 8.1.1 |
| pytest-xdist | Parallel execution | 3.5.0 |
| pytest-rerunfailures | Flaky test retry | 14.0 |
| allure-pytest | Reporting | 2.13.5 |
| requests | HTTP client for API tests | 2.32.3 |
| jsonschema | API response schema validation | 4.23.0 |
| Locust | Load testing | 2.32.3 |

**Infrastructure & Utilities**

| Technology | Purpose | Version |
|-----------|---------|---------|
| GitHub Actions | CI/CD | — |
| Selenium Manager | Automatic driver management (built-in) | — |
| python-dotenv | Environment config | 1.0.1 |
| colorlog | Structured colored logging | 6.8.2 |

---

## ⚙️ Installation

**Prerequisites:** Python 3.10+, Google Chrome and/or Firefox

```bash
git clone https://github.com/AbdurrahmanDemirci/abdurrahman_demirci_case.git
cd abdurrahman_demirci_case

python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
cp .env.example .env
```

No manual driver installation needed — Selenium Manager downloads ChromeDriver and GeckoDriver automatically.

### Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://insiderone.com` | UI test target URL |
| `BROWSER` | `chrome` | Default browser (`chrome` \| `firefox`) |
| `HEADLESS` | `false` | Headless browser mode |
| `EXPLICIT_WAIT` | `30` | Selenium explicit wait timeout (seconds) |
| `API_BASE_URL` | `https://petstore.swagger.io/v2` | API test base URL |
| `API_TIMEOUT` | `10` | HTTP request timeout (seconds) |
| `LOAD_TEST_ENV` | `production` | Load test target (`production` \| `staging` \| `local`) |
| `P95_THRESHOLD_MS` | `3000` | P95 response time warning threshold (ms) |
| `THINK_TIME_MIN` | `2` | Minimum think time between tasks (seconds) |
| `THINK_TIME_MAX` | `5` | Maximum think time between tasks (seconds) |

---

## ▶️ Usage

### Make Commands

```bash
make help                  # list all available targets

# UI Tests
make ui-chrome             # Chrome (headed)
make ui-firefox            # Firefox (headed)
make ui-all-headless       # Chrome + Firefox headless (CI mode)
make ui-parallel           # Chrome, -n auto workers

# API Tests
make api-test              # full suite
make api-smoke             # smoke markers only

# Load Tests
make load-test             # 1 user, 60s (assessment default)
make load-test-smoke       # smoke-tagged tasks only
make load-test-scale       # 10 users, 120s

# Reports
make report-open-ui        # generate + open Allure UI report
make report-open-api       # generate + open Allure API report

# Cleanup
make clean
```

### pytest Directly

```bash
pytest -m smoke                                          # critical-path only
pytest -m regression                                     # full suite
pytest ui_tests/tests/ --browser=chrome
pytest api_tests/tests/
pytest api_tests/tests/test_pet_lifecycle.py -v
```

### Locust

```bash
locust --headless                               # 1 user, 60s (locust.conf defaults)
locust --headless --tags smoke                  # smoke scenarios only
locust --headless -u 10 -r 2 --run-time 120s   # scale test
LOAD_TEST_ENV=staging locust --headless         # staging environment
locust                                          # web UI at http://localhost:8089
```

---

## 🏗️ Architecture

### UI — Five-Layer POM

```
ui_tests/
├── locators/   ← WHAT to find      CSS/XPath only — zero logic
├── pages/      ← HOW to interact   BasePage subclasses — zero selectors
├── flows/      ← WHICH sequence    cross-page business flows
├── data/       ← WHAT to expect    assertion constants — zero inline strings
└── tests/      ← WHAT to verify    imports everything above — zero locators
```

A selector change touches exactly **one** locator file. Pages, flows, and tests are untouched.

### API — Four-Layer Architecture

```
api_tests/
├── api/        ← BaseAPI           session, headers, _get/_post/_put/_delete + auto-logging
├── client/     ← PetClient(BaseAPI) 5 CRUD methods, no raw HTTP
├── models/     ← PetBuilder        full(), minimal(), without_name(), invalid_body()
├── schemas/    ← PET_RESPONSE_SCHEMA  jsonschema, additionalProperties: false
├── data/       ← constants         INVALID_PET_ID, NEGATIVE_PET_ID, VALID_STATUSES
├── tests/      ← 6 operation files test_pet_{create,read,update,delete,lifecycle,negative}.py
└── conftest.py                     client (session-scoped) + created_pet (teardown fixture)
```

### Load — Modular Locust Design

```
load_tests/
├── locustfile.py   ← thin entry point — imports user classes, no task logic
├── config.py       ← env-driven: base URL, P95 threshold, think time
├── data/           ← POPULAR_QUERIES, TECH_QUERIES, EDGE_CASE_QUERIES
├── utils/          ← response_validator (P95 checks) + logger (sys.path-safe)
└── scenarios/      ← one file per user type; __init__.py registers them all
```

Adding a scenario = one new file + one import line in `__init__.py`. Nothing else changes.

### Key Decisions

| Decision | Rationale |
|----------|-----------|
| `flows/` layer | Extracts repeated multi-page sequences (cookie handling, QA job navigation) out of tests |
| `pytest_generate_tests` parametrization | Chrome + Firefox from a single `pytest` invocation; failures isolated per browser |
| `implicitly_wait(0)` | Prevents silent implicit/explicit wait conflicts; all waits are explicit |
| `BaseAPI` inheritance | Shared session, headers, and logging in one place; each client adds only method definitions |
| `jsonschema` with `additionalProperties: false` | Strict contract — unexpected response fields fail the test immediately |
| `created_pet` fixture with `yield` | Guaranteed API cleanup even when the test itself fails |
| Self-contained `load_tests/utils/` | Avoids `sys.path` collision when Locust prepends the locustfile directory |

---

## 🧪 Testing

### UI (InsiderOne Careers)

| Test | Markers | What is verified |
|------|---------|-----------------|
| `test_01_home_page_is_opened_and_loaded` | smoke, regression | URL, title keyword, main blocks visible |
| `test_02_careers_page_is_opened_and_loaded` | regression | Careers URL, department section visible |
| `test_03_qa_jobs_listed` | smoke, regression | QA job board present on Lever |
| `test_04_first_qa_job_details_are_correct` | regression | Position, department, location match |

Each test runs on **both Chrome and Firefox** — `pytest_generate_tests` parametrizes the `driver` fixture at collection time.

### API (Petstore Pet CRUD)

| File | Tests | Coverage |
|------|-------|----------|
| `test_pet_create.py` | 2 | POST full payload + schema; POST minimal payload |
| `test_pet_read.py` | 4 | GET by ID + schema; GET findByStatus (parametrized × 3 statuses) |
| `test_pet_update.py` | 2 | PUT + schema; PUT persistence verify (GET after PUT) |
| `test_pet_delete.py` | 2 | DELETE + GET 404; idempotent DELETE (second call → 404) |
| `test_pet_lifecycle.py` | 1 | Create → Read → Update → Verify Persistence → Delete → Verify 404 |
| `test_pet_negative.py` | 7 | Non-existent ID, string ID, negative ID (BVA), no body, invalid type, invalid status |

**18 tests total** — 4 smoke, 18 regression. All positive tests assert status code, response fields, Content-Type header, and JSON Schema.

### Load (n11.com Search)

| Scenario | Weight | Tags | Assertions |
|----------|--------|------|-----------|
| `CategorySearchUser` | 1 | smoke | HTTP 200, response body ≥ 500 bytes |
| `ProductSearchUser` | 3 | smoke, regression | HTTP 200, P95 ≤ 3000ms, no-results detection |
| `UserJourneyUser` | 1 | — | Sequential homepage → search flow completion |

### Allure Reports

```bash
allure serve automation-test-results/ui/allure-results   # UI
allure serve automation-test-results/api/allure-results  # API
```

---

## 🔐 Security & Best Practices

- Secrets and environment config live in `.env` (gitignored); `.env.example` ships with no real values
- All endpoints, timeouts, and thresholds are environment-driven — no hardcoded URLs in test code
- `requests.Session()` per test run — connection pooling without shared mutable state between tests
- `created_pet` fixture teardown is guaranteed via `yield` — the API is cleaned up even on failure
- Load tests use a browser-like `User-Agent` to reflect realistic traffic, not to circumvent controls
- Selenium `implicitly_wait(0)` is set explicitly to prevent silent interactions with default timeouts

---

## 📦 Deployment

### Local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make ui-all-headless   # headless UI suite
make api-test          # API suite
make load-test         # load test (1 user, 60s)
```

### CI (GitHub Actions)

Push or open a PR against `main`, `master`, or `develop`. Four jobs run in parallel:

| Job | Mode | Artifact |
|-----|------|---------|
| UI Tests — Chrome | headless | Allure results (7 days) |
| UI Tests — Firefox | headless | Allure results (7 days) |
| API Tests | — | Allure results (7 days) |
| Load Tests | headless, 1 user / 60s | Locust HTML report (7 days) |

Path filters ensure only changed test directories trigger their respective jobs.

### Docker

Not yet containerized — tracked in the roadmap. To run headlessly today, set `HEADLESS=true` in `.env` and use any standard Python Docker image.

---

## 🗺️ Roadmap

- [ ] Add `User` and `Store` endpoint coverage using the existing API client layer
- [ ] Dockerize the test suite for fully portable, dependency-free execution
- [ ] Extend load test to staging with production vs. staging threshold comparison
- [ ] Allure Trend reports for historical pass-rate tracking across runs

---

## 🤝 Contributing

1. Fork the repository and create a feature branch
2. Follow the existing layer conventions — no selectors in tests, no inline assertion strings, no hardcoded payloads
3. Run `make ui-all-headless` and `make api-test` locally before opening a PR
4. Use [Conventional Commits](https://www.conventionalcommits.org/) — `feat`, `fix`, `test`, `refactor`, `chore`

---

## 📄 License

This project is submitted as part of a Senior QA Engineer technical assessment and is not licensed for redistribution.

---

### Troubleshooting

| Error | Fix |
|-------|-----|
| `allure: command not found` | `brew install allure` (macOS) or see [allurereport.org](https://allurereport.org/docs/) |
| `ModuleNotFoundError: load_tests` | Run from the project root — `pythonpath = .` is set in `pytest.ini` |
| Chrome/Firefox not found | Selenium Manager downloads the driver automatically; update Chrome if version mismatch |
| n11.com requests failing | Rate limiting may be active — increase `THINK_TIME_MAX` in `.env` |
| API tests flaky | Petstore is a public demo API — `--reruns=2` handles transient failures automatically |
