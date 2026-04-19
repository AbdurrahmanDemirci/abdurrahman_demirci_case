from load_tests.config import MIN_RESPONSE_BODY_SIZE, RESPONSE_TIME_P95_MS
from load_tests.data.search_data import NO_RESULTS_TEXT
from load_tests.utils.logger import get_logger

logger = get_logger(__name__)


def validate_search_response(response, query: str = "") -> bool:
    if response.status_code != 200:
        response.failure(f"Expected 200, got {response.status_code} | query='{query}'")
        logger.error(f"Search failed | status={response.status_code} | query='{query}'")
        return False

    if NO_RESULTS_TEXT in response.text.lower():
        response.failure(f"Zero results returned for query: '{query}'")
        logger.warning(f"No results | query='{query}'")
        return False

    elapsed_ms = response.elapsed.total_seconds() * 1000
    if elapsed_ms > RESPONSE_TIME_P95_MS:
        logger.warning(
            f"Slow response | {elapsed_ms:.0f}ms > p95 {RESPONSE_TIME_P95_MS}ms"
            f" | query='{query}'"
        )

    response.success()
    return True


def validate_homepage_response(response) -> bool:
    if response.status_code != 200:
        response.failure(f"Homepage returned {response.status_code}")
        logger.error(f"Homepage failed | status={response.status_code}")
        return False

    response.success()
    return True


def validate_edge_case_response(response, query: str = "") -> bool:
    if response.status_code in (200, 301, 302):
        response.success()
        return True
    response.failure(
        f"Unexpected status for edge case | status={response.status_code} | query='{query}'"
    )
    logger.warning(f"Edge case failed | status={response.status_code} | query='{query}'")
    return False


def validate_category_response(response, slug: str = "") -> bool:
    if response.status_code != 200:
        response.failure(f"Category page failed [{slug}]: {response.status_code}")
        logger.error(f"Category failed | status={response.status_code} | slug='{slug}'")
        return False

    if len(response.text) < MIN_RESPONSE_BODY_SIZE:
        response.failure(f"Category page body too small — possible empty/error page: {slug}")
        logger.warning(f"Thin response | slug='{slug}' | size={len(response.text)}")
        return False

    elapsed_ms = response.elapsed.total_seconds() * 1000
    if elapsed_ms > RESPONSE_TIME_P95_MS:
        logger.warning(
            f"Slow response | {elapsed_ms:.0f}ms > p95 {RESPONSE_TIME_P95_MS}ms"
            f" | slug='{slug}'"
        )

    response.success()
    return True
