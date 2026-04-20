import pytest
import allure

from ui_tests.flows.site_flow import SiteFlow
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.careers_page import CareersPage
from ui_tests.data.expected_content import (
    EXPECTED_JOB_POSITION_KEYWORDS,
    EXPECTED_JOB_LOCATION,
    EXPECTED_LEVER_APPLY_URL_FRAGMENT,
)


@allure.parent_suite("UI Tests")
@allure.suite("Insider Careers")
class TestInsiderCareers:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Before each test: open your browser, go to the homepage, and close the cookie banner."""
        self.driver = driver
        self.flow = SiteFlow(driver)
        self.home = HomePage(self.driver)
        self.home.open()
        self.flow.handle_cookie_banner()

    @pytest.mark.regression
    def test_02_careers_page_is_opened_and_loaded(self):
        """
        Step 2: Navigate to the Careers page and verify it is opened
        with department content blocks loaded.
        """
        self.home.go_to_careers()

        careers = CareersPage(self.driver)

        assert careers.is_on_correct_page(), (
            f"Expected URL to contain '{careers.PAGE_URL}', got: {careers.get_current_url()}"
        )
        assert careers.is_page_loaded(), "Careers page department section is not visible"

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_03_qa_jobs_listed(self):
        """
        Step 3: Click 'See all teams', navigate to Quality Assurance open positions
        and verify the job list is present.
        """
        job_page = self.flow.navigate_to_qa_jobs(self.home)

        assert job_page.is_on_correct_page(), (
            f"Expected Lever job board, got: {job_page.get_current_url()}"
        )
        assert job_page.is_job_list_present(), (
            "Quality Assurance job listings are not visible on Lever job board"
        )

    @pytest.mark.regression
    def test_04_all_qa_job_details_are_correct(self):
        """
        Step 4: On the QA jobs page, verify ALL listed jobs contain
        'Quality Assurance' (or 'QA') in position and 'Istanbul' in location.
        """
        job_page = self.flow.navigate_to_qa_jobs(self.home)
        job_page.select_istanbul_location()

        jobs = job_page.get_all_job_details()
        assert len(jobs) > 0, "No jobs found for Quality Assurance in Istanbul"

        for job in jobs:
            assert any(kw in job["position"] for kw in EXPECTED_JOB_POSITION_KEYWORDS), (
                f"Position '{job['position']}' does not contain any of"
                f" {EXPECTED_JOB_POSITION_KEYWORDS}"
            )
            assert EXPECTED_JOB_LOCATION in job["location"], (
                f"Location '{job['location']}' does not contain '{EXPECTED_JOB_LOCATION}'"
            )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_05_apply_button_redirects_to_lever_form(self):
        """
        Step 5: Click the 'Apply' button on the first QA job listing
        and verify the browser redirects to the Lever application form.
        """
        job_page = self.flow.navigate_to_qa_jobs(self.home)

        job_page.click_first_apply_button()

        assert EXPECTED_LEVER_APPLY_URL_FRAGMENT in job_page.get_current_url(), (
            f"Expected Lever apply form URL containing '{EXPECTED_LEVER_APPLY_URL_FRAGMENT}', "
            f"got: {job_page.get_current_url()}"
        )
