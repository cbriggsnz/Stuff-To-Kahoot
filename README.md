# Automated Quiz Bot System

This repository provides a system to automate the collection of quiz data from a quiz platform and upload it to a Kahoot account. It uses Selenium to interact with web pages, retrieve data, and create quizzes programmatically.

----------

## Features

-   **QuizBot**: Logs into a quiz platform, scrapes quiz questions and answers, and saves relevant data.
-   **KahootBot**: Logs into a Kahoot account, creates a new quiz, and uploads questions and images programmatically.
-   **Logging**: Comprehensive logging system for debugging and monitoring operations.
-   **Environment Variable Management**: Uses a `.env` file to store credentials securely.
-   **Executable Script**: Can be packaged as an executable for ease of use.

----------

## Repository Structure

The repository contains the following files:

-   **`main.py`**: The entry point for the program. Handles setup, initialization, and orchestrates the `QuizBot` and `KahootBot` workflows. Checks for the presence of a `.env` file and creates a template if not found.
-   **`QuizBot.py`**: Automates quiz data collection. Logs into the quiz platform, navigates through questions, collects data, and retrieves associated images.
-   **`KahootBot.py`**: Automates Kahoot quiz creation. Uses the quiz data collected by `QuizBot` to create a Kahoot quiz with questions, answers, and images.
-   **`Logger.py`**: Configures logging for both console and file output. Supports color-coded console output for better readability.
-   **`SeleniumHelpers.py`**: Contains utility functions to simplify Selenium interactions. Includes robust methods for handling retries, waiting for elements, and managing stale elements.

----------

## Requirements

### 1. Python Version

-   Python 3.7 or higher is recommended.

### 2. Dependencies

-   Install dependencies from `requirements.txt`:
    
    bash
    
    Copy code
    
    `pip install -r requirements.txt` 
    

### 3. WebDriver

-   Download the ChromeDriver version compatible with your Chrome browser from ChromeDriver.
-   Ensure the ChromeDriver executable is in your system's PATH.

----------

## Setup

### Step 1: Clone the Repository

bash

Copy code

`git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name` 

### Step 2: Create and Edit the `.env` File

The program will automatically create a `.env` file if it doesn't exist. Run the program once:

bash

Copy code

`python main.py` 

This will generate a `.env` file with the following structure:

plaintext

Copy code

`QUIZ_USERNAME=your_quiz_username
QUIZ_PASSWORD=your_quiz_password
KAHOOT_USERNAME=your_kahoot_username
KAHOOT_PASSWORD=your_kahoot_password` 

Edit the `.env` file to include your credentials.

### Step 3: Install Dependencies

Install the required Python packages:

bash

Copy code

`pip install -r requirements.txt` 

----------

## How to Use `QuizBot`

### Overview

`QuizBot` is responsible for logging into the quiz platform and scraping quiz data. It uses your credentials from the `.env` file to perform the login and then collects questions, answers, and associated images.

### Steps

1.  Ensure your quiz platform credentials (`QUIZ_USERNAME` and `QUIZ_PASSWORD`) are set correctly in the `.env` file.
2.  The bot will:
    -   Log into the quiz platform.
    -   Navigate through the quiz questions.
    -   Collect multiple-choice and text-entry question data.
    -   Retrieve associated images and save them locally.

### Output

-   Collected data is logged in `debug.log`.
-   Images are saved in the `Images` folder.

----------

## How to Use `KahootBot`

### Overview

`KahootBot` uses the data collected by `QuizBot` to create a new Kahoot quiz. It uploads questions, answers, and associated images to your Kahoot account.

### Steps

1.  Ensure your Kahoot credentials (`KAHOOT_USERNAME` and `KAHOOT_PASSWORD`) are set correctly in the `.env` file.
2.  The bot will:
    -   Log into your Kahoot account.
    -   Create a new quiz with the title provided by `QuizBot`.
    -   Upload questions and answers (multiple-choice format).
    -   Upload associated images, if available.

### Notes

-   If a question has missing data (e.g., no correct answer), `KahootBot` will skip it and log a warning.
-   Images must be available in the `Images` folder and named according to the expected format (e.g., `Image 1.webp`).

----------

## Running the Program

Run the program using:

bash

Copy code

`python main.py` 

The program will:

1.  Use `QuizBot` to scrape quiz data from the quiz platform.
2.  Use `KahootBot` to upload the collected data to your Kahoot account as a new quiz.

----------

## Packaging as an Executable

You can package the project as an executable using `PyInstaller`:

1.  Install PyInstaller:
    
    bash
    
    Copy code
    
    `pip install pyinstaller` 
    
2.  Create the executable:
    
    bash
    
    Copy code
    
    `pyinstaller --onefile main.py` 
    
3.  The executable will be created in the `dist` folder. You can run it directly:
    
    bash
    
    Copy code
    
    `./dist/main` 
    

----------

## Logging

Logs are saved to `debug.log` by default. Console logs are color-coded for better readability. The logging configuration can be customized in `Logger.py`.

----------

## Troubleshooting

### Common Issues

1.  **Missing `.env` File**:
    -   Ensure the `.env` file exists and is correctly formatted.
2.  **WebDriver Errors**:
    -   Check that ChromeDriver is installed and compatible with your Chrome version.

### Debugging

Enable debug-level logging by editing the log level in `main.py`:

python

Copy code

`initialize_logging(console_log_level="debug")` 

----------

## Contributing

1.  Fork the repository.
2.  Create a feature branch:
    
    bash
    
    Copy code
    
    `git checkout -b feature-name` 
    
3.  Commit your changes:
    
    bash
    
    Copy code
    
    `git commit -m "Description of changes"` 
    
4.  Push to your branch:
    
    bash
    
    Copy code
    
    `git push origin feature-name` 
    
5.  Create a Pull Request.

----------

## License

This project is licensed under the MIT License. See the LICENSE file for details.

----------

## Acknowledgments

-   Selenium for enabling browser automation.
-   Python community for the amazing libraries and support.
