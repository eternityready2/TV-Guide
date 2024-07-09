from .common import Trawler
import requests
from bs4 import BeautifulSoup
import datetime

def get_data(the_date):
    try:
        url = "https://missiontv.com/category/missiontv-live/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all program elements with class 'qt-part-show-schedule-day-item'
        cont = soup.find('ul', id="menu-cat-new")
        programs_a = cont.find_all('li', class_="menu-item")
        
        programs = []

        for i, program in enumerate(programs_a):
            if program:
                # Extract relevant information from program_element
                program_name = program.text.strip()
                # Calculate start time based on index and convert to 24-hour clock system
                starts_hour = (i * 80) // 60  # Calculate hour
                starts_minute = (i * 80) % 60  # Calculate minute
                starts = "{:02d}{:02d}".format(starts_hour, starts_minute)

                programs.append({
                    "starts": starts,
                    "duration": 80,  
                    "program_name": program_name
                })
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

class TrawlercMission(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            # Pass the date to get_data function
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})
        return schedule
