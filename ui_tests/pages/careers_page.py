from ui_tests.config import BASE_URL
from ui_tests.locators.careers_page_locators import CareersPageLocators as L
from ui_tests.pages.base_page import BasePage
from ui_tests.pages.job_listing_page import JobListingPage


class CareersPage(BasePage):
    PAGE_URL = BASE_URL + "/careers/"

    def is_page_loaded(self) -> bool:
        return self._is_visible(L.careersPage_departmentCards_section)

    def click_see_all_teams(self) -> "CareersPage":
        self._click(L.careersPage_seeAllTeams_btn)
        return self

    def click_qa_open_positions(self) -> JobListingPage:
        self._navigate_via_href(L.careersPage_qaOpenPositions_btn)
        return JobListingPage(self.driver)
