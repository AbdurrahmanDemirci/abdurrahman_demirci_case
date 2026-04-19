from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from ui_tests.config import BROWSER, HEADLESS


def create_driver(browser: str | None = None, headless: bool | None = None) -> webdriver.Remote:
    _browser = (browser or BROWSER).lower()
    _headless = headless if headless is not None else HEADLESS

    if _browser == "chrome":
        options = ChromeOptions()
        if _headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    if _browser in ("firefox", "gecko"):
        options = FirefoxOptions()
        if _headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    raise ValueError(f"Unsupported browser: {_browser!r}. Use 'chrome' or 'firefox'.")
