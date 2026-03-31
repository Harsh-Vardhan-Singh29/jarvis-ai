from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import os
from utils.logger import log

driver = None


# ====================================
# CREATE DRIVER
# ====================================
def create_driver():
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")

    # reduce automation detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument("--disable-infobars")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--disable-session-crashed-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")

    # persistent whatsapp login profile
    profile_path = os.path.abspath("whatsapp_profile")

    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    options.add_argument(f"--user-data-dir={profile_path}")

    service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


# ====================================
# GET DRIVER (SAFE VERSION)
# ====================================
def get_driver():
    global driver

    try:
        if driver is None:
            driver = create_driver()

        # check if session still alive
        driver.title

    except WebDriverException:
        log("WebDriverException caught, creating new driver instance.")
        try:
            driver.quit()
        except:
            pass

        driver = create_driver()

    return driver


# ====================================
# RESET DRIVER MANUALLY
# ====================================
def reset_driver():
    global driver

    try:
        if driver:
            driver.quit()
    except:
        pass

    driver = None