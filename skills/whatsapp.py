from core.browser import get_driver
from voice.speak import speak
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, logging
from core.tab_manager import register_tab, get_tab
from utils.logger import log



driver = None
current_contact = None


def sanitize_text(text: str):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)


# ====================================
# OPEN WHATSAPP
# ====================================

def open_whatsapp():
    driver = get_driver()

    existing = get_tab("whatsapp")

    # If WhatsApp tab already exists → switch to it
    if existing and existing in driver.window_handles:
        driver.switch_to.window(existing)
        return "WhatsApp already open."

    # Open NEW tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    # Load WhatsApp
    driver.get("https://web.whatsapp.com")

    # Register tab in manager
    register_tab("whatsapp", driver.current_window_handle)

    # Wait for WhatsApp UI
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        )
    )

    return "WhatsApp opened."


# ====================================
# OPEN CHAT
# ====================================
def open_chat(contact_name):
    global current_contact
    current_contact = contact_name
    global driver
    driver = get_driver()

    try:
        log(f"Attempting to open chat for '{contact_name}'")

        # 1. Wait for the search box
        search_box = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        
        # Click to focus
        search_box.click()
        time.sleep(0.5)

        # Clear the box (Select All -> Backspace)
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)

        # 2. Type the voice command (WhatsApp handles case automatically!)
        search_box.send_keys(contact_name)
        log(f"Typed '{contact_name}' into search box.")

        # 3. CRITICAL: Wait 3 seconds for WhatsApp to search and show the list
        time.sleep(3)

        # 4. THE MAGIC: Use Keyboard Navigation
        # Instead of hunting for complex HTML to click, we just hit ENTER. 
        # In WhatsApp Web, hitting ENTER in the search box opens the first matching chat.
        search_box.send_keys(Keys.ENTER)
        
        # Backup: If just ENTER doesn't trigger it, sometimes it needs an Arrow Down first
        # search_box.send_keys(Keys.ARROW_DOWN)
        # time.sleep(0.5)
        # search_box.send_keys(Keys.ENTER)

        print(f"SUCCESS: Opened chat for '{contact_name}' using keyboard navigation.")
        
        # Wait 2 seconds for the chat right-panel to open before moving on
        time.sleep(2) 
        return True

    except Exception as e:
        print(f"CHAT ERROR: {e}")
        return False



# ====================================
# SEND MESSAGE
# ====================================

def send_message(message):
    global driver, current_contact

    if not driver:
        return "WhatsApp not open."

    try:
        msg_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//footer//div[@contenteditable='true']")
            )
        )

        msg_box.click()
        msg_box.send_keys(sanitize_text(message))
        msg_box.send_keys(Keys.ENTER)

        speak(f"Message sent to {current_contact}")

        log(f"Message sent successfully to {current_contact}")

        return "Message sent."

    except Exception as e:
        logging.exception("SEND ERROR: %s", e)
        close_whatsapp()
        return "Failed to send message."


# ====================================
# CLOSE WHATSAPP
# ====================================

def close_whatsapp():
    global driver

    try:
        if driver:
            log("Closing WhatsApp tab.")
            driver.close()
    except Exception as e:
        log(f"CLOSE ERROR: {e}")

    driver = None
