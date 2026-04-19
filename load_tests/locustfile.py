"""
n11.com Search Module — Load Test Entry Point
=============================================
Target : https://www.n11.com  (configurable via LOAD_TEST_ENV env var)
Scope  : Header search behavior — category navigation, product search, user journeys

Architecture
------------
This file is intentionally thin. All scenarios live in load_tests/scenarios/.
Adding a new scenario = create a new file there + one import in scenarios/__init__.py.

  load_tests/
  ├── locustfile.py              ← entry point (this file)
  ├── locust.conf                ← default CLI parameters
  ├── config.py                  ← environments, thresholds, think time
  ├── data/
  │   └── search_data.py         ← categorized test data
  ├── utils/
  │   └── response_validator.py  ← shared validation + P95 threshold checks
  └── scenarios/
      ├── __init__.py            ← registers all scenario classes
      ├── category_search.py     ← Scenario A: category page via suggestion  [smoke]
      ├── product_search.py      ← Scenario B: weighted keyword searches     [smoke+regression]
      └── user_journey.py        ← Scenario C: sequential homepage→search journey

User distribution (weight):
  ProductSearchUser  : weight=3 → ~60% of users
  CategorySearchUser : weight=1 → ~20% of users
  UserJourneyUser    : weight=1 → ~20% of users

Run
---
# Behavioral check — 1 user, 60 seconds (all defaults from locust.conf)
locust --headless

# Scale up — 10 concurrent users
locust --headless -u 10 -r 2 --run-time 120s

# Smoke only
locust --headless --tags smoke

# Staging environment
LOAD_TEST_ENV=staging locust --headless

# Web UI (real-time charts)
locust
"""

from load_tests.scenarios import (  # noqa: F401
    CategorySearchUser, ProductSearchUser, UserJourneyUser,
)

# Locust discovers user classes automatically from this module's namespace.
# No further code needed here — extend via scenarios/ directory.
