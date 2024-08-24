from .common import Trawler
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pytz import timezone
import time
from selenium.webdriver.common.by import By

path='./data/chromedriver-linux64/chromedriver'
def get_data(the_date):

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
        driver.get("https://www.family.ca/watch/?d={}".format(the_date.strftime("%Y-%m-%d")))

        time.sleep(5)
        # Get the page source after it has fully loaded
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        

        driver.quit()  # Close the WebDriver

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []

    for article in soup.find_all("div", class_="rM7ckN YJEKQk comp-lx4tukx65-container comp-lx4tukx65 wixui-box wixui-list-row list-row"):
        try:
            start_time = article.find("p", class_="font_2 wixui-rich-text__text").text.replace("p.m.", "pm").replace("a.m.", "am").strip()
            title = article.find("h3").text.strip()

            # print('\n-----------\n',start_time,title)
            # Assuming the start time is in Eastern Time, parse it and localize it
            start_time_parsed = datetime.datetime.strptime(f"{the_date.strftime('%Y-%m-%d')} {start_time} -0500", "%Y-%m-%d %I:%M %p %z")
            if start_time_parsed.date() == the_date:
                programs.append(
                    {
                        "starts": start_time_parsed.strftime("%H%M"),
                        "duration": 30,  # Default duration
                        "program_name": title,
                    }
                )
        except Exception as e:
            print(f"Error parsing program data: {e}")

    # Calculate durations based on the next program's start time
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    
   
    return programs


class TrawlerFamilyTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
