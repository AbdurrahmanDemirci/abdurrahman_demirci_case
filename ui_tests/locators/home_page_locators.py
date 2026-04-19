from selenium.webdriver.common.by import By

from ui_tests.locators.locator import Locator


class HomePageLocators:
    homePage_cookieAccept_btn          = Locator(By.CSS_SELECTOR, "#wt-cli-accept-all-btn")
    homePage_cookieOnlyNecessary_btn   = Locator(By.CSS_SELECTOR, "#wt-cli-accept-btn")
    homePage_cookieDecline_btn         = Locator(By.CSS_SELECTOR, "#wt-cli-reject-btn")
    homePage_mainNavigation_container  = Locator(By.CSS_SELECTOR, "header")
    homePage_heroSection_section       = Locator(By.CSS_SELECTOR, ".homepage-hero")
    homePage_careersNavigation_link    = Locator(By.CSS_SELECTOR, "a[href='/careers/']")
