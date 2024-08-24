from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        response = requests.get("https://cycnow.com/weekly-schedule/")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    programs_elements = soup.find_all('li', class_="simcal-event simcal-event-recurring simcal-events-calendar-423 simcal-tooltip")
    
    for li in programs_elements:
        start_span = li.find('span', class_='simcal-event-start')
        starts = datetime.datetime.strptime(start_span['content'].replace('-04:00', '-0400'), "%Y-%m-%dT%H:%M:%S%z")
        starts = starts.astimezone(central_tz)

        if starts.date() == the_date:

            title = li.find('span', class_='simcal-event-title').text.strip()

            programs.append({
                "starts": starts.strftime("%H%M"),
                "program_name": title,
                "duration": None  # Placeholder for duration calculation
            })

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlerCYC(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
