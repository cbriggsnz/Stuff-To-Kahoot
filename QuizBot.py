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
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        # Initialize WebDriver and set page load strategy
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_quiz_page(self):
        """Open the specified quiz page URL."""
        self.driver.get(self.url)

    def find_iframe_by_class(self, class_name, retries=3):
        """Locate and click a button inside an iframe by class name with retries."""
        # Wait until iframes are present on the page
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        print("Found iframes on page.")

        button_clicked = False
        while retries > 0:
            # Refresh the list of iframes each retry
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            print(f"Found {len(iframes)} iframes on this retry.")

            for index, iframe in enumerate(iframes):
                try:
                    # Switch to the iframe
                    self.driver.switch_to.frame(iframe)
                    print(f"Switched to iframe {index + 1}")

                    # Attempt to find the button by class name
                    button = self.driver.find_element(By.CLASS_NAME, class_name)

                    # Try clicking the button
                    try:
                        button.click()
                        print(f"Clicked button in iframe {index + 1}")
                        button_clicked = True
                        break  # Exit the loop if the button is clicked successfully
                    except ElementNotInteractableException:
                        print("Button found but not interactable. Retrying...")

                except (NoSuchElementException, TimeoutException):
                    print(f"Button not found in iframe {index + 1}, moving to next iframe.")
                    self.driver.switch_to.default_content()
                except (NoSuchFrameException, StaleElementReferenceException):
                    print(f"Iframe {index + 1} became stale or inaccessible, retrying.")
                    self.driver.switch_to.default_content()

            if button_clicked:
                break
            else:
                retries -= 1
                print(f"Retrying... {retries} retries left.")
                self.driver.switch_to.default_content()

        if not button_clicked:
            print("Button not found in any iframe after all retries.")

    def login(self):
        """Logs in using provided credentials."""
        email_field = self.wait.until(EC.element_to_be_clickable((By.ID, "signInName")))
        email_field.send_keys(self.username, Keys.ENTER)

        password_field = self.wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_field.send_keys(self.password, Keys.ENTER)

    def gather_quiz_data(self):
        """Collect quiz data by interacting with each question."""
        quiz_list = []
        for i in range(15):
            if not self.click_with_retry((By.CSS_SELECTOR, ".choice")):
                continue

            # Gather answers and question
            buttons = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".choice-title")))
            question_dict = {}
            for idx, b in enumerate(buttons):
                index = idx + 1
                correct = b.find_elements(By.CSS_SELECTOR, ".correct")
                question_dict[f"Answer {index}"] = b.text
                if correct:
                    question_dict["Correct"] = index

            # Retrieve question text
            question_text = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text
            question_dict["Question"] = question_text

            print(question_dict)
            quiz_list.append(question_dict)

            # Click "Next" button with retry logic
            if not self.click_with_retry((By.XPATH, '//button[text()="Next"]')):
                break

        return quiz_list

    def click_with_retry(self, locator, retries=3):
        """Attempt to click an element, retrying if necessary."""
        while retries > 0:
            try:
                button = self.wait.until(EC.element_to_be_clickable(locator))
                button.click()
                return True
            except (StaleElementReferenceException, ElementNotInteractableException):
                retries -= 1
        return False

    def run_quiz(self):
        """Complete the quiz process from start to finish."""
        self.open_quiz_page()
        self.find_iframe_by_class("stuff-button")
        self.driver.switch_to.default_content()
        self.login()
        WebDriverWait(self.driver, 10).until(EC.title_contains("Stuff quiz"))
        self.find_iframe_by_class("block-nav", retries=16)
        return self.gather_quiz_data()

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()

