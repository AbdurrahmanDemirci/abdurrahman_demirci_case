import logging

import requests

from api_tests.config import BASE_URL, TIMEOUT

logger = logging.getLogger(__name__)


class BaseAPI:
    base_url: str = BASE_URL
    timeout: int = TIMEOUT

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _get(self, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("GET %s", url)
        resp = self.session.get(url, timeout=self.timeout, **kwargs)
        logger.info("← %d %s", resp.status_code, url)
        return resp

    def _post(self, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("POST %s", url)
        resp = self.session.post(url, timeout=self.timeout, **kwargs)
        logger.info("← %d %s", resp.status_code, url)
        return resp

    def _put(self, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("PUT %s", url)
        resp = self.session.put(url, timeout=self.timeout, **kwargs)
        logger.info("← %d %s", resp.status_code, url)
        return resp

    def _delete(self, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("DELETE %s", url)
        resp = self.session.delete(url, timeout=self.timeout, **kwargs)
        logger.info("← %d %s", resp.status_code, url)
        return resp
