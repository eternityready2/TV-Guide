from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone


def get_data(the_date):
    try:
        url = "https://lifeendtimes.tv/#{}".format(the_date.strftime("%A").lower())
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        program_elements = soup.find_all('div', class_='qt-part-show-schedule-day-item')

        
        program_elements_filtered = [program_element for program_element in program_elements
                                     if program_element.find('span', class_='qt-day qt-capfont').text.strip() == the_date.strftime("%A")]
        

        programs = []
        for program_element in program_elements_filtered:
            start_time = program_element.find('span', class_='qt-time').get_text(strip=True)
            am_pm = program_element.find('span', class_='qt-am').get_text(strip=True)
            start_time_am_pm = start_time + am_pm
            starts = datetime.datetime.strptime("{} {} -0600".format(the_date.strftime("%m/%d/%Y"), start_time_am_pm), "%m/%d/%Y %I:%M%p %z")

            if starts.date() != the_date:
                continue

            program_name = program_element.find('a', class_='qt-t').get_text(strip=True)

            programs.append({
                "starts": starts.strftime("%H%M"),
                "duration": 30,  
                "program_name": program_name
            })

        
        for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

class TrawlerKCSETVLifeEnd(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
