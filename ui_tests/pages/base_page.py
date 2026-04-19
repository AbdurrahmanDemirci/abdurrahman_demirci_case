from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ui_tests.config import EXPLICIT_WAIT
from ui_tests.utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._wait = WebDriverWait(driver, EXPLICIT_WAIT)

    @staticmethod
    def _name(locator: tuple) -> str:
        return getattr(locator, "name", f"{locator[0]} '{locator[1]}'")

    def _find(self, locator: tuple) -> WebElement:
        logger.info("WAIT → %s", self._name(locator))
        return self._wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator: tuple) -> None:
        logger.info("CLICK → %s", self._name(locator))
        element = self._wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            logger.info("CLICK (JS fallback) → %s", self._name(locator))
            self.driver.execute_script("arguments[0].click();", element)

    def _click_if_exists(self, locator: tuple, timeout: int = 5) -> bool:
        """Click element if it appears within timeout. Returns True if clicked."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
            logger.info("CLICK (optional) → %s", self._name(locator))
            return True
        except TimeoutException:
            logger.info("SKIP (not found) → %s", self._name(locator))
            return False

    def _is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def open(self) -> "BasePage":
        logger.info("OPEN → %s", self.PAGE_URL)
        self.driver.get(self.PAGE_URL)
        self.wait_for_document_ready()
        return self

    def _navigate_via_href(self, locator: tuple) -> None:
        """Read the href attribute of a link element and navigate to it directly.
        Use instead of click() when the anchor's click handler does not trigger navigation."""
        element = self._find(locator)
        href = element.get_attribute("href")
        logger.info("NAVIGATE → %s: %s", self._name(locator), href)
        self.driver.get(href)
        self.wait_for_document_ready()

    def wait_for_document_ready(self) -> None:
        self._wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def is_on_correct_page(self) -> bool:
        """Check current URL contains this page's expected URL. Override PAGE_URL in subclass."""
        return self.PAGE_URL in self.driver.current_url
