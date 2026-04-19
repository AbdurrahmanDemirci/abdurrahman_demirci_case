"""
Scenario: Product Search
========================
Simulates a user who types a keyword in the header search box and views results.
Flow: Homepage → /arama?q=<keyword> → search results listing

Scalability note
----------------
New keywords = add to config.SEARCH_KEYWORDS.
New environments = set LOAD_TEST_ENV env var.
To test authenticated search (future): override on_start to perform login first.
"""

import random

from locust import HttpUser, between, task

from load_tests.config import BASE_URL, DEFAULT_HEADERS, SEARCH_KEYWORDS


class ProductSearchUser(HttpUser):
    host = BASE_URL
    wait_time = between(2, 4)

    def on_start(self):
        with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Homepage unreachable: {resp.status_code}")
            else:
                resp.success()

    @task
    def search_product(self):
        keyword = random.choice(SEARCH_KEYWORDS)
        with self.client.get(
            "/arama",
            params={"q": keyword},
            headers=DEFAULT_HEADERS,
            name="/arama?q=[keyword]",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Search failed [{keyword}]: {resp.status_code}")
            elif "sonuç bulunamadı" in resp.text.lower():
                resp.failure(f"Zero results returned for keyword: {keyword}")
            else:
                resp.success()
