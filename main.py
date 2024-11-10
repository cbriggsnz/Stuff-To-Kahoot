
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
# bot.mainLoop()

# quiz = bot.run_quiz()
quiz = {'Title': 'Stuff quiz: Morning trivia challenge: October 29, 2024', 'Quiz_Data': [{'Correct': 1, 'Answers': ['Hack shack', 'Chop shop', 'Whip strip', 'Wreck deck'], 'Question': 'A place where stolen vehicles are dismantled so that the parts can be sold or used to repair other stolen vehicles is called a ...'}, {'Correct': 1, 'Answers': ['Gerald Ford', 'Richard Nixon', 'Lyndon B Johnson', 'Dwight D Eisenhower'], 'Question': 'Which US president was at the centre of the Watergate scandal?'}, {'Correct': 2, 'Answers': ['Rampart', 'Keep', 'Embrasure', 'Portcullis'], 'Question': 'In a medieval castle, what name was given to an opening in the wall from which cannons were fired?'}, {'Correct': 0, 'Answers': ['Eroica', 'Pastorale'], 'Question': "What is the alternate name for Beethoven's Third Symphony?"}, {'Correct': 1, 'Answers': ['Tears', 'Ear wax', 'Urine', 'Stomach acid'], 'Question': 'Cerumen is more commonly known as ...'}, {'Correct': 1, 'Answers': ['Djibouti', 'Eritrea', 'Somalia', 'South Sudan'], 'Question': 'Which country broke away from Ethiopia in 1991?'}, {'Correct': 0, 'Answers': ['Echinoderms', 'Pinnipeds', 'Fissipeds', 'Crustaceans'], 'Question': 'Sea urchins belong to which marine animal group?'}, {'Correct': 2, 'Answers': ['A piece of playground equipment', 'A police informant', 'A bar with an honour system', 'A small stove'], 'Question': 'What is an "Honest John"?'}, {'Correct': 2, 'Answers': ['Paris', 'Tokyo', 'Rome', 'London'], 'Question': 'According to the saying, which city wasn\'t "built in a day"?'}, {'Correct': 0, 'Answers': ['Lettuce', 'Tomatoes', 'Potatoes', 'Cucumber'], 'Question': 'What produce might be butterhead, iceberg, or romaine?'}, {'Correct': 0, 'Answers': ['Uptown Girl', 'Always a Woman', "We Didn't Start the Fire", 'Piano Man'], 'Question': 'What Billy Joel song was inspired by a night out with Christie Brinkley, Whitney Houston and Elle Macpherson?'}, {'Correct': 1, 'Answers': ['A cat', 'A cow', 'A duck', 'A goat'], 'Question': 'According to legend, what kind of animal caused the great Chicago fire of 1871?'}, {'Correct': 0, 'Answers': ['Five', 'Six'], 'Question': 'How many points are on a single star on the American flag?'}, {'Correct': 2, 'Answers': ['Tongue', 'Throat', 'Toe', 'Tonsils'], 'Question': 'Bunions affect which body part?'}, {'Correct': 0, 'Answers': ['Married', 'Brother and sister-in-law', 'Cousins', 'Twins'], 'Question': 'Actors Nick Offerman and Megan Mullally are ...'}]}

print(quiz)
# print(len(quiz_data))

quiz_data = quiz["Quiz_Data"]
# quiz_data = [{'Correct': 2, 'Answers': ['Hack shack', 'Wreck deck', 'Chop shop', 'Whip strip'], 'Question': 'A place where stolen vehicles are dismantled so that the parts can be sold or used to repair other stolen vehicles is called a ...'}, {'Correct': 2, 'Answers': ['Dwight D Eisenhower', 'Lyndon B Johnson', 'Richard Nixon', 'Gerald Ford'], 'Question': 'Which US president was at the centre of the Watergate scandal?'}, {'Correct': 2, 'Answers': ['Keep', 'Portcullis', 'Embrasure', 'Rampart'], 'Question': 'In a medieval castle, what name was given to an opening in the wall from which cannons were fired?'}, {'Correct': 0, 'Answers': ['Eroica', 'Pastorale'], 'Question': "What is the alternate name for Beethoven's Third Symphony?"}, {'Correct': 0, 'Answers': ['Ear wax', 'Stomach acid', 'Tears', 'Urine'], 'Question': 'Cerumen is more commonly known as ...'}, {'Correct': 0, 'Answers': ['Eritrea', 'Somalia', 'Djibouti', 'South Sudan'], 'Question': 'Which country broke away from Ethiopia in 1991?'}, {'Correct': 1, 'Answers': ['Crustaceans', 'Echinoderms', 'Fissipeds', 'Pinnipeds'], 'Question': 'Sea urchins belong to which marine animal group?'}, {'Correct': 2, 'Answers': ['A police informant', 'A small stove', 'A bar with an honour system', 'A piece of playground equipment'], 'Question': 'What is an "Honest John"?'}, {'Correct': 1, 'Answers': ['Tokyo', 'Rome', 'Paris', 'London'], 'Question': 'According to the saying, which city wasn\'t "built in a day"?'}, {'Correct': 2, 'Answers': ['Potatoes', 'Cucumber', 'Lettuce', 'Tomatoes'], 'Question': 'What produce might be butterhead, iceberg, or romaine?'}, {'Correct': 1, 'Answers': ['Piano Man', 'Uptown Girl', "We Didn't Start the Fire", 'Always a Woman'], 'Question': 'What Billy Joel song was inspired by a night out with Christie Brinkley, Whitney Houston and Elle Macpherson?'}, {'Correct': 2, 'Answers': ['A duck', 'A goat', 'A cow', 'A cat'], 'Question': 'According to legend, what kind of animal caused the great Chicago fire of 1871?'}, {'Correct': 1, 'Answers': ['Six', 'Five'], 'Question': 'How many points are on a single star on the American flag?'}, {'Correct': 0, 'Answers': ['Toe', 'Tongue', 'Throat', 'Tonsils'], 'Question': 'Bunions affect which body part?'}, {'Correct': 2, 'Answers': ['Cousins', 'Twins', 'Married', 'Brother and sister-in-law'], 'Question': 'Actors Nick Offerman and Megan Mullally are ...'}]

