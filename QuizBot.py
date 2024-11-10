from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchFrameException, TimeoutException,
    StaleElementReferenceException, ElementNotInteractableException
)

class QuizBot:
    def __init__(self, driver, url, username, password, debug=False):
        self.driver = driver  # Use the provided driver
        self.url = url
        self.username = username
        self.password = password
        self.debug = debug
        self.wait = WebDriverWait(self.driver, 10)

    def debug_print(self, message):
        """Prints debug messages only if debug mode is enabled."""
        if self.debug:
            print(message)

    def open_quiz_page(self):
        """Open the specified quiz page URL."""
        self.driver.get(self.url)

    def find_iframe_by_class(self, class_name, retries=3):
        """Locate and click a button inside an iframe by class name with retries."""
        # Wait until iframes are present on the page
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        button_clicked = False
        while retries > 0:
            # Refresh the list of iframes each retry
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            self.debug_print(f"Found {len(iframes)} iframes on this retry. {retries} retries left.")

            for index, iframe in enumerate(iframes):
                try:
                    # Switch to the iframe
                    self.driver.switch_to.frame(iframe)

                    # Attempt to find the button by class name
                    button = self.driver.find_element(By.CLASS_NAME, class_name)

                    # Try clicking the button
                    try:
                        button.click()
                        self.debug_print(f"Clicked button in iframe {index + 1}")
                        button_clicked = True
                        break  # Exit the loop if the button is clicked successfully
                    except ElementNotInteractableException:
                        self.debug_print("Button found but not interactable. Retrying...")

                except (NoSuchElementException, TimeoutException):
                    self.debug_print(f"{class_name} button not found in iframe {index + 1}, moving to next iframe.")
                    self.driver.switch_to.default_content()
                except (NoSuchFrameException, StaleElementReferenceException):
                    self.debug_print(f"Iframe {index + 1} became stale or inaccessible, retrying.")
                    self.driver.switch_to.default_content()

            if button_clicked:
                break
            else:
                retries -= 1
                self.driver.switch_to.default_content()

        if not button_clicked:
            self.debug_print("Button not found in any iframe after all retries.")

    def login(self):
        """Logs in using provided credentials."""
        email_field = self.wait.until(EC.element_to_be_clickable((By.ID, "signInName")))
        email_field.send_keys(self.username, Keys.ENTER)

        password_field = self.wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_field.send_keys(self.password, Keys.ENTER)

    def get_quiz_title(self):
        quiz_title = ""
        try:
            # Wait for the <h1> element with the quiz title to be present
            h1_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".stuff-box.stuff-article-header h1"))
            )
            # Get the text of the <h1> element
            # quiz_title = h1_element.text
            # print(f"Quiz title: {quiz_title}")
            quiz_title = h1_element.text

        except Exception as e:
            print("Could not find the quiz title:", e)

        return quiz_title

    def gather_quiz_data(self):
        """Collect quiz data by interacting with each question."""
        quiz_list = []
        question_number = 1  # Track question count

        while question_number <= 15:  # Repeat until all 15 questions are completed
            self.debug_print(f"Processing question {question_number}")

            # Attempt to click the ".choice" button to select an answer
            if not self.click_with_retry((By.CSS_SELECTOR, ".choice")):
                self.debug_print("Unable to click on a choice button. Exiting current question loop.")
                break  # Exit if unable to click any choice button

            # Gather answers if selection was successful
            buttons = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".choice-title")))
            question_dict = {}
            answer_list = []
            for index, b in enumerate(buttons):
                correct = b.find_elements(By.CSS_SELECTOR, ".correct")
                # question_dict[f"Answer {index}"] = b.text
                answer_list.append(b.text)
                if correct:
                    question_dict["Correct"] = index
            question_dict["Answers"] = answer_list
            # Retrieve question text
            question_text = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text
            question_dict["Question"] = question_text



            self.debug_print(f"Collected question data: {question_dict}")

            # Add question dictionary to quiz_list
            if "Correct" in question_dict:
                quiz_list.append(question_dict)
            else:
                self.debug_print("No correct answer found. Reattempting question.")
                continue

            # Attempt to click "Next" button if it exists; exit if click fails
            if not self.click_with_retry((By.XPATH, '//button[text()="Next"]')):
                self.debug_print("Unable to click 'Next' button. Exiting loop.")
                break

            # Move to the next question only if "Next" was successfully clicked
            question_number += 1

        return quiz_list

    def click_with_retry(self, locator, retries=3):
        """Attempt to click an element with retries, ensuring presence and visibility."""
        while retries > 0:
            try:
                # First, ensure the element is present
                self.wait.until(EC.presence_of_element_located(locator))

                # Then, check if it is clickable and try clicking it
                button = self.wait.until(EC.element_to_be_clickable(locator))
                button.click()
                self.debug_print(f"Clicked the {locator} element successfully.")
                return True
            except TimeoutException:
                self.debug_print(f"Timeout: Element {locator} not clickable after waiting. Retries left: {retries - 1}")
                retries -= 1
                if retries == 0:
                    self.debug_print(f"Failed to locate and click the element {locator} after multiple retries.")
                    return False
            except StaleElementReferenceException:
                self.debug_print("Stale element reference encountered. Retrying...")
                retries -= 1

    def run_quiz(self):
        """Complete the quiz process from start to finish."""
        self.open_quiz_page()
        self.find_iframe_by_class("stuff-button", retries=16)
        self.driver.switch_to.default_content()
        self.login()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Stuff quiz"))
        quiz_title = self.get_quiz_title()
        self.find_iframe_by_class("block-nav", retries=16)
        quiz_data = self.gather_quiz_data()
        quiz = {"Title" : quiz_title, "Quiz_Data" : quiz_data}
        return quiz


    def close(self):
        """Close the WebDriver."""
        self.driver.quit()

