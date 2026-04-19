from selenium.webdriver.common.by import By

from ui_tests.locators.locator import Locator


class CareersPageLocators:
    # ── Page verification ────────────────────────────────────────────────────
    careersPage_departmentCards_section = Locator(By.CSS_SELECTOR, ".insiderone-icon-cards-grid")

    # ── Department cards ─────────────────────────────────────────────────────
    careersPage_seeAllTeams_btn         = Locator(By.CSS_SELECTOR, "a.inso-btn.see-more")
    careersPage_qaOpenPositions_btn     = Locator(
        By.CSS_SELECTOR, "a[href*='lever.co'][href*='Quality']"
    )
