import re
from datetime import datetime

import allure
import pytest

from ui_tests.utils.driver_factory import create_driver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Single browser: chrome | firefox. Omit to run both.",
    )
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Headless mode override: true | false",
    )


def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        browser_opt = metafunc.config.getoption("--browser")
        browsers = [browser_opt] if browser_opt else ["chrome", "firefox"]
        metafunc.parametrize("driver", browsers, indirect=True)


@pytest.fixture
def driver(request):
    browser = request.param
    headless_opt = request.config.getoption("--headless")
    headless = headless_opt.lower() == "true" if headless_opt is not None else None

    d = create_driver(browser=browser, headless=headless)
    d.implicitly_wait(0)
    d.maximize_window()
    yield d
    d.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        d = item.funcargs.get("driver")
        if d:
            test_name = re.sub(r"[^\w\-]", "_", item.name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            allure.attach(
                d.get_screenshot_as_png(),
                name=f"FAIL_{test_name}_{timestamp}",
                attachment_type=allure.attachment_type.PNG,
            )
