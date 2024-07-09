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
import time

path='./data/chromedriver-linux64/chromedriver'
def get_data(the_date):
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    
    driver.implicitly_wait(random.randint(5, 7))  

    url = 'https://inspiration.org/tv/livestream#schedule'
    driver.get(url)

    
   
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "schedule-entry")))

    page_source = driver.page_source 

    
    soup = BeautifulSoup(page_source, 'html.parser')

    tab = soup.find('div', id="schedule-tabs-est-0")

    program_divs = tab.find_all('div', class_="schedule-entry")
    programs = []

    for program_div in program_divs:
      
        time.sleep(random.uniform(1, 2))  

        time_element = program_div.find('div', class_="schedule-time").text
        time_4 = datetime.strptime(time_element, "%I:%M%p").strftime("%H%M")
     
        program_title = program_div.find('div', class_="schedule-show").text

        programs.append({
            "starts": time_4,
            "program_name": program_title,
            "duration": 30  
        })
    
    for i in range(len(programs) - 1):
        start_time_next = datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

   
    driver.quit()
    programs.sort(key=lambda x: datetime.strptime(x['starts'], "%H%M"))
    return programs 


class Trawlerinsptv(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule