"""
Load Test Configuration
=======================
Central config for all load test scenarios.
To add a new environment: add an entry to ENVIRONMENTS.
To add new test data: extend CATEGORY_SLUGS or SEARCH_KEYWORDS.
"""

import os

# ---------------------------------------------------------------------------
# Environments
# ---------------------------------------------------------------------------
ENVIRONMENTS = {
    "production": "https://www.n11.com",
    "staging":    "https://staging.n11.com",   # update when staging URL is known
    "local":      "http://localhost:3000",
}

TARGET_ENV = os.getenv("LOAD_TEST_ENV", "production")
BASE_URL = ENVIRONMENTS[TARGET_ENV]

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
# Test data
# Adding a new category or keyword = one line below, no other file changes.
# ---------------------------------------------------------------------------
CATEGORY_SLUGS = [
    "/bilgisayar",
    "/telefon-ve-aksesuarlari",
]

SEARCH_KEYWORDS = [
    "Apple Macbook Pro m5",
    "iPhone 17 Pro Max",
    "Samsung Galaxy S25",
    "Sony WH-1000XM5",
    "Xiaomi tablet",
]

# ---------------------------------------------------------------------------
# Thresholds (used in response validation)
# ---------------------------------------------------------------------------
MIN_RESPONSE_BODY_SIZE = 500   # bytes — anything smaller = likely empty/error page
