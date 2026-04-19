"""
Scenario: Full User Journey
============================
Simulates a complete user session in strict sequence:
  homepage → keyword search → view results

Uses SequentialTaskSet to enforce execution order.
interrupt(reschedule=True) at the end restarts the journey loop.

Scalability note
----------------
New journey steps = add @task methods in the desired sequence position.
Step state (current query) is stored on the instance between steps.
"""

import random

from locust import HttpUser, SequentialTaskSet, between, task

from load_tests.config import BASE_URL, DEFAULT_HEADERS, THINK_TIME_MIN, THINK_TIME_MAX
from load_tests.data.search_data import POPULAR_QUERIES
from load_tests.utils.response_validator import validate_homepage_response, validate_search_response
from load_tests.utils.logger import get_logger

logger = get_logger(__name__)


class UserJourneyTasks(SequentialTaskSet):
    _current_query: str = "laptop"

    @task
    def visit_homepage(self) -> None:
        with self.client.get(
            "/",
            headers=DEFAULT_HEADERS,
            name="/ (homepage)",
            catch_response=True,
        ) as resp:
            validate_homepage_response(resp)
            logger.info(
                f"Homepage | status={resp.status_code} | {resp.elapsed.total_seconds():.2f}s"
            )

    @task
    def perform_search(self) -> None:
        self._current_query = random.choice(POPULAR_QUERIES)
        with self.client.get(
            "/arama",
            params={"q": self._current_query},
            headers=DEFAULT_HEADERS,
            name="/arama?q=[keyword]",
            catch_response=True,
        ) as resp:
            validate_search_response(resp, query=self._current_query)
            logger.info(
                f"Journey | search | query='{self._current_query}' "
                f"| {resp.elapsed.total_seconds():.2f}s"
            )

        self.interrupt(reschedule=True)


class UserJourneyUser(HttpUser):
    host      = BASE_URL
    weight    = 1
    tasks     = [UserJourneyTasks]
    wait_time = between(THINK_TIME_MIN, THINK_TIME_MAX)
