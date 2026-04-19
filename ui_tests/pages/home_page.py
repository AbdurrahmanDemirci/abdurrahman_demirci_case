from ui_tests.config import BASE_URL
from ui_tests.locators.home_page_locators import HomePageLocators as L
from ui_tests.pages.base_page import BasePage


class HomePage(BasePage):
    PAGE_URL = BASE_URL

    def is_page_loaded(self) -> bool:
        """Verify navigation header and hero section are both visible."""
        return (
            self._is_visible(L.homePage_mainNavigation_container)
            and self._is_visible(L.homePage_heroSection_section)
        )

    def go_to_careers(self) -> "HomePage":
        self._click(L.homePage_careersNavigation_link)
        return self
