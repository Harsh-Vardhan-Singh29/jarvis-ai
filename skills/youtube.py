# skills/youtube.py

from core.state import state
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core.browser import get_driver
import threading
import time
from core.tab_manager import register_tab, get_tab
from utils.logger import log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


youtube_tab = None


# =========================
# OPEN YOUTUBE IN NEW TAB
# =========================
def open_youtube():
    global youtube_tab

    driver = get_driver()

    existing = get_tab("youtube")

    # check if stored tab died
    if youtube_tab and youtube_tab not in driver.window_handles:
        youtube_tab = None

    if existing and existing in driver.window_handles:
        youtube_tab = existing
        driver.switch_to.window(existing)
        return "YouTube already open."

    # open new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    driver.get("https://www.youtube.com")

    youtube_tab = driver.current_window_handle

    register_tab("youtube", youtube_tab)

    time.sleep(2)

    return "Opening YouTube."


# =========================
# SEARCH + PLAY VIDEO
# =========================

def play_video(query):

    driver = get_driver()

    yt_tab = get_tab("youtube")

    if not yt_tab or yt_tab not in driver.window_handles:
        open_youtube()
        yt_tab = get_tab("youtube")

    ensure_youtube_tab()

    wait = WebDriverWait(driver, 20)

    try:
        box = wait.until(
            EC.element_to_be_clickable((By.NAME, "search_query"))
        )

        box.clear()
        box.send_keys(query)
        box.send_keys(Keys.ENTER)

        video = wait.until(
            EC.element_to_be_clickable((By.ID, "video-title"))
        )

        video.click()

        return f"Playing {query} on YouTube."

    except Exception as e:
        log(f"YT ERROR: {e}")
        return "I couldn't play that video."


# =========================
# AUTO SKIP ADS
# =========================
def _auto_skip_ads():
    driver = get_driver()

    while True:
        try:
            skip_buttons = driver.find_elements(
                By.XPATH,
                '//button[contains(@class,"ytp-ad-skip-button") '
                'or contains(@class,"ytp-ad-skip-button-modern") '
                'or contains(@aria-label,"Skip")]'
            )

            if skip_buttons:
                skip_buttons[0].click()
                log("Ad skipped.")
                time.sleep(3)

        except:
            pass

        time.sleep(2)


# =========================
# PLAYER CONTROLS
# =========================
def _send_key(key):

    driver = get_driver()
    yt_tab = get_tab("youtube")

    if not yt_tab:
        return False

    ensure_youtube_tab()

    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(key)

    return True


# =========================
# PAUSE / PLAY VIDEO
# =========================
def pause_video():

    driver = get_driver()
    yt_tab = get_tab("youtube")

    if not yt_tab:
        return "YouTube is not open."

    ensure_youtube_tab()
    try:
        video = driver.find_element(By.TAG_NAME, "video")

        driver.execute_script("""
        if(arguments[0].paused){
            arguments[0].play();
        } else {
            arguments[0].pause();
        }
        """, video)

        return "Toggled play or pause."

    except Exception as e:
        log(f"YT CONTROL ERROR: {e}")
        return "I couldn't control the video."


# =========================
# FULLSCREEN
# =========================
def fullscreen():
    if _send_key("f"):
        return "Fullscreen mode."
    return "YouTube is not open."


# =========================
# MUTE
# =========================
def mute():
    if _send_key("m"):
        return "Muted."
    return "YouTube is not open."


# =========================
# NEXT VIDEO
# =========================
def next_video():

    from core.browser import get_driver
    from selenium.webdriver.common.by import By

    driver = get_driver()

    try:
        driver.switch_to.window(youtube_tab)

        video = driver.find_element(By.TAG_NAME, "video")

        video.click()  # focus the player

        driver.execute_script("""
        document.querySelector('video').dispatchEvent(
            new KeyboardEvent('keydown', {
                key: 'n',
                shiftKey: true
            })
        );
        """)

        return "Next video."

    except Exception as e:
        print("YT NEXT ERROR:", e)
        return "I couldn't play the next video."


# =========================
# VOLUME
# =========================
def volume_up():
    if _send_key(Keys.ARROW_UP):
        return "Volume up."
    return "YouTube is not open."


def volume_down():
    if _send_key(Keys.ARROW_DOWN):
        return "Volume down."
    return "YouTube is not open."



def start_watch_mode():

    from core.browser import get_driver
    from core.tab_manager import get_tab

    driver = get_driver()

    yt_tab = get_tab("youtube")

    if not yt_tab:
        return

    ensure_youtube_tab()

    while True:

        try:

            video = driver.find_element(By.TAG_NAME, "video")

            ended = driver.execute_script("return arguments[0].ended;", video)

            if ended:
                log("Video ended, moving to next.")

                next_btn = driver.find_element(By.CSS_SELECTOR, ".ytp-next-button")
                next_btn.click()

                time.sleep(5)

        except:
            pass

        time.sleep(5)
        
def ensure_youtube_tab():

    global youtube_tab

    driver = get_driver()

    if youtube_tab not in driver.window_handles:
        youtube_tab = None

    if not youtube_tab:
        open_youtube()

    driver.switch_to.window(youtube_tab)