from Logger import set_up_logging
import logging
from selenium import webdriver
from QuizBot import QuizBot
from KahootBot import KahootBot
from dotenv import load_dotenv
import os



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

# Initialize WebDriver in main.py
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keep Chrome open after script runs (optional)

driver = webdriver.Chrome(options=options)

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials
quiz_username = os.getenv("QUIZ_USERNAME")
quiz_password = os.getenv("QUIZ_PASSWORD")
kahoot_username = os.getenv("KAHOOT_USERNAME")
kahoot_password = os.getenv("KAHOOT_PASSWORD")

# QuizBot setup and scraping
quiz_bot = QuizBot(
    driver=driver,  # Pass the driver to QuizBot
    quiz_type = "morning",
    username=quiz_username,
    password=quiz_password
)

# Run QuizBot to scrape the quiz data
logging.info("Running Quiz Bot")
quiz = quiz_bot.run_quiz()
logging.info(quiz)
#
#
# quiz = {'Title': 'Stuff quiz: Morning trivia challenge: November 14, 2024', 'Quiz_Data': [{'Type': 'multiple-choice', 'Question': 'Which drink is distilled from the agave plant?', 'Answers': ['Vodka', 'Tequila', 'Gin', 'White rum'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'What name was given to German submarines in World War II?', 'Answers': ['T-boat', 'Q-boat', 'M-boat', 'U-boat'], 'Correct': 3}, {'Type': 'multiple-choice', 'Question': 'Which African nation was once led by Idi Amin?', 'Answers': ['Zimbabwe', 'Kenya', 'Somalia', 'Uganda'], 'Correct': 3}, {'Type': 'text-entry', 'Question': 'Which name is given to the art of ornamental tree-shaping?', 'Answer': 'Topiary'}, {'Type': 'multiple-choice', 'Question': 'A simple story with a moral is known as a ...', 'Answers': ['Riddle', 'Fable', 'Folklore', 'Fan-fiction'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'Terry Gene Bollea is better known as ...', 'Answers': ['Hulk Hogan', 'Rey Mysterio', 'Randy Savage', 'John Cena'], 'Correct': 0}, {'Type': 'multiple-choice', 'Question': 'The female organ of a flower is the ...', 'Answers': ['Stamen', 'Pistil'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'The Plains of Abraham is a reserve in ...', 'Answers': ['Quito', 'Queenstown', 'Quebec', 'Qingdao'], 'Correct': 2}, {'Type': 'multiple-choice', 'Question': 'Which musical term means "very softly"?', 'Answers': ['Diminuendo', 'Allegro', 'Cadenza', 'Pianissimo'], 'Correct': 3}, {'Type': 'multiple-choice', 'Question': 'The term pulmonary relates to the ...', 'Answers': ['Throat', 'Heart', 'Lungs', 'Sinuses'], 'Correct': 2}, {'Type': 'multiple-choice', 'Question': 'Which Jewish festival falls 50 days after Passover?', 'Answers': ['Pentecost', 'Rosh Hashanah', 'Sukkot', 'Shavuot'], 'Correct': 3}, {'Type': 'multiple-choice', 'Question': 'The South American Pampas are ...', 'Answers': ['Grass plains', 'Rocky cliffs', 'Salt flats', 'Deserts'], 'Correct': 0}, {'Type': 'multiple-choice', 'Question': 'A baby turkey is called a ...', 'Answers': ['Chick', 'Turkling', 'Tucklet', 'Poult'], 'Correct': 3}, {'Type': 'multiple-choice', 'Question': 'Which of these is a ring-toss game?', 'Answers': ['Croquet', 'Lacrosse', 'Quoits', 'Bocce'], 'Correct': 2}, {'Type': 'multiple-choice', 'Question': 'Good King Wenceslas was the duke of ...', 'Answers': ['Edinburgh', 'Bohemia', 'Arabia', 'Somerset'], 'Correct': 1}]}

#
# # KahootBot setup and quiz creation
quiz_data = quiz["Quiz_Data"]
title = quiz["Title"]


kahoot_bot = KahootBot(
    driver=driver,  # Pass the same driver to KahootBot
    username=kahoot_username,
    password=kahoot_password,
    title=title,
    quiz_data=quiz_data,
    debug=True
)
kahoot_bot.run()

# driver.quit()

