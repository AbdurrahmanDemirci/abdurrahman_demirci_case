from ui_tests.locators.home_page_locators import HomePageLocators as L
from ui_tests.pages.base_page import BasePage
from ui_tests.pages.careers_page import CareersPage
from ui_tests.pages.job_listing_page import JobListingPage

_COOKIE_ACTIONS = {
    "accept_all":     L.homePage_cookieAccept_btn,
    "only_necessary": L.homePage_cookieOnlyNecessary_btn,
    "decline_all":    L.homePage_cookieDecline_btn,
}


class SiteFlow(BasePage):

    def handle_cookie_banner(self, action: str = "accept_all") -> None:
        if action not in _COOKIE_ACTIONS:
            raise ValueError(
                f"Unknown cookie action '{action}'. "
                f"Allowed: {list(_COOKIE_ACTIONS)}"
            )
        self._click_if_exists(_COOKIE_ACTIONS[action])

    def navigate_to_qa_jobs(self, home_page) -> JobListingPage:
        home_page.go_to_careers()
        careers = CareersPage(self.driver)
        careers.click_see_all_teams()
        return careers.click_qa_open_positions()
