from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
)
from SeleniumHelpers import wait_and_click, wait_and_send_keys

class KahootBot:
    def __init__(self, driver, username, password, title, quiz_data, debug=False):
        self.driver = driver  # Use the provided driver
        self.username = username
        self.password = password
        self.title = title
        self.quiz_data = quiz_data
        self.debug = debug
        self.wait = WebDriverWait(self.driver, 10)

    def debug_print(self, message):
        """Prints debug messages only if debug mode is enabled."""
        if self.debug:
            print(message)

    def open_login_page(self):
        """Opens the Kahoot login page."""
        self.driver.get("https://create.kahoot.it/auth/login")

    def login(self):
        """Logs in to Kahoot with the provided username and password."""
        self.open_login_page()
        wait_and_click(self.driver, By.XPATH, '//button[text()="Accept all cookies"]')
        wait_and_send_keys(self.driver, By.ID, "username", self.username + Keys.ENTER)
        wait_and_send_keys(self.driver, By.ID, "password", self.password + Keys.ENTER)
        self.wait.until(EC.title_is("Kahoot!"))
        self.debug_print("Login successful.")

    def create_quiz(self):
        """Creates a quiz using the provided quiz data."""
        self.driver.get("https://create.kahoot.it/creator")
        wait_and_click(self.driver, By.XPATH, '//div[@data-cta="blank"]')

        for idx, question in enumerate(self.quiz_data):
            self.debug_print(f"Adding question {idx + 1}: {question}")
            wait_and_send_keys(self.driver, By.CSS_SELECTOR, "p[data-placeholder='Start typing your question']",
                                    question["Question"][:120] + Keys.ENTER)

            answers = question["Answers"]
            for i in range(len(answers)):
                wait_and_send_keys(self.driver, By.ID, f"question-choice-{i}", answers[i])

            wait_and_click(self.driver, By.XPATH, f'//button[@aria-label="Toggle answer {question["Correct"] + 1} correct."]',
                                retries=3)

            if idx < 14:  # Only add "Add question" buttons for the first 14 questions
                wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="add-question-button"]')
                wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="create-button__quiz"]')

    def save_quiz(self):
        """Saves the quiz with the provided title."""
        wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="top-bar__save-button"]')
        wait_and_send_keys(self.driver, By.ID, "kahoot-title", self.title + Keys.ENTER)
        wait_and_click(self.driver, By.CSS_SELECTOR, 'button[data-functional-selector="dialog-add-title__continue"]')
        self.debug_print("Quiz saved successfully.")

    def run(self):
        """Executes the full sequence: login, create quiz, and save."""
        self.login()
        self.create_quiz()
        self.save_quiz()  # Replace with desired title

    def close(self):
        """Closes the WebDriver."""
        self.driver.quit()
