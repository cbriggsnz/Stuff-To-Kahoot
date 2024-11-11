# bot_helpers.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from datetime import datetime
import logging

def wait_and_click(driver, locator_type, locator_value, timeout=10, retries=3, debug=False):
    """Waits for an element to be clickable and clicks it, with retries."""
    wait = WebDriverWait(driver, timeout)
    for attempt in range(retries):
        try:
            element = wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
            element.click()
            logging.info(f"Clicked element with {locator_type}='{locator_value}' successfully.")
            return
        except ElementClickInterceptedException:
            logging.warning(f"Click intercepted, retrying... (Attempt {attempt + 1})")
            wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference, re-locating element... (Attempt {attempt + 1})")
            wait.until(EC.presence_of_element_located((locator_type, locator_value)))
    logging.error(f"Element with {locator_type}='{locator_value}' was not found or clickable after {retries} attempts.")

def wait_and_send_keys(driver, locator_type, locator_value, text, timeout=10, debug=False):
    """Waits for an element to be visible and sends keys to it."""
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.visibility_of_element_located((locator_type, locator_value)))
        element.send_keys(text)
        #logging.info(f"Text '{text}' sent to element with {locator_type}='{locator_value}' successfully.")
    except Exception as e:
        logging.warning(f"Failed to send text to element with {locator_type}='{locator_value}': {e}")


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

            logging.info(f"Clicked the {locator_value} element successfully.")
            return True
        except TimeoutException:
            logging.warning(f"Timeout: Element {locator_value} not clickable after waiting. Retries left: {retries - attempt - 1}")
        except StaleElementReferenceException:
            logging.warning("Stale element reference encountered. Retrying...")

    # Final failure message if all retries are exhausted
    logging.error(f"Failed to locate and click the element {locator_value} after {retries} retries.")
    return False


def get_image_url(driver, locator_type, locator_value):
    """Retrieve the image URL from an <img> tag located by the selector."""
    try:
        # Locate the <img> element
        img_element = driver.find_element(locator_type, locator_value)
        # Get the src attribute (image URL)
        image_url = img_element.get_attribute("src")
        return image_url
    except Exception as e:
        logging.warning(f"Could not retrieve the image URL: {e}")
        return None