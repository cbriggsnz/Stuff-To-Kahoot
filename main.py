from Logger import set_up_logging
import logging
from selenium import webdriver
from QuizBot import QuizBot
from KahootBot import KahootBot
from dotenv import load_dotenv
import os
from pathlib import Path


def create_env_template():
    """Create a .env file template with placeholders for credentials."""
    env_path = Path(".") / ".env"
    if not env_path.exists():
        logging.info("No .env file found. Creating a template .env file.")
        with env_path.open("w") as env_file:
            env_file.write(
                "QUIZ_USERNAME=your_quiz_username\n"
                "QUIZ_PASSWORD=your_quiz_password\n"
                "KAHOOT_USERNAME=your_kahoot_username\n"
                "KAHOOT_PASSWORD=your_kahoot_password\n"
            )
        logging.info(f"Template .env file created at: {env_path.resolve()}")
        logging.info("Please edit the .env file to add your credentials.")
        return False  # Indicates that the .env file was just created
    return True  # Indicates that the .env file already exists


def initialize_logging():
    """Set up the logging configuration."""
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


def initialize_driver():
    """Initialize the Selenium WebDriver with desired options."""
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Keep Chrome open after script runs (optional)

    return webdriver.Chrome(options=options)


def load_credentials():
    """Load credentials from environment variables and validate them."""
    load_dotenv()

    quiz_username = os.getenv("QUIZ_USERNAME")
    quiz_password = os.getenv("QUIZ_PASSWORD")
    kahoot_username = os.getenv("KAHOOT_USERNAME")
    kahoot_password = os.getenv("KAHOOT_PASSWORD")

    if not all([quiz_username, quiz_password, kahoot_username, kahoot_password]):
        missing = [name for name, value in {
            "QUIZ_USERNAME": quiz_username,
            "QUIZ_PASSWORD": quiz_password,
            "KAHOOT_USERNAME": kahoot_username,
            "KAHOOT_PASSWORD": kahoot_password
        }.items() if not value]
        logging.error(f"Missing environment variables: {', '.join(missing)}")
        return None

    return {
        "quiz_username": quiz_username,
        "quiz_password": quiz_password,
        "kahoot_username": kahoot_username,
        "kahoot_password": kahoot_password
    }


def run_quiz_bot(driver, credentials):
    """Run QuizBot to gather quiz data."""
    quiz_bot = QuizBot(
        driver=driver,
        quiz_type="morning",
        username=credentials["quiz_username"],
        password=credentials["quiz_password"]
    )

    logging.info("Running Quiz Bot")
    quiz = quiz_bot.run_quiz()
    logging.info(quiz)
    return quiz


def run_kahoot_bot(driver, credentials, quiz):
    """Run KahootBot to create a Kahoot quiz."""
    kahoot_bot = KahootBot(
        driver=driver,
        username=credentials["kahoot_username"],
        password=credentials["kahoot_password"],
        title=quiz["Title"],
        quiz_data=quiz["Quiz_Data"],
        debug=True
    )
    kahoot_bot.run()


def main():
    try:
        # Initialize logging
        initialize_logging()

        # Check for or create .env file
        if not create_env_template():
            logging.info("Edit the .env file and re-run the program.")
            return

        # Initialize WebDriver
        driver = initialize_driver()

        # Load and validate credentials
        credentials = load_credentials()
        if credentials is None:
            return

        # Run QuizBot and KahootBot
        quiz = run_quiz_bot(driver, credentials)
        run_kahoot_bot(driver, credentials, quiz)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        # Ensure WebDriver cleanup
        if 'driver' in locals():
            driver.quit()


# Run the main function when executed directly
if __name__ == "__main__":
    main()
