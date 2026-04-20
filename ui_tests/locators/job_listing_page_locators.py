from selenium.webdriver.common.by import By

from ui_tests.locators.locator import Locator


class JobListingPageLocators:
    # ── Job listings (Lever hosted job board) ───────────────────────────────
    leverPage_jobItems_list          = Locator(By.CSS_SELECTOR, ".postings-group .posting")
    leverPage_applyBtn               = Locator(By.CSS_SELECTOR, ".posting-btn-submit")
    leverPage_jobDetailApplyBtn      = Locator(By.CSS_SELECTOR, "a.postings-btn")
    # ── Location filter ──────────────────────────────────────────────────────
    leverPage_locationFilterBtn      = Locator(By.CSS_SELECTOR, "[aria-label='Filter by Location: All'] > .filter-button")
    leverPage_locationIstanbul       = Locator(By.XPATH, "//a[.='Istanbul']")
