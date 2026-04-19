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

from locust import HttpUser, TaskSet, between, tag, task

from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.data.search_data import EDGE_CASE_QUERIES, POPULAR_QUERIES, TECH_QUERIES
from load_tests.utils.response_validator import (
    validate_edge_case_response, validate_homepage_response, validate_search_response,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductSearchTasks(TaskSet):

    def on_start(self):
        with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
            validate_homepage_response(resp)

    @tag("smoke", "regression")
    @task(5)
    def search_popular_keyword(self):
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
    def search_tech_category(self):
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
    def search_edge_cases(self):
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

    def on_stop(self):
        logger.info("ProductSearchTasks session ended.")


class ProductSearchUser(HttpUser):
    host      = BASE_URL
    weight    = 3
    tasks     = [ProductSearchTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
