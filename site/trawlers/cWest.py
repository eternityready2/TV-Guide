from .common import Trawler
import requests
from bs4 import BeautifulSoup
import datetime

def get_data(the_date):
    try:
        url = "https://thewesternschannel.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all program elements with class 'qt-part-show-schedule-day-item'
        program_elements1 = soup.find('div', id="n2-ss-3item3")
        program_elements2 = soup.find('div', id="n2-ss-3item4")
        program_elements3 = soup.find('div', id="n2-ss-3item5")

        programs = []

        for program_elements in [program_elements1, program_elements2, program_elements3]:
            if program_elements:
                # Extract relevant information from program_element
                program_name = program_elements.text.strip()

                if program_elements == program_elements1:
                    starts = "0000"
                elif program_elements == program_elements2:
                    starts = "0800"
                elif program_elements == program_elements3:
                    starts = "1600"

                programs.append({
                    "starts": starts,
                    "duration": 480,  # Assuming each program has a duration of 8 hours (480 minutes)
                    "program_name": program_name
                })
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []
class TrawlercWesternChannel(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            # Pass the date to get_data function
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})
        return schedule
