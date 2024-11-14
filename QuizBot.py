
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchFrameException, TimeoutException,
    StaleElementReferenceException, ElementNotInteractableException
)
from SeleniumHelpers import wait_and_send_keys, click_with_retry, get_image_url, save_image_from_url
import logging


class QuizBot:
    def __init__(self, driver, quiz_type, username, password):
        self.driver = driver  # Use the provided driver
        self.quiz_type = quiz_type
        self.username = username
        self.password = password
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
            logging.info(f"Found {len(iframes)} iframes on this retry. {retries} retries left.")

            for index, iframe in enumerate(iframes):
                try:
                    # Switch to the iframe
                    self.driver.switch_to.frame(iframe)
                    button = self.driver.find_element(By.CLASS_NAME, class_name)

                    # Try clicking the button
                    if button and click_with_retry(self.driver, By.CLASS_NAME, class_name):
                        logging.info(f"Clicked button in iframe {index + 1}")
                        button_clicked = True
                        break

                except (NoSuchElementException, TimeoutException, NoSuchFrameException, StaleElementReferenceException):
                    logging.warning(f"Error accessing button in iframe {index + 1}. Retrying next iframe.")
                    self.driver.switch_to.default_content()

            if button_clicked:
                break
            else:
                self.driver.switch_to.default_content()

        if not button_clicked:
            logging.error("Button not found in any iframe after all retries.")

    def login(self):
        """Logs in using provided credentials."""
        wait_and_send_keys(self.driver, By.ID, "signInName", self.username + Keys.ENTER)
        wait_and_send_keys(self.driver, By.ID, "password", self.password + Keys.ENTER)

    def get_quiz_title(self):
        quiz_title = ""
        try:
            # Wait for the <h1> element with the quiz title to be present
            h1_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".stuff-box.stuff-article-header h1"))
            )

            quiz_title = h1_element.text

        except Exception as e:
            logging.error(f"Could not find the quiz title: {e}")

        return quiz_title

    def wait_for_answer_explanation_and_collect_answer(self):
        """Waits for the answer explanation to appear and extracts the correct answer text."""
        try:
            # Wait for the answer explanation div to be present on the page
            explanation_div = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".answer-explanation"))
            )
            logging.info("Answer explanation screen appeared.")

            # Extract the answer text from the <p> tag inside the .description div
            answer_text = explanation_div.find_element(By.CSS_SELECTOR, ".description p").text
            logging.info(f"Collected correct answer: {answer_text}")

            return answer_text
        except Exception as e:
            logging.error(f"Failed to collect answer explanation: {e}")
            return None


    def gather_quiz_data(self):
        """Collect quiz data by interacting with each question."""
        quiz_list = []
        question_number = 1  # Track question count

        while question_number <= 15:  # Repeat until all 15 questions are completed
            logging.info(f"Processing question {question_number}")

            # Attempt to click the ".choice" button to select an answer
            if click_with_retry(self.driver, By.CSS_SELECTOR, ".choice"):
                # Gather answers if selection was successful
                buttons = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".choice-title")))
                answer_list, correct_answer = [], None

                logging.info(f"Found {len(buttons)} of type .choice-title")

                for index, button in enumerate(buttons):
                    answer_text = button.text
                    answer_list.append(answer_text)
                    if button.find_elements(By.CSS_SELECTOR, ".correct"):
                        correct_answer = index

                question_text = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text
                question_dict = {"Type": "multiple-choice", "Question": question_text, "Answers": answer_list, "Correct": correct_answer}

                logging.info(f"Collected question data: {question_dict}")

                # Add question dictionary to quiz_list
                if correct_answer is not None:
                    quiz_list.append(question_dict)

                    image_url = get_image_url(self.driver, By.CSS_SELECTOR, "div.image-embed img.img")
                    logging.info(f"Image URL = {image_url}")
                    save_image_from_url(image_url, "Images", f"Image {question_number}")
                else:
                    logging.warning("No correct answer found. Reattempting question.")
                    continue

                # Attempt to click "Next" button if it exists; exit if click fails
                if not click_with_retry(self.driver, By.XPATH, '//button[text()="Next"]'):
                    logging.error("Unable to click 'Next' button. Exiting loop.")
                    break

            else:
                logging.info("Detected text-entry question.")
                try:
                    text_entry = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".text-entry-wrapper textarea")))
                    question_text = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text

                    # Collect text-entry question data

                    wait_and_send_keys(self.driver, By.CSS_SELECTOR, ".text-entry-wrapper textarea" , " "+ Keys.ENTER)
                    logging.info(f"Sent a space")
                    answer = self.wait_for_answer_explanation_and_collect_answer()
                    question_dict = {
                        "Type": "text-entry",
                        "Question": question_text,
                        "Answer": answer  # Placeholder or actual answer if available
                    }
                    quiz_list.append(question_dict)
                    logging.info(f"Collected text-entry question: {question_dict}")
                    quiz_list.append(question_dict)
                    image_url = get_image_url(self.driver, By.CSS_SELECTOR, "div.image-embed img.img")
                    logging.info(f"Image URL = {image_url}")
                    save_image_from_url(image_url, "Images", f"Image {question_number}")
                    click_with_retry(self.driver, By.CSS_SELECTOR, "button[data-test='next-btn']")
                except Exception as e:
                    logging.warning(f"Failed to process text-entry question: {e}")
                    continue  # Skip to the next question if neither type is found
            # Move to the next question only if "Next" was successfully clicked
            question_number += 1

        return quiz_list

    def find_latest_quiz(self):
        # XPath to select the latest morning quiz
        latest_morning_quiz_xpath = f'(//a[contains(@href, "/quizzes/") and contains(.//h5, "{self.quiz_type}")])[1]'

        # Wait for the element to appear and click it
        try:
            # Wait until the latest morning quiz element is clickable, then click
            latest_morning_quiz = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, latest_morning_quiz_xpath))
            )
            latest_morning_quiz.click()
            print("Successfully clicked the latest morning quiz.")
        except Exception as e:
            print(f"Could not find or click the latest morning quiz: {e}")


    def run_quiz(self):

        """Complete the quiz process from start to finish."""
        # self.open_quiz_page()
        self.driver.get("https://www.stuff.co.nz/quizzes")
        self.find_latest_quiz()
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

