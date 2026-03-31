import threading
import time

from core.browser import driver
from utils.logger import log


CHECK_INTERVAL = 60


def monitor_driver():
    """
    Monitor selenium driver health without creating it.
    """

    global driver

    while True:

        try:
            # Only check if driver already exists
            if driver:

                driver.title   # health check

        except Exception:

            log("Browser session died. Resetting driver.")

            try:
                driver.quit()
            except:
                pass

            driver = None

        time.sleep(CHECK_INTERVAL)


def start_driver_monitor():

    thread = threading.Thread(
        target=monitor_driver,
        daemon=True
    )

    thread.start()

    log("Driver monitor started.")