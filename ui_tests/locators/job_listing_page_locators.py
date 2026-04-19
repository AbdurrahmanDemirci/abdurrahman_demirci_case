from selenium.webdriver.common.by import By

from ui_tests.locators.locator import Locator


class JobListingPageLocators:
    # ── Job listings (Lever hosted job board) ───────────────────────────────
    leverPage_jobItems_list = Locator(By.CSS_SELECTOR, ".postings-group .posting")
