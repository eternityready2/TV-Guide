from .common import Trawler
import datetime
from bs4 import BeautifulSoup
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
        driver = webdriver.Chrome( options=chrome_options)

        # Navigate to the webpage
        driver.get("https://www.stream.emmanuel.tv/main")
        time.sleep(10)  # Allow time for the page to load completely

        # Get the page source after loading
        source1 = driver.page_source
        soup1 = BeautifulSoup(source1, 'html.parser')

        # Click the "Next Day" button to get programs for the next day
        try:
            next_day_button = driver.find_element(By.CSS_SELECTOR, "span#day-8")  # Adjust CSS selector as needed
            next_day_button.click()
            time.sleep(10)  # Allow time for the page to load after clicking
        except Exception as e:
            print(f"Error clicking 'Next Day' button: {e}")

        source2 = driver.page_source
        soup2 = BeautifulSoup(source2, 'html.parser')

        driver.quit()  # Close the WebDriver

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    
    programs = []
    central_tz = timezone('America/Chicago')

    # Parsing today's programs
    for block in soup1.find_all("li", class_="timeline-item-p"):
        try:
            time_text = block.find("div", class_="timeProgram").text.strip()
            title = block.find("div", class_="programTitle").text.strip()
            time_str = "{} {} +0100".format(the_date.strftime("%Y-%m-%d"), time_text.split()[0].replace("LIVE", "04:00"))
            starts = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M %z")
            starts = starts.astimezone(central_tz)
            if starts.date() == the_date:
                programs.append(
                    {
                        "starts": starts.strftime("%H%M"),
                        "duration": 30,  # Default duration
                        "program_name": title,
                    }
                )
        except Exception as e:
            print(f"Error parsing today's program: {e}")
            continue
        
    # Parsing next day's programs
    for block2 in soup2.find_all("li", class_="timeline-item-p"):
        try:
            time_text2 = block2.find("div", class_="timeProgram").text.strip()
            title2 = block2.find("div", class_="programTitle").text.strip()
            time_str2 = "{} {} +0100".format((the_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), time_text2.split()[0])
            starts2 = datetime.datetime.strptime(time_str2, "%Y-%m-%d %H:%M %z")
            starts2 = starts2.astimezone(central_tz)
            if starts2.date() == the_date:
                programs.append(
                    {
                        "starts": starts2.strftime("%H%M"),
                        "duration": 40,  # Default duration
                        "program_name": title2,
                    }
                )
        except Exception as e:
            print(f"Error parsing next day's program: {e}")
            continue

    # Calculate durations based on start times
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs



class TrawlerEmmanuelTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
