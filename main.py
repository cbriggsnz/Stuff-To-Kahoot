
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
import time
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Option to keep Chrome open

# # # Specify path to Chrome User Data Folder
# options.add_argument(r'--user-data-dir=C:\Users\Craig\AppData\Local\Google\Chrome\User Data')
#
# options.add_argument('--profile-directory=SeleniumProfile')

driver = webdriver.Chrome(options=options)
#
driver.get("https://www.stuff.co.nz/quizzes/350407318/stuff-quiz-morning-trivia-challenge-october-29-2024")

time.sleep(3)
# driver.switch_to.frame(2)
# iframe = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.login-modal > iframe")))
# iframe = driver.find_element(By.CSS_SELECTOR, "iframe")

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
# #main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list
# #main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div > ul
# time.sleep(4)
# jobs = driver.find_elements(By.CSS_SELECTOR, value = ".job-card-container--clickable")
# # <h1 class="t-24 t-bold inline"><a href="/jobs/view/4046079284/?alternateChannel=search&amp;refId=HfM4ycjCmtbVSxZ0LAROPA%3D%3D&amp;trackingId=uFCmfIiuvi2Xer6mob4xGg%3D%3D&amp;trk=d_flagship3_job_details" id="ember1545" class="ember-view">Salesforce Developer</a></h1>
# print(len(jobs))
# for idx, job in enumerate(jobs):
#     print("Opening Job")
#     job.click()
#     time.sleep(2)
#
#     title = driver.find_element(By.CSS_SELECTOR, value = "h1 a")
#     print(f"{idx}   {title.text}   ")
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
# time.sleep(3)

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