# bot_helpers.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from datetime import datetime
import logging
import requests
import os
import time

def wait_and_click(driver, locator_type, locator_value, timeout=10, retries=3):
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

def wait_and_send_keys(driver, locator_type, locator_value, text, timeout=10, mask_text=False):
    """Waits for an element to be visible and sends keys to it."""
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.visibility_of_element_located((locator_type, locator_value)))
        element.send_keys(text)
        # cleaned_text = text.replace(Keys.ENTER, "") if Keys.ENTER in text else text
        display_text = "[HIDDEN]" if mask_text else text.replace(Keys.ENTER, "") if Keys.ENTER in text else text

        logging.info(f"Text '{display_text}' sent to element with {locator_type}='{locator_value}' successfully.")
    except Exception as e:
        logging.warning(f"Failed to send text to element with {locator_type}='{locator_value}': {e}")


def click_with_retry(driver, locator_type, locator_value, timeout=10, retries=3):
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
        except ElementClickInterceptedException as e:
            logging.warning("Element click intercepted")

    # Final failure message if all retries are exhausted
    logging.error(f"Failed to locate and click the element {locator_value} after {retries} retries.")
    return False


# def get_image_url(driver, locator_type, locator_value):
#     """Retrieve the image URL from an <img> tag located by the selector."""
#     try:
#         # Locate the <img> element
#         img_element = driver.find_element(locator_type, locator_value)
#         # Get the src attribute (image URL)
#         image_url = img_element.get_attribute("src")
#         return image_url
#     except Exception as e:
#         logging.warning(f"Could not retrieve the image URL: {e}")
#         return None


def get_image_url(driver, locator_type, locator_value):
    """Retrieve the image URL from an <img> tag located by the selector."""
    try:
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((locator_type, locator_value))
        )
        # Locate the <img> element
        img_element = driver.find_element(locator_type, locator_value)
        # Get the src attribute (image URL)
        image_url = img_element.get_attribute("src")

        if image_url:
            return image_url
        else:

            logging.warning("Image src attribute is missing.")
            return None
    except NoSuchElementException:
        logging.warning(f"Image element with selector '{locator_value}' not found.")
        return None

def save_image_from_url(url, save_dir=".", file_name=None):
    """Download and save an image from a URL, optionally saving it with a specific name.

    Args:
        url (str): The URL of the image to download.
        save_dir (str): The directory where the image should be saved (default is the current directory).
        file_name (str): Optional. The name to save the image as. If no extension is provided, the original extension from the URL is used.

    Returns:
        str: The full path to the saved image if successful, None otherwise.
    """
    try:
        # Check if the URL is None or empty
        if not url:
            logging.warning("No valid image URL provided. Skipping image save.")
            return None

        # Ensure the save directory exists
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        # Extract the original file extension from the URL
        original_extension = os.path.splitext(url)[1]

        # Use the original name if no custom file_name is provided
        if not file_name:
            file_name = os.path.basename(url)
        else:
            # Append the original extension if the file_name doesn't already have one
            if not os.path.splitext(file_name)[1]:
                file_name += original_extension

        # Construct the full path to save the image
        save_path = os.path.join(save_dir, file_name)

        # Download the image
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"Image saved to {save_path}")
            return save_path
        else:
            logging.error(f"Failed to retrieve the image. HTTP Status Code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while downloading the image: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def upload_image(driver, locator_type, locator_value, image_path):
    """Upload an image to the file input field."""
    image_path = os.path.abspath(image_path)
    try:
        # Locate the file input element and send the image path
        file_input = driver.find_element(locator_type, locator_value)
        file_input.send_keys(image_path)
        logging.info(f"Image uploaded from {image_path}")
    except Exception as e:
        logging.warning(f"Failed to upload image: {e}")

def wait_until_element_appears(driver, locator_type, locator_value, timeout=10):
    """Wait until an element appears on the page."""
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((locator_type, locator_value)))
        logging.info(f"Element with {locator_type}='{locator_value}' appeared.")
        return True
    except TimeoutException:
        logging.warning(f"Timed out waiting for element with {locator_type}='{locator_value}' to appear.")
        return False

def get_image_url_with_retry(driver, locator_type, locator_value, retries=3, delay=1):
    """Tries to retrieve the image URL, retrying if a StaleElementReferenceException occurs."""
    for attempt in range(retries):
        try:
            img_element = driver.find_element(locator_type, locator_value)
            image_url = img_element.get_attribute("src")
            return image_url
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference encountered. Retrying... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
    logging.error("Failed to retrieve image URL after retries.")
    return None