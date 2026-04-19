"""
n11.com Search Module — Load Test Entry Point
=============================================
Target : https://www.n11.com  (configurable via LOAD_TEST_ENV env var)
Scope  : Header search behavior — category navigation & product search results

Architecture
------------
This file is intentionally thin. All scenarios live in load_tests/scenarios/.
Adding a new scenario = create a new file there + one import in scenarios/__init__.py.

  load_tests/
  ├── locustfile.py          ← entry point (this file)
  ├── config.py              ← environments, test data, thresholds
  └── scenarios/
      ├── __init__.py        ← registers all scenario classes
      ├── category_search.py ← Scenario A: category page via suggestion
      └── product_search.py  ← Scenario B: keyword search → /arama?q=

Run
---
# Behavioral check — 1 user, 60 seconds (assessment default)
locust -f load_tests/locustfile.py --headless -u 1 -r 1 --run-time 60s

# Scale up — 10 concurrent users
locust -f load_tests/locustfile.py --headless -u 10 -r 2 --run-time 120s

# Specific environment
LOAD_TEST_ENV=staging locust -f load_tests/locustfile.py --headless -u 1 -r 1 --run-time 60s

# Web UI (real-time charts)
locust -f load_tests/locustfile.py
"""

from load_tests.scenarios import CategorySearchUser, ProductSearchUser  # noqa: F401

# Locust discovers user classes automatically from this module's namespace.
# No further code needed here — extend via scenarios/ directory.
