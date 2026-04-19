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

from locust import HttpUser, TaskSet, between, tag, task

from load_tests.config import (
    BASE_URL, CATEGORY_SLUGS, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX,
)
from load_tests.utils.response_validator import (
    validate_category_response, validate_homepage_response,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class CategorySearchTasks(TaskSet):

    def on_start(self):
        with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
            validate_homepage_response(resp)

    @tag("smoke")
    @task
    def navigate_to_category(self):
        slug = random.choice(CATEGORY_SLUGS)
        with self.client.get(
            slug,
            headers=DEFAULT_HEADERS,
            name="/[category-slug]",
            catch_response=True,
        ) as resp:
            validate_category_response(resp, slug=slug)
            logger.info(
                f"Category | slug='{slug}' "
                f"| status={resp.status_code} | {resp.elapsed.total_seconds():.2f}s"
            )

    def on_stop(self):
        logger.info("CategorySearchTasks session ended.")


class CategorySearchUser(HttpUser):
    host      = BASE_URL
    weight    = 1
    tasks     = [CategorySearchTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
