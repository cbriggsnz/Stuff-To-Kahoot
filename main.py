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

# Initialize WebDriver in main.py
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keep Chrome open after script runs (optional)

driver = webdriver.Chrome(options=options)

# QuizBot setup and scraping
quiz_bot = QuizBot(
    driver=driver,  # Pass the driver to QuizBot
    quiz_type = "morning",
    username="cbriggsnz1977@gmail.com",
    password="?NtLdRR8NQQff$3g"
)

# Run QuizBot to scrape the quiz data
logging.info("Running Quiz Bot")
# quiz = quiz_bot.run_quiz()
# print(quiz)
#
#
quiz = {'Title': 'Stuff quiz: Morning trivia challenge: November 14, 2024', 'Quiz_Data': [{'Type': 'multiple-choice', 'Question': 'Which drink is distilled from the agave plant?', 'Answers': ['Tequila', 'White rum', 'Gin', 'Vodka'], 'Correct': 0}, {'Type': 'multiple-choice', 'Question': 'What name was given to German submarines in World War II?', 'Answers': ['Q-boat', 'U-boat', 'T-boat', 'M-boat'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'Which African nation was once led by Idi Amin?', 'Answers': ['Zimbabwe', 'Uganda', 'Somalia', 'Kenya'], 'Correct': 1}, {'Type': 'text-entry', 'Question': 'Which name is given to the art of ornamental tree-shaping?', 'Answer': 'Topiary'}, {'Type': 'text-entry', 'Question': 'Which name is given to the art of ornamental tree-shaping?', 'Answer': 'Topiary'}, {'Type': 'multiple-choice', 'Question': 'A simple story with a moral is known as a ...', 'Answers': ['Riddle', 'Fan-fiction', 'Folklore', 'Fable'], 'Correct': 3}, {'Type': 'multiple-choice', 'Question': 'Terry Gene Bollea is better known as ...', 'Answers': ['Rey Mysterio', 'John Cena', 'Randy Savage', 'Hulk Hogan'], 'Correct': 3}, {'Type': 'multiple-choice', 'Question': 'The female organ of a flower is the ...', 'Answers': ['Stamen', 'Pistil'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'The Plains of Abraham is a reserve in ...', 'Answers': ['Qingdao', 'Quito', 'Quebec', 'Queenstown'], 'Correct': 2}, {'Type': 'multiple-choice', 'Question': 'Which musical term means "very softly"?', 'Answers': ['Cadenza', 'Diminuendo', 'Pianissimo', 'Allegro'], 'Correct': 2}, {'Type': 'multiple-choice', 'Question': 'The term pulmonary relates to the ...', 'Answers': ['Heart', 'Lungs', 'Throat', 'Sinuses'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'Which Jewish festival falls 50 days after Passover?', 'Answers': ['Shavuot', 'Pentecost', 'Rosh Hashanah', 'Sukkot'], 'Correct': 0}, {'Type': 'multiple-choice', 'Question': 'The South American Pampas are ...', 'Answers': ['Rocky cliffs', 'Grass plains', 'Salt flats', 'Deserts'], 'Correct': 1}, {'Type': 'multiple-choice', 'Question': 'A baby turkey is called a ...', 'Answers': ['Poult', 'Turkling', 'Chick', 'Tucklet'], 'Correct': 0}, {'Type': 'multiple-choice', 'Question': 'Which of these is a ring-toss game?', 'Answers': ['Quoits', 'Bocce', 'Croquet', 'Lacrosse'], 'Correct': 0}, {'Type': 'multiple-choice', 'Question': 'Good King Wenceslas was the duke of ...', 'Answers': ['Bohemia', 'Edinburgh', 'Somerset', 'Arabia'], 'Correct': 0}]}

#
# # KahootBot setup and quiz creation
kahoot_username = "mrbriggsteach@gmail.com"
kahoot_password = "AiyfqEPC43sNr$@o"
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