options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Option to keep Chrome open

kahoot_username = "mrbriggsteach@gmail.com"
kahoot_password = "AiyfqEPC43sNr$@o"

driver = webdriver.Chrome(options = options)
driver.get("https://create.kahoot.it/auth/login")

# Function to wait for an element and click it
def wait_and_click(locator_type, locator_value, timeout=10, retries=3):
    for attempt in range(retries):
        try:
            # Locate the element and wait until it's clickable
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((locator_type, locator_value))
            )
            element.click()
            print(f"Clicked element with {locator_type}='{locator_value}' successfully.")
            return
        except ElementClickInterceptedException:
            print(f"Click intercepted, retrying... (Attempt {attempt + 1})")
            # Use WebDriverWait to wait for the element to be clickable again immediately
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((locator_type, locator_value))
            )
        except StaleElementReferenceException:
            print(f"Stale element reference, re-locating element... (Attempt {attempt + 1})")
            # Attempt to re-locate the element by waiting for it to be present
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator_value))
            )
    # If it fails after retries, log an error
    print(f"Element with {locator_type}='{locator_value}' was not found or clickable after {retries} attempts.")

# Function to wait for an element and send keys to it
def wait_and_send_keys(locator_type, locator_value, text, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((locator_type, locator_value))
        )
        element.send_keys(text)
        print(f"Text '{text}' sent to element with {locator_type}='{locator_value}' successfully.")
    except Exception as e:
        print(f"Failed to send text to element with {locator_type}='{locator_value}': {e}")

# Function to check if an element is present and optionally click based on attribute value
# def check_and_click_if_expanded(locator_type, locator_value, attribute="aria-expanded", expected_value="true"):
#     try:
#         element = driver.find_element(locator_type, locator_value)
#         if element.get_attribute(attribute) == expected_value:
#             element.click()
#             print(f"Clicked the element with {locator_type}='{locator_value}' as it was expanded.")
#         else:
#             print(f"Element with {locator_type}='{locator_value}' is not expanded; no action taken.")
#     except NoSuchElementException:
#         print(f"Element with {locator_type}='{locator_value}' is not present on the page.")
#     except Exception as e:
#         print(f"An error occurred while checking and clicking element with {locator_type}='{locator_value}': {e}")


wait_and_click(By.XPATH, '//button[text()="Accept all cookies"]')

wait_and_send_keys(By.ID, "username", kahoot_username + Keys.ENTER)

wait_and_send_keys(By.ID, "password", kahoot_password + Keys.ENTER)

WebDriverWait(driver, 10).until(EC.title_is("Kahoot!"))

driver.get("https://create.kahoot.it/creator")

wait_and_click(By.XPATH, '//div[@data-cta="blank"]')

# Send text to <p> element
for idx, question in enumerate(quiz_data):
    print(question)
    wait_and_send_keys(By.CSS_SELECTOR, "p[data-placeholder='Start typing your question']", question["Question"][:120] + Keys.ENTER)

    # Enter answers into multiple fields
    answers = question["Answers"]
    for i in range(len(answers)):
        wait_and_send_keys(By.ID, f"question-choice-{i}", answers[i])

    # Click "Toggle answer # correct" button with retries for intercepted clicks
    wait_and_click(By.XPATH, f'//button[@aria-label="Toggle answer {question["Correct"] + 1} correct."]', retries=3)

    # Click "Add question" button
    if idx < 14:
        wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="add-question-button"]')

        # Click "Add a new Quiz type question" button
        wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="create-button__quiz"]')

wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="top-bar__save-button"]')

wait_and_send_keys(By.ID, "kahoot-title", quiz["Title"] + Keys.ENTER)

wait_and_click(By.CSS_SELECTOR, 'button[data-functional-selector="dialog-add-title__continue"]')