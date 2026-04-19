"""
Scenario: Category Search
=========================
Simulates a user who selects a category from search autocomplete suggestions.
Flow: Homepage → category listing page

Scalability note
----------------
New categories = add slug to config.CATEGORY_SLUGS.
New environments = set LOAD_TEST_ENV env var.
"""

import random

from locust import HttpUser, between, task

from load_tests.config import BASE_URL, CATEGORY_SLUGS, DEFAULT_HEADERS, MIN_RESPONSE_BODY_SIZE


class CategorySearchUser(HttpUser):
    host = BASE_URL
    wait_time = between(2, 4)

    def on_start(self):
        with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Homepage unreachable: {resp.status_code}")
            else:
                resp.success()

    @task
    def navigate_to_category(self):
        slug = random.choice(CATEGORY_SLUGS)
        with self.client.get(
            slug,
            headers=DEFAULT_HEADERS,
            name="/[category-slug]",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Category page failed [{slug}]: {resp.status_code}")
            elif len(resp.text) < MIN_RESPONSE_BODY_SIZE:
                resp.failure(f"Category page body too small — possible empty/error page: {slug}")
            else:
                resp.success()
