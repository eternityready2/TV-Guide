from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup

def get_data(the_date):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get("https://ctvn.org/schedule/?_program_guide_date_controls={}".format(the_date.strftime("%Y-%m-%d")), headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        program_elements = soup.find_all('div', class_="wpgb-card-wrapper")
        programs = []

        for program in program_elements:
            program_name_element = program.find('h2', style="font-weight: 500;font-size: 24px;line-height: 36px;")
            if program_name_element:
                program_name = program_name_element.text.strip()
            else:
                program_name = ""
            time_element = program.find('div', class_="ctvn-wpgb-episode-card_meta time-meta")
            if time_element:
                time = time_element.text.strip()
                # Check if duration information is available
                if '-' in time:
                    start_time, duration = time.split('-')
                    start_time = start_time.strip()
                    duration = duration.replace(' minutes', '').strip()
                else:
                    # Skip this program if start_time is empty
                    continue
            else:
               # Skip this program if time_element is not found
               continue

            starts = datetime.datetime.strptime(start_time, "%I:%M %p").strftime("%H%M")

            programs.append({
                "starts": starts,
                "duration": duration,
                "program_name": program_name,
            })

        for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs
                     
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
class TrawlerCornerstone(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule