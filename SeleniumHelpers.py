# bot_helpers.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from datetime import datetime

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


def click_with_retry(driver, locator_type, locator_value, timeout=10, retries=3, debug=False):
    """Attempt to click an element with retries, ensuring presence and visibility."""
    wait = WebDriverWait(driver, timeout)
    for attempt in range(retries):
        try:
            # Ensure the element is present
            wait.until(EC.presence_of_element_located((locator_type, locator_value)))

            # Check if it is clickable and attempt to click
            button = wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
            button.click()

            if debug:
                print(f"Clicked the {locator_value} element successfully.")
            return True
        except TimeoutException:
            if debug:
                print(f"Timeout: Element {locator_value} not clickable after waiting. Retries left: {retries - attempt - 1}")
        except StaleElementReferenceException:
            if debug:
                print("Stale element reference encountered. Retrying...")

    # Final failure message if all retries are exhausted
    if debug:
        print(f"Failed to locate and click the element {locator_value} after {retries} retries.")
    return False


def debug_print(message, debug=False):
    """Prints debug messages only if debug mode is enabled, with a timestamp."""
    if debug:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

def get_image_url(driver, locator_type, locator_value):
    """Retrieve the image URL from an <img> tag located by the selector."""
    try:
        # Locate the <img> element
        img_element = driver.find_element(locator_type, locator_value)
        # Get the src attribute (image URL)
        image_url = img_element.get_attribute("src")
        return image_url
    except Exception as e:
        print("Could not retrieve the image URL:", e)
        return None