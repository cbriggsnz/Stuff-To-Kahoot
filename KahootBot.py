from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
)


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

    def wait_and_click(self, locator_type, locator_value, retries=3):
        """Clicks an element with retries to handle potential intercepts or staleness."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
                element.click()
                self.debug_print(f"Clicked element with {locator_type}='{locator_value}' successfully.")
                return
            except ElementClickInterceptedException:
                self.debug_print(f"Click intercepted, retrying... (Attempt {attempt + 1})")
                self.wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
            except StaleElementReferenceException:
                self.debug_print(f"Stale element reference, re-locating element... (Attempt {attempt + 1})")
                self.wait.until(EC.presence_of_element_located((locator_type, locator_value)))
        self.debug_print(
            f"Element with {locator_type}='{locator_value}' was not found or clickable after {retries} attempts.")

    def wait_and_send_keys(self, locator_type, locator_value, text):
        """Waits for an element and sends keys to it."""
        try:
            element = self.wait.until(EC.visibility_of_element_located((locator_type, locator_value)))
            element.send_keys(text)
            self.debug_print(f"Text '{text}' sent to element with {locator_type}='{locator_value}' successfully.")
        except TimeoutException as e:
            self.debug_print(f"Failed to send text to element with {locator_type}='{locator_value}': {e}")

    def login(self):
        """Logs in to Kahoot with the provided username and password."""
        self.open_login_page()
        self.wait_and_click(By.XPATH, '//button[text()="Accept all cookies"]')
        self.wait_and_send_keys(By.ID, "username", self.username + Keys.ENTER)
        self.wait_and_send_keys(By.ID, "password", self.password + Keys.ENTER)
        self.wait.until(EC.title_is("Kahoot!"))
        self.debug_print("Login successful.")

    def create_quiz(self):
        """Creates a quiz using the provided quiz data."""
        self.driver.get("https://create.kahoot.it/creator")
        self.wait_and_click(By.XPATH, '//div[@data-cta="blank"]')

        for idx, question in enumerate(self.quiz_data):
            self.debug_print(f"Adding question {idx + 1}: {question}")
            self.wait_and_send_keys(By.CSS_SELECTOR, "p[data-placeholder='Start typing your question']",
                                    question["Question"][:120] + Keys.ENTER)

            answers = question["Answers"]
            for i in range(len(answers)):
                self.wait_and_send_keys(By.ID, f"question-choice-{i}", answers[i])

            self.wait_and_click(By.XPATH, f'//button[@aria-label="Toggle answer {question["Correct"] + 1} correct."]',
                                retries=3)

            if idx < 14:  # Only add "Add question" buttons for the first 14 questions
                self.wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="add-question-button"]')
                self.wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="create-button__quiz"]')

    def save_quiz(self):
        """Saves the quiz with the provided title."""
        self.wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="top-bar__save-button"]')
        self.wait_and_send_keys(By.ID, "kahoot-title", self.title + Keys.ENTER)
        self.wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="dialog-add-title__continue"]')
        self.debug_print("Quiz saved successfully.")

    def run(self):
        """Executes the full sequence: login, create quiz, and save."""
        self.login()
        self.create_quiz()
        self.save_quiz()  # Replace with desired title

    def close(self):
        """Closes the WebDriver."""
        self.driver.quit()
