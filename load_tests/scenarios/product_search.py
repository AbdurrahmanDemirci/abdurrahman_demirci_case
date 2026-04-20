"""
Scenario: Product Search
========================
Simulates users performing keyword searches with varied intents:
popular queries, tech-specific searches, and edge cases.

Scalability note
----------------
New query categories → add list to data/search_data.py, import here.
New environments     → set LOAD_TEST_ENV env var.
"""

import random

from locust import HttpUser, between, tag, task

from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.data.search_data import EDGE_CASE_QUERIES, POPULAR_QUERIES, TECH_QUERIES
from load_tests.utils.base_task_set import BaseTaskSet
from load_tests.utils.logger import get_logger
from load_tests.utils.response_validator import (
    validate_edge_case_response, validate_search_response,
)

logger = get_logger(__name__)


class ProductSearchTasks(BaseTaskSet):

    @tag("smoke", "regression")
    @task(5)
    def search_popular_keyword(self) -> None:
        query = random.choice(POPULAR_QUERIES)
        with self.client.get(
            "/arama",
            params={"q": query},
            headers=DEFAULT_HEADERS,
            name="/arama?q=[popular]",
            catch_response=True,
        ) as resp:
            validate_search_response(resp, query=query)
            logger.info(
                f"Popular search | query='{query}' "
                f"| status={resp.status_code} | {resp.elapsed.total_seconds():.2f}s"
            )

    @tag("regression")
    @task(2)
    def search_tech_category(self) -> None:
        query = random.choice(TECH_QUERIES)
        with self.client.get(
            "/arama",
            params={"q": query},
            headers=DEFAULT_HEADERS,
            name="/arama?q=[tech]",
            catch_response=True,
        ) as resp:
            validate_search_response(resp, query=query)
            logger.info(
                f"Tech search | query='{query}' "
                f"| {resp.elapsed.total_seconds():.2f}s"
            )

    @tag("regression")
    @task(1)
    def search_edge_cases(self) -> None:
        query = random.choice(EDGE_CASE_QUERIES)
        with self.client.get(
            "/arama",
            params={"q": query},
            headers=DEFAULT_HEADERS,
            name="/arama?q=[edge_case]",
            catch_response=True,
        ) as resp:
            validate_edge_case_response(resp, query=query)
            logger.info(
                f"Edge case | query='{query}' "
                f"| status={resp.status_code} | {resp.elapsed.total_seconds():.2f}s"
            )


class ProductSearchUser(HttpUser):
    host      = BASE_URL
    weight    = 3
    tasks     = [ProductSearchTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
