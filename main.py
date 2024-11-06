
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# options = webdriver.ChromeOptions()
# options.page_load_strategy = 'eager'
# options.add_experimental_option("detach", True)  # Option to keep Chrome open
#
# driver = webdriver.Chrome(options = options)
# driver.get("https://www.stuff.co.nz/quizzes/350407318/stuff-quiz-morning-trivia-challenge-october-29-2024")
#
# def find_iframe_by_class(class_name: str, retries: int = 3):
#     # Wait for iframes to be present initially
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
#     print("Found iframes on page.")
#
#     overall_retries = retries
#     button_clicked = False
#
#     while overall_retries > 0:
#         print(f"Attempt {retries - overall_retries + 1} to locate and click the button.")
#         # Refresh the list of iframes each retry
#         iframes = driver.find_elements(By.TAG_NAME, 'iframe')
#         print(f"Found {len(iframes)} iframes on this retry.")
#
#         for index, iframe in enumerate(iframes):
#             try:
#                 # Switch to the iframe
#                 driver.switch_to.frame(iframe)
#                 print(f"Switched to iframe {index + 1}")
#
#                 # Try to locate the button with the specified class
#                 button = driver.find_element(By.CLASS_NAME, class_name)
#                 # Click the button if found
#                 button.click()
#                 print(f"Clicked button in iframe {index + 1}")
#                 button_clicked = True
#                 break  # Exit the loop if the button is clicked successfully
#
#             except (NoSuchElementException, TimeoutException):
#                 print(f"Button not found in iframe {index + 1}, moving to the next iframe.")
#                 driver.switch_to.default_content()  # Switch back to main content
#
#             except (NoSuchFrameException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException):
#                 print(f"Cannot interact with iframe {index + 1}.")
#                 driver.switch_to.default_content()
#
#         # Exit the retry loop if the button was clicked
#         if button_clicked:
#             break
#         else:
#             # Decrement overall retry count and print a message
#             overall_retries -= 1
#             print(f"Retrying... {overall_retries} retries left.")
#             driver.switch_to.default_content()  # Ensure we return to the main content
#
#     # Final check to confirm if the button was clicked
#     if not button_clicked:
#         print("Button not found in any iframe after all retries.")
# wait = WebDriverWait(driver, 10)
#
# find_iframe_by_class("stuff-button")
#
# driver.switch_to.default_content()
#
# email_address = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, "signInName"))
# )
# email_address.send_keys("cbriggsnz1977@gmail.com", Keys.ENTER)
#
# password = driver.find_element(By.ID, value = "password")
# password.send_keys("?NtLdRR8NQQff$3g", Keys.ENTER)
#
# WebDriverWait(driver, 10).until(EC.title_contains("Stuff quiz"))
#
# find_iframe_by_class("block-nav", retries=16)
#
# quiz_list = []
#
# # Define a helper function to handle clicking with retry logic
# def click_with_retry(driver, locator, retries=3):
#     while retries > 0:
#         try:
#             # Wait for the element to be clickable and click it
#             button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
#             button.click()
#             return True
#         except (StaleElementReferenceException, ElementNotInteractableException, TimeoutException):
#             retries -= 1
#             if retries == 0:
#                 print(f"Failed to locate and click the element {locator} after multiple retries.")
#     return False
#
# for i in range(15):
#     # Click the ".choice" button with retry logic
#     if not click_with_retry(driver, (By.CSS_SELECTOR, ".choice")):
#         print("Skipping to next iteration due to unrecoverable click error.")
#         continue  # Move to the next iteration if click fails
#
#     # Wait for ".choice-title" elements to be present
#     buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".choice-title")))
#
#     # Gather question and answers into a dictionary
#     question_dict = {}
#     for idx, b in enumerate(buttons):
#         index = idx + 1
#         correct = b.find_elements(By.CSS_SELECTOR, ".correct")
#         question_dict[f"Answer {index}"] = b.text
#         if correct:  # Non-empty list implies correctness
#             question_dict["Correct"] = index
#
#     # Wait for the question title to load and retrieve its text
#     question_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))).text
#     question_dict["Question"] = question_text
#
#     # Print and append the question dictionary to the quiz list
#     print(question_dict)
#     quiz_list.append(question_dict)
#
#     # Click the "Next" button with retry logic to ensure smooth transition
#     if not click_with_retry(driver, (By.XPATH, '//button[text()="Next"]')):
#         print("Encountered issue clicking 'Next' button. Exiting loop.")
#         break  # Stop the loop if the "Next" button fails
#
# print(quiz_list)

# from QuizBot import QuizBot
#
# bot = QuizBot(
#     url="https://www.stuff.co.nz/quizzes/350407318/stuff-quiz-morning-trivia-challenge-october-29-2024",
#     username="cbriggsnz1977@gmail.com",
#     password="?NtLdRR8NQQff$3g",
#     debug=False
# )
# # bot.mainLoop()
#
# quiz_data = bot.run_quiz()
# print(quiz_data)
# print(len(quiz_data))
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_experimental_option("detach", True)  # Option to keep Chrome open

kahoot_username = "mrbriggsteach@gmail.com"
kahoot_password = "AiyfqEPC43sNr$@o"

driver = webdriver.Chrome(options = options)
driver.get("https://create.kahoot.it/auth/login")

time.sleep(2)

button = driver.find_element(By.XPATH, '//button[text()="Accept all cookies"]')
button.click()

email_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username")))
email_field.send_keys(kahoot_username, Keys.ENTER)

password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))
password_field.send_keys(kahoot_password, Keys.ENTER)

print(driver.title)
# time.sleep(3)
WebDriverWait(driver, 10).until(EC.title_is("Kahoot!"))
print(driver.title)

driver.get("https://create.kahoot.it/creator")

try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-cta="blank"]'))
    )
    # Click the button
    button.click()
    print("Clicked on the 'Blank canvas' button successfully.")
except Exception as e:
    print("The 'Blank canvas' button did not appear or was not clickable:", e)



try:
    p_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p[data-placeholder='Start typing your question']"))
    )
    p_element.send_keys("This is a test", Keys.ENTER)
    # Add text to the <p> element using JavaScript
    print("Text added to the <p> element successfully.")
except Exception as e:
    print("The <p> element with data-placeholder='Start typing your question' did not load:", e)

def enter_answers(answer_id, answer):
    try:
        div_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, answer_id))
        )

        div_element.send_keys(answer)
        # Add text to the contenteditable <div> using JavaScript
        print("Text added to the <div> element successfully.")
    except Exception as e:
        print("The <div> element with id='question-choice-0' did not load or was not visible:", e)

for i in range(4):
    enter_answers(f"question-choice-{i}", f"Answer {i}")