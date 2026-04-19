from locust import TaskSet

from load_tests.config import DEFAULT_HEADERS
from load_tests.utils.logger import get_logger
from load_tests.utils.response_validator import validate_homepage_response

logger = get_logger(__name__)


class BaseTaskSet(TaskSet):

    def on_start(self) -> None:
        with self.client.get("/", headers=DEFAULT_HEADERS, catch_response=True) as resp:
            validate_homepage_response(resp)

    def on_stop(self) -> None:
        logger.info(f"{self.__class__.__name__} session ended.")
