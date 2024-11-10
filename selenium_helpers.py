# bot_helpers.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

def wait_and_click(driver, locator_type, locator_value, timeout=10, retries=3, debug=False):
    """Waits for an element to be clickable and clicks it, with retries."""
    wait = WebDriverWait(driver, timeout)
    for attempt in range(retries):
        try:
            element = wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
            element.click()
            if debug:
                print(f"Clicked element with {locator_type}='{locator_value}' successfully.")
            return
        except ElementClickInterceptedException:
            if debug:
                print(f"Click intercepted, retrying... (Attempt {attempt + 1})")
            wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
        except StaleElementReferenceException:
            if debug:
                print(f"Stale element reference, re-locating element... (Attempt {attempt + 1})")
            wait.until(EC.presence_of_element_located((locator_type, locator_value)))
    if debug:
        print(f"Element with {locator_type}='{locator_value}' was not found or clickable after {retries} attempts.")

def wait_and_send_keys(driver, locator_type, locator_value, text, timeout=10, debug=False):
    """Waits for an element to be visible and sends keys to it."""
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.visibility_of_element_located((locator_type, locator_value)))
        element.send_keys(text)
        if debug:
            print(f"Text '{text}' sent to element with {locator_type}='{locator_value}' successfully.")
    except Exception as e:
        if debug:
            print(f"Failed to send text to element with {locator_type}='{locator_value}': {e}")
