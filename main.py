
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"


options = webdriver.ChromeOptions()

options.page_load_strategy = 'eager'
options.add_experimental_option("detach", True)  # Option to keep Chrome open

driver = webdriver.Chrome(options = options)
#
driver.get("https://www.stuff.co.nz/quizzes/350407318/stuff-quiz-morning-trivia-challenge-october-29-2024")

# time.sleep(3)

    # switch to selected iframe
# driver.switch_to.frame(3)

    # Now click on button
# driver.find_element(By.TAG_NAME, 'button').click()
# driver.switchTo().frame(driver.findElement(By.cssSelector("iframe")));
# username = driver.find_element(By.XPATH, value = '//*[@id="template-container"]/div/div[2]/article/div[2]/div/button')
# username.click()
# print(driver.page_source.encode("utf-8"))
# username.send_keys("cbriggsnz@gmail.com")
#
# password = driver.find_element(By.ID, value = "password")
# password.send_keys("gumoh1977", Keys.ENTER)
#
# driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4046079284&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")

# elements = driver.find_elements(By.CSS_SELECTOR, ".event-widget .shrubbery ul li ")
# # print(element.text)
# events = {}
# for idx, element in enumerate(elements):
#     # print(element.text)
#     event_details = element.text.split("\n")
#     dict = {"name" : event_details[0], "time":event_details[1] }
#     events[idx] = dict

# print(events)
# price_whole = driver.find_element(
#     by=By.XPATH,
#     value='//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[2]/span[2]'
# )
# print(price_whole.text)
# driver.quit()

# Wait for the page to load
time.sleep(3)

# Get all iframe elements on the page

iframes = driver.find_elements(By.TAG_NAME, 'iframe')

button_clicked = False

# Iterate through each iframe
for index, iframe in enumerate(iframes):
    try:
        # Switch to the iframe
        driver.switch_to.frame(iframe)
        # Try to find the button with the specified text
        button = driver.find_element(By.CLASS_NAME, "stuff-button")
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

# iframe_locator = (By.ID, 'Morning October 29, 2024')
#
# # Wait for the iframe to load and switch to it
# iframe = wait_for_iframe_and_switch((By.ID, 'Morning October 29, 2024'))
#
# if iframe:
#     # Now you are within the iframe and can interact with elements inside it
#     # Perform your actions here
#
#     print("Locatied")
# else:
#     print("Failed to locate and switch to iframe.")

    # driver.quit()
# quiz = wait_for(By.CSS_SELECTOR, ".content-slot iframe")#
html_text = driver.find_element(By.CSS_SELECTOR, value = ".content-slot iframe").text
# print(html_text.text)
print(type(html_text))
# print("\n\n\n\n")

# Dictionary to store questions and answers
quiz_dict = {}
quiz_list = []
# Regular expression to capture each question and its answers
question_pattern = r"<h[23]>(.*?)</h[23]>"
answers_pattern = r"<li>(.*?)</li>"

# Find all sections and iterate over them
for section in re.findall(r"<section.*?</section>", html_text, re.DOTALL):
    # Extract the question
    question_match = re.search(question_pattern, section)
    if question_match:
        question_text = question_match.group(1)

        # Extract all answers for this question
        answers = re.findall(answers_pattern, section)

        # Create dictionary for the current question
        question_dict = {"Question": question_text}

        # Assign letters (A, B, C...) to each answer
        for idx, answer in enumerate(answers):
            question_dict[f"Answer {chr(65 + idx)}"] = answer  # chr(65) is 'A', chr(66) is 'B', etc.

        # Append the question dictionary to the list
        quiz_list.append(question_dict)

# Print the result
print(quiz_list)
# section = driver.find_element(By.TAG_NAME, "li")
# print(section.text)
# Locate all sections with `data-block="SingleChoice"`
# sections = driver.find_elements(By.TAG_NAME, 'h2')
#
# section = driver.find_element(By.CSS_SELECTOR, "section[data-block='SingleChoice']")
# print(section.text)
# for idx, section in enumerate(sections):
# #     # Extract the question text from the <h2> or <h3> tag
#     print(f"{idx} - {section.text}")
#     # question_element = section.find_element(By.XPATH, './h2 | ./h3')
    # question = question_element.text
    #
    # # Extract answers from <li> tags within the <ul> tag
    # answer_elements = section.find_elements(By.XPATH, './ul/li')
    # answers = [answer.text for answer in answer_elements]
    #
    # # Add question and answers to the dictionary
    # qa_dict[question] = answers

# Print the resulting dictionary
# print(qa_dict)