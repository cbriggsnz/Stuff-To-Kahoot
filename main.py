from Logger import set_up_logging
import logging
from selenium import webdriver
from QuizBot import QuizBot
from KahootBot import KahootBot

# fix error with sending text passwords

set_up_logging(
    console_log_output="stdout",
    console_log_level="info",
    console_log_color=True,
    logfile_file="debug.log",
    logfile_log_level="info",
    logfile_log_color=False,
    log_line_template="%(color_on)s [%(asctime)s] [%(threadName)s] [%(filename)s:%(lineno)d] [%(levelname)-8s] %(message)s%(color_off)s",
    datefmt="%Y-%m-%d %H:%M:%S"  # Format as desired
)
logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")




# Initialize WebDriver in main.py
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keep Chrome open after script runs (optional)

driver = webdriver.Chrome(options=options)

# QuizBot setup and scraping
quiz_bot = QuizBot(
    driver=driver,  # Pass the driver to QuizBot
    url="https://www.stuff.co.nz/quizzes/350407318/stuff-quiz-morning-trivia-challenge-october-29-2024",
    username="cbriggsnz1977@gmail.com",
    password="?NtLdRR8NQQff$3g",
    debug=True
)

# Run QuizBot to scrape the quiz data
print("Running Quiz Bot")
quiz = quiz_bot.run_quiz()

#
#
# # quiz = {'Title': 'Stuff quiz: Morning trivia challenge: October 29, 2024', 'Quiz_Data': [{'Correct': 1, 'Answers': ['Hack shack', 'Chop shop', 'Whip strip', 'Wreck deck'], 'Question': 'A place where stolen vehicles are dismantled so that the parts can be sold or used to repair other stolen vehicles is called a ...'}, {'Correct': 1, 'Answers': ['Gerald Ford', 'Richard Nixon', 'Lyndon B Johnson', 'Dwight D Eisenhower'], 'Question': 'Which US president was at the centre of the Watergate scandal?'}, {'Correct': 2, 'Answers': ['Rampart', 'Keep', 'Embrasure', 'Portcullis'], 'Question': 'In a medieval castle, what name was given to an opening in the wall from which cannons were fired?'}, {'Correct': 0, 'Answers': ['Eroica', 'Pastorale'], 'Question': "What is the alternate name for Beethoven's Third Symphony?"}, {'Correct': 1, 'Answers': ['Tears', 'Ear wax', 'Urine', 'Stomach acid'], 'Question': 'Cerumen is more commonly known as ...'}, {'Correct': 1, 'Answers': ['Djibouti', 'Eritrea', 'Somalia', 'South Sudan'], 'Question': 'Which country broke away from Ethiopia in 1991?'}, {'Correct': 0, 'Answers': ['Echinoderms', 'Pinnipeds', 'Fissipeds', 'Crustaceans'], 'Question': 'Sea urchins belong to which marine animal group?'}, {'Correct': 2, 'Answers': ['A piece of playground equipment', 'A police informant', 'A bar with an honour system', 'A small stove'], 'Question': 'What is an "Honest John"?'}, {'Correct': 2, 'Answers': ['Paris', 'Tokyo', 'Rome', 'London'], 'Question': 'According to the saying, which city wasn\'t "built in a day"?'}, {'Correct': 0, 'Answers': ['Lettuce', 'Tomatoes', 'Potatoes', 'Cucumber'], 'Question': 'What produce might be butterhead, iceberg, or romaine?'}, {'Correct': 0, 'Answers': ['Uptown Girl', 'Always a Woman', "We Didn't Start the Fire", 'Piano Man'], 'Question': 'What Billy Joel song was inspired by a night out with Christie Brinkley, Whitney Houston and Elle Macpherson?'}, {'Correct': 1, 'Answers': ['A cat', 'A cow', 'A duck', 'A goat'], 'Question': 'According to legend, what kind of animal caused the great Chicago fire of 1871?'}, {'Correct': 0, 'Answers': ['Five', 'Six'], 'Question': 'How many points are on a single star on the American flag?'}, {'Correct': 2, 'Answers': ['Tongue', 'Throat', 'Toe', 'Tonsils'], 'Question': 'Bunions affect which body part?'}, {'Correct': 0, 'Answers': ['Married', 'Brother and sister-in-law', 'Cousins', 'Twins'], 'Question': 'Actors Nick Offerman and Megan Mullally are ...'}]}
#
#
# # KahootBot setup and quiz creation
# kahoot_username = "mrbriggsteach@gmail.com"
# kahoot_password = "AiyfqEPC43sNr$@o"
# quiz_data = quiz["Quiz_Data"]
# title = quiz["Title"]
#

# kahoot_bot = KahootBot(
#     driver=driver,  # Pass the same driver to KahootBot
#     username=kahoot_username,
#     password=kahoot_password,
#     title=title,
#     quiz_data=quiz_data,
#     debug=True
# )
# kahoot_bot.run()

# driver.quit()

