from .common import Trawler
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

path='./data/chromedriver-linux64/chromedriver'
def get_data(the_date):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://hopetv.org/schedule/hope-channel?day={}T00%3A00%3A00%2B03%3A00'.format(the_date.strftime("%Y-%m-%d"))
    
    driver.get(url)
    
    allow_button_present = len(driver.find_elements(By.XPATH, "//a[.//span[contains(text(), 'Allow everything')]]")) > 0
    if allow_button_present:
        allow_selected_button = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[contains(text(), 'Allow everything')]]")))
        allow_selected_button.click()
    
    # Wait for the programs to load
    wait = WebDriverWait(driver, 40)
    program_divs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='cursor-pointer group py-1 outline-none transition-all duration-300 ease-in-out z-10 hover:z-30 focus:z-30 ']")))
    
    programs = []
    
    for program_div in program_divs:
        time_element = program_div.find_element(By.CSS_SELECTOR, 'div.text-right').text
        starts = datetime.strptime(time_element, "%I:%M %p").strftime("%H%M")
        program_info_div = program_div.find_element(By.CSS_SELECTOR, 'div.flex-grow')
        program_title = program_info_div.find_element(By.CSS_SELECTOR, 'h3').text
        duration = program_div.find_element(By.CSS_SELECTOR, 'div.md\\:shrink-0 span').text
        duration = duration.replace(' min', '')
        programs.append({
            "starts":  starts,
            "program_name": program_title,
            "duration": duration
        })

    driver.quit()
    programs.sort(key=lambda x: datetime.strptime(x['starts'], "%H%M"))
    return programs 


class TrawlerHopeTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
