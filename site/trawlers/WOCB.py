from .common import Trawler
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import datetime
import pytz

path='./data/chromedriver-linux64/chromedriver'
def get_data(the_date):
    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Emulate human-like behavior
    driver.implicitly_wait(random.randint(4, 5))  # Add random wait time before actions

    url = 'https://www.qvc.com/content/programguide.weekly.html'
    driver.get(url)
    # Wait for the page to fully render
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "showList")))

    page_so = driver.page_source 

    # Use BeautifulSoup to parse the HTML 
    soup = BeautifulSoup(page_so, 'html.parser')        

    programs = []
    block = soup.find('div', class_="showList")
    shows = block.find_all("li", attrs={"data-starttime": True})
    
    for show in shows:
        start_time = show["data-starttime"]
        start_time_pacific = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z").astimezone(pytz.timezone("US/Pacific"))
        program_name = show.find('h3').text.strip()

        if start_time_pacific.date() == the_date:
            program_name = show.find('h3').text.strip()
            programs.append({
                "starts": start_time_pacific.strftime("%H%M"),
                "duration": 30, 
                "program_name": program_name,
            })

    # Calculate program durations
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    driver.quit()
    programs.sort(key=lambda x: datetime.strptime(x['starts'], "%H%M"))
    return programs

class Trawlerwocb(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
