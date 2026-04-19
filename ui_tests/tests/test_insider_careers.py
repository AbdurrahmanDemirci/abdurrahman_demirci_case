import pytest

from ui_tests.flows.site_flow import SiteFlow
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.careers_page import CareersPage
from ui_tests.data.expected_content import (
    EXPECTED_JOB_DEPARTMENT,
    EXPECTED_JOB_POSITION_KEYWORDS,
    EXPECTED_JOB_LOCATION,
)


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
    def test_04_first_qa_job_details_are_correct(self):
        """
        Step 4: On the QA jobs page, verify the first listed job contains
        'Quality Assurance' (or 'QA') in its position, 'Quality Assurance'
        in its department, and 'Istanbul' in its location.
        """
        job_page = self.flow.navigate_to_qa_jobs(self.home)

        jobs = job_page.get_all_job_details()
        assert len(jobs) > 0, "No jobs found on the Quality Assurance page"

        first = jobs[0]

        assert any(kw in first["position"] for kw in EXPECTED_JOB_POSITION_KEYWORDS), (
            f"Position '{first['position']}' does not contain any of"
            f" {EXPECTED_JOB_POSITION_KEYWORDS}"
        )
        assert EXPECTED_JOB_DEPARTMENT in first["department"], (
            f"Department '{first['department']}' does not contain '{EXPECTED_JOB_DEPARTMENT}'"
        )
        assert EXPECTED_JOB_LOCATION in first["location"], (
            f"Location '{first['location']}' does not contain '{EXPECTED_JOB_LOCATION}'"
        )
