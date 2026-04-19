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

from locust import HttpUser, between, tag, task

from load_tests.config import (
    BASE_URL, CATEGORY_SLUGS, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX,
)
from load_tests.utils.base_task_set import BaseTaskSet
from load_tests.utils.logger import get_logger
from load_tests.utils.response_validator import validate_category_response

logger = get_logger(__name__)


class CategorySearchTasks(BaseTaskSet):

    @tag("smoke")
    @task
    def navigate_to_category(self) -> None:
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


class CategorySearchUser(HttpUser):
    host      = BASE_URL
    weight    = 1
    tasks     = [CategorySearchTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
