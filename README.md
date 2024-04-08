Amazon Scraper
This project automates the task of scraping data from Amazon's website across multiple regional domains (USA, Germany, UK, France). 
It uses Selenium WebDriver to simulate user interactions with web pages, managing elements like captchas and dynamically loaded content effectively. 
The scraper is set to run at predefined intervals, collecting data such as ASINs (Amazon Standard Identification Numbers) related to specific keywords and handling various challenges like location settings and captcha verifications.

Features
Multi-Region Support: Works across multiple Amazon domains (amazon.com, amazon.de, amazon.co.uk, amazon.fr) to collect market-specific data.
Captcha Handling: Automatically detects and resolves captcha challenges to maintain continuous scraping operations.
Data Extraction and Association: Retrieves product ASINs and matches them with company-specific SKUs from an internal catalog, along with extracting page positions, prices, and other relevant details.
Headless Browsing: Runs in headless mode for improved performance on server environments.
Dynamic Proxy Use: Implements proxy management to simulate requests from various geographic locations, aiding in localized data collection and minimizing IP-related blocks.
Scheduled Execution: Utilizes Python's datetime and timedelta for scheduling scraping sessions.
Telecommunication and Database Integration: Sends updates and alerts via region-specific Telegram bots and stores the extracted data in a database for further analysis.
Configurable: Easily adjustable settings for adding more regions or altering configurations.
Prerequisites
Before you run the scraper, ensure you have the following installed:

Python 3.8+
Selenium WebDriver
Google Chrome or Chromium Browser
ChromeDriver compatible with your browser version
Necessary Python packages (listed in requirements.txt)

Setup
Clone the Repository:
git clone [https://github.com/katrinaturcha/amazon_impressions.git]
cd amazon-scraper

Install Dependencies:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

Configuration:
Edit the .env file with your proxy information, Telegram bot tokens, and other settings as needed.

Running the Scraper:
python scraper.py

Usage:
Execute the main script with configurations tailored based on the target region and other parameters set in the .env. 
The script logs activities and saves data, while also sending alerts and updates through integrated Telegram bots. 
Extracted data is sent to a database for persistent storage and further analysis.
