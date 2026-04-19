import pytest
import allure

from ui_tests.data.expected_content import EXPECTED_HOME_TITLE_KEYWORD
from ui_tests.flows.site_flow import SiteFlow
from ui_tests.pages.home_page import HomePage


@allure.parent_suite("UI Tests")
@allure.suite("Home Page")
class TestHomePage:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.flow = SiteFlow(driver)
        self.home = HomePage(self.driver)
        self.home.open()
        self.flow.handle_cookie_banner()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_01_home_page_is_opened_and_loaded(self):
        """
        Step 1: Visit https://insiderone.com and verify the home page
        is opened with all main blocks loaded.
        """
        assert self.home.is_on_correct_page(), (
            f"Expected URL to contain '{self.home.PAGE_URL}', got: {self.home.get_current_url()}"
        )
        assert EXPECTED_HOME_TITLE_KEYWORD in self.home.get_title(), (
            f"Expected '{EXPECTED_HOME_TITLE_KEYWORD}' in title, got: '{self.home.get_title()}'"
        )
        assert self.home.is_page_loaded(), "Main navigation header and hero section are not visible"
