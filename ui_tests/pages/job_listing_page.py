from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ui_tests.config import EXPLICIT_WAIT
from ui_tests.locators.job_listing_page_locators import JobListingPageLocators as L
from ui_tests.pages.base_page import BasePage
from ui_tests.utils.logger import get_logger

logger = get_logger(__name__)


class JobListingPage(BasePage):
    PAGE_URL = "https://jobs.lever.co/insiderone"

    def is_job_list_present(self) -> bool:
        """Returns True if at least one job posting is visible on the Lever board."""
        try:
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located(L.leverPage_jobItems_list)
            )
            items = self.driver.find_elements(*L.leverPage_jobItems_list)
            logger.info("Job listings found: %d", len(items))
            return len(items) > 0
        except Exception:
            return False

    def select_istanbul_location(self) -> None:
        current_url = self.get_current_url().split("&location=")[0]
        self.driver.get(f"{current_url}&location=Istanbul")
        WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located(L.leverPage_jobItems_list)
        )

    def click_first_apply_button(self) -> None:
        """Two-step Lever flow: listing Apply → job detail → Apply for this job → form."""
        self._click(L.leverPage_applyBtn)
        self._click(L.leverPage_jobDetailApplyBtn)

    def is_on_apply_form(self) -> bool:
        return "/apply" in self.get_current_url()

    def get_all_job_details(self) -> list[dict]:
        """Returns position, department, and location for each job posting."""
        postings = self.driver.find_elements(*L.leverPage_jobItems_list)
        jobs = []
        for posting in postings:
            # Department header belongs to the parent .postings-group, not the posting itself.
            # Location uses textContent to bypass CSS text-transform:uppercase.
            data = self.driver.execute_script("""
                var p = arguments[0];
                var group = p.closest('.postings-group');
                var dept = group ? group.querySelector('h4,h3,[class*=category]') : null;
                return {
                    position:   (p.querySelector('h5') || {}).textContent || '',
                    department: (dept || {}).textContent || '',
                    location:   (p.querySelector('.location') || {}).textContent || ''
                };
            """, posting)
            jobs.append({k: v.strip() for k, v in data.items()})
        logger.info(
            "Postings found: %d → %s",
            len(jobs),
            [(j["position"][:40], j["location"]) for j in jobs],
        )
        return jobs
