from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By

path='./data/chromedriver-linux64/chromedriver'
def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (optional, improves performance)
        chrome_options.add_argument("--disable-notifications")  # Disable notifications
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (for some environments)
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in containers

        # Set up the WebDriver with options
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the webpage
        driver.get("https://miraclechannel.ca/schedule/")

        time.sleep(5)
        # Get the page source after it has fully loaded
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        

        driver.quit()  # Close the WebDriver

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []
    
    # The schedule is organized by time slots and program details
    slots = soup.find_all('div', class_='schedule_widget__slot')
    cards = soup.find_all('div', class_='schedule_widget__card-wrapper')


    for slot, card in zip(slots, cards):
        time_str = slot.text.strip()
        program_name = card.find('div', class_='schedule_widget__card-inner-title').text.strip()

        start_time = datetime.datetime.strptime("{} {} -0600".format(the_date.strftime("%Y-%m-%d"), time_str), "%Y-%m-%d %I:%M %p %z")
        start_time = start_time.astimezone(central_tz)

        if start_time.date() == the_date:
            duration_text = card.find('div', class_='schedule_widget__card-inner-duration').text.strip()
            duration_match = re.search(r'(\d+)', duration_text)

            if duration_match:  # Ensure that a match is found before accessing group(1)
                duration = int(duration_match.group(1))

                programs.append({
                    "starts": start_time.strftime("%H%M"),
                    "duration": duration,
                    "program_name": program_name
                })

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerMiracleChannel(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
