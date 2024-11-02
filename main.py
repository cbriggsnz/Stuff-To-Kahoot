
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

options = webdriver.ChromeOptions()

options.page_load_strategy = 'eager'
options.add_experimental_option("detach", True)  # Option to keep Chrome open

driver = webdriver.Chrome(options = options)
#
driver.get("https://www.stuff.co.nz/quizzes/350407318/stuff-quiz-morning-trivia-challenge-october-29-2024")

# Wait for the page to load
time.sleep(3)

# Get all iframe elements on the page



def find_iframe_by_class(class_name: str):
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    button_clicked = False
    # Iterate through each iframe
    for index, iframe in enumerate(iframes):
        try:
            # Switch to the iframe
            driver.switch_to.frame(iframe)
            # Try to find the button with the specified text
            button = driver.find_element(By.CLASS_NAME, class_name)
            button.click()
            print(f"Clicked button in iframe {index + 1}")
            button_clicked = True
            break  # Exit loop if the button is found and clicked

        except NoSuchElementException:
            # print(f"Button not found in iframe {index + 1}")
            # Switch back to the default content to continue to the next iframe
            driver.switch_to.default_content()

        except NoSuchFrameException:
            pass
            # print(f"Could not switch to iframe {index + 1}")

    # Switch back to the main content if no button was clicked
    if not button_clicked:
        driver.switch_to.default_content()
        print(f"Button not found in any iframe")

find_iframe_by_class("stuff-button")
time.sleep(3)

driver.switch_to.default_content()


email_address = driver.find_element(By.ID, value = "signInName")
email_address.send_keys("cbriggsnz1977@gmail.com", Keys.ENTER)

password = driver.find_element(By.ID, value = "password")
password.send_keys("?NtLdRR8NQQff$3g", Keys.ENTER)

time.sleep(6)

# print(driver.page_source)
def wait_for_iframe_and_switch(iframe_locator, timeout=20):
    try:
        # Wait for the iframe to be present
        iframe = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, iframe_locator)))

        # Switch to the iframe
        return iframe

    except TimeoutException:
        print("Iframe not found within the given time.")
        return None

def wait_for_load(condition, element):
    elem = None
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((condition, element)) #This is a dummy element
        )

    finally:
        return elem

find_iframe_by_class("block-nav")

quiz_list = []

wait = WebDriverWait(driver, 10)


# Define a helper function to handle clicking with retry logic
def click_with_retry(driver, locator, retries=3):
    while retries > 0:
        try:
            # Wait for the element to be clickable and click it
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
            button.click()
            return True
        except StaleElementReferenceException:
            retries -= 1
            if retries == 0:
                print(f"Failed to locate and click the element {locator} after multiple retries.")
    return False


wait = WebDriverWait(driver, 10)

for i in range(15):
    # Click the ".choice" button with retry logic
    if not click_with_retry(driver, (By.CSS_SELECTOR, ".choice")):
        print("Skipping to next iteration due to unrecoverable click error.")
        continue  # Move to the next iteration if click fails

    # Wait for ".choice-title" elements to be present
    buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".choice-title")))

    # Gather question and answers into a dictionary
    question_dict = {}
    for idx, b in enumerate(buttons):
        index = idx + 1
        correct = b.find_elements(By.CSS_SELECTOR, ".correct")
        question_dict[f"Answer {index}"] = b.text
        if correct:  # Non-empty list implies correctness
            question_dict["Correct"] = index

    # Wait for the question title to load and retrieve its text
    question_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text
    question_dict["Question"] = question_text

    # Print and append the question dictionary to the quiz list
    print(question_dict)
    quiz_list.append(question_dict)

    # Click the "Next" button with retry logic to ensure smooth transition
    if not click_with_retry(driver, (By.XPATH, '//button[text()="Next"]')):
        print("Encountered issue clicking 'Next' button. Exiting loop.")
        break  # Stop the loop if the "Next" button fails

print(quiz_list)
