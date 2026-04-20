"""
Load Test Configuration
=======================
Central config for all load test scenarios.
To add a new environment: add an entry to ENVIRONMENTS.
To add new category targets: extend CATEGORY_SLUGS.
Test data (keywords, queries) lives in data/search_data.py.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Environments
# ---------------------------------------------------------------------------
ENVIRONMENTS = {
    "production": "https://www.n11.com",
    "staging":    "https://staging.n11.com",
    "local":      "http://localhost:3000",
}

TARGET_ENV = os.getenv("LOAD_TEST_ENV")
BASE_URL    = ENVIRONMENTS[TARGET_ENV]

# ---------------------------------------------------------------------------
# Shared HTTP headers (browser-like, avoids bot rejection)
# ---------------------------------------------------------------------------
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ---------------------------------------------------------------------------
# Route targets (environment-specific, not test data)
# ---------------------------------------------------------------------------
CATEGORY_SLUGS = [
    "/bilgisayar",
    "/telefon-ve-aksesuarlari",
]

# ---------------------------------------------------------------------------
# Performance thresholds (env-configurable)
# ---------------------------------------------------------------------------
MIN_RESPONSE_BODY_SIZE = int(os.getenv("MIN_RESPONSE_BODY_SIZE"))
RESPONSE_TIME_P95_MS   = int(os.getenv("P95_THRESHOLD_MS"))

# ---------------------------------------------------------------------------
# Think time (env-configurable)
# ---------------------------------------------------------------------------
THINK_TIME_MIN = float(os.getenv("THINK_TIME_MIN"))
THINK_TIME_MAX = float(os.getenv("THINK_TIME_MAX"))
