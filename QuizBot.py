from http.cookiejar import debug

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchFrameException, TimeoutException,
    StaleElementReferenceException, ElementNotInteractableException
)
from SeleniumHelpers import wait_and_click, wait_and_send_keys, click_with_retry, debug_print, get_image_url
from datetime import datetime

class QuizBot:
    def __init__(self, driver, url, username, password, debug=False):
        self.driver = driver  # Use the provided driver
        self.url = url
        self.username = username
        self.password = password
        self.debug = debug
        self.wait = WebDriverWait(self.driver, 10)

    def open_quiz_page(self):
        """Open the specified quiz page URL."""
        self.driver.get(self.url)

    def find_iframe_by_class(self, class_name, retries=3):
        """Locate and click a button inside an iframe by class name with retries."""
        # Wait until iframes are present on the page
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        button_clicked = False
        for attempt in range(retries):
            # Refresh the list of iframes each retry
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            debug_print(f"Found {len(iframes)} iframes on this retry. {retries} retries left.")

            for index, iframe in enumerate(iframes):
                try:
                    # Switch to the iframe
                    self.driver.switch_to.frame(iframe)
                    button = self.driver.find_element(By.CLASS_NAME, class_name)

                    # Try clicking the button
                    if button and click_with_retry(self.driver, By.CLASS_NAME, class_name, debug=self.debug):
                        debug_print(f"Clicked button in iframe {index + 1}")
                        button_clicked = True
                        break

                except (NoSuchElementException, TimeoutException, NoSuchFrameException, StaleElementReferenceException):
                    debug_print(f"Error accessing button in iframe {index + 1}. Retrying next iframe.")
                    self.driver.switch_to.default_content()

            if button_clicked:
                break
            else:
                self.driver.switch_to.default_content()

        if not button_clicked:
            debug_print("Button not found in any iframe after all retries.")

    def login(self):
        """Logs in using provided credentials."""
        wait_and_send_keys(self.driver, By.ID, "signInName", self.username + Keys.ENTER, debug=self.debug)
        wait_and_send_keys(self.driver, By.ID, "password", self.password + Keys.ENTER, debug=self.debug)

    def get_quiz_title(self):
        quiz_title = ""
        try:
            # Wait for the <h1> element with the quiz title to be present
            h1_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".stuff-box.stuff-article-header h1"))
            )

            quiz_title = h1_element.text

        except Exception as e:
            debug_print("Could not find the quiz title:", e)

        return quiz_title


    def gather_quiz_data(self):
        """Collect quiz data by interacting with each question."""
        quiz_list = []
        question_number = 1  # Track question count

        while question_number <= 15:  # Repeat until all 15 questions are completed
            debug_print(f"Processing question {question_number}")

            image_url = get_image_url(self.driver, By.CSS_SELECTOR, "div.image-embed img.img")

            debug_print(f"Image URL = {image_url}")

            # Attempt to click the ".choice" button to select an answer
            if not click_with_retry(self.driver, By.CSS_SELECTOR, ".choice", debug=self.debug):
                debug_print("Unable to click on a choice button. Exiting current question loop.")
                break  # Exit if unable to click any choice button

            # Gather answers if selection was successful
            buttons = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".choice-title")))
            answer_list, correct_answer = [], None

            for index, button in enumerate(buttons):
                answer_text = button.text
                answer_list.append(answer_text)
                if button.find_elements(By.CSS_SELECTOR, ".correct"):
                    correct_answer = index

            question_text = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text
            question_dict = {"Question": question_text, "Answers": answer_list, "Correct": correct_answer}

            debug_print(f"Collected question data: {question_dict}")

            # Add question dictionary to quiz_list
            if correct_answer is not None:
                quiz_list.append(question_dict)
            else:
                debug_print("No correct answer found. Reattempting question.")
                continue

            # Attempt to click "Next" button if it exists; exit if click fails
            if not click_with_retry(self.driver, By.XPATH, '//button[text()="Next"]', debug=self.debug):
                debug_print("Unable to click 'Next' button. Exiting loop.")
                break

            # Move to the next question only if "Next" was successfully clicked
            question_number += 1

        return quiz_list

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

