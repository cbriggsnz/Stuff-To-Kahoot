from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
)
from SeleniumHelpers import wait_and_click, wait_and_send_keys, upload_image, wait_until_element_appears
import logging
import time
class KahootBot:
    def __init__(self, driver, username, password, title, quiz_data, debug=False):
        self.driver = driver  # Use the provided driver
        self.username = username
        self.password = password
        self.title = title
        self.quiz_data = quiz_data
        self.debug = debug
        self.wait = WebDriverWait(self.driver, 10)

    def open_login_page(self):
        """Opens the Kahoot login page."""
        self.driver.get("https://create.kahoot.it/auth/login")

    def login(self):
        """Logs in to Kahoot with the provided username and password."""
        self.open_login_page()
        wait_and_click(self.driver, By.XPATH, '//button[text()="Accept all cookies"]')
        wait_and_send_keys(self.driver, By.ID, "username", self.username + Keys.ENTER, mask_text=True)
        wait_and_send_keys(self.driver, By.ID, "password", self.password + Keys.ENTER, mask_text=True)
        self.wait.until(EC.title_is("Kahoot!"))
        logging.info("Login successful.")

    def upload_image_to_question(self, image_path):
        """Uploads an image to the current question."""
        wait_and_click(self.driver, By.CSS_SELECTOR,
                       '[data-functional-selector="media-library-info-view__add-media-button"]')
        wait_and_click(self.driver, By.CSS_SELECTOR, '[data-functional-selector="open-upload-media-dialog-button"]')
        upload_image(self.driver, By.CSS_SELECTOR, "input[type='file']#media-upload", image_path)

        # Wait until the image upload completes
        upload_complete_selector = '[data-functional-selector="media-details__with-media"]'
        if wait_until_element_appears(self.driver, By.CSS_SELECTOR, upload_complete_selector):
            logging.info("Image upload completed successfully.")
        else:
            logging.warning("Image upload did not complete within the expected time.")

    def create_quiz(self):
        """Creates a quiz using the provided quiz data."""
        self.driver.get("https://create.kahoot.it/creator")
        wait_and_click(self.driver, By.XPATH, '//div[@data-cta="blank"]')

        for idx, question in enumerate(self.quiz_data):
            if idx > 0:  # Only add "Add question" buttons for the first 14 questions

                if question["Type"] == "text-entry":
                    logging.info(f"Skipping text-entry question {idx + 1}")
                    continue
                wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="add-question-button"]')

                wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="create-button__quiz"]')

                    #wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="create-button__open-ended"]')

            logging.info(f"Adding question {idx + 1}: {question}")

            wait_and_send_keys(self.driver, By.CSS_SELECTOR, "p[data-placeholder='Start typing your question']",
                                    question["Question"][:120] + Keys.ENTER)

            answers = question["Answers"]
            for i in range(len(answers)):
                wait_and_send_keys(self.driver, By.ID, f"question-choice-{i}", answers[i])

            wait_and_click(self.driver, By.XPATH, f'//button[@aria-label="Toggle answer {question["Correct"] + 1} correct."]',
                    retries=3)

            self.upload_image_to_question(f"Images/Image {idx + 1}.webp")

    def save_quiz(self):
        """Saves the quiz with the provided title."""
        wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="top-bar__save-button"]')
        wait_and_send_keys(self.driver, By.ID, "kahoot-title", self.title + Keys.ENTER)
        wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="dialog-add-title__continue"]')
        logging.info("Quiz saved successfully.")

    def run(self):
        """Executes the full sequence: login, create quiz, and save."""
        self.login()
        self.create_quiz()
        self.save_quiz()  # Replace with desired title

