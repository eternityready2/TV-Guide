from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get("https://geb.tv/schedule/")
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    the_day = the_date.strftime("%A").lower()

    # Check if the day's schedule is available
    day_schedule = soup.find("div", {"id": "{}-row".format(the_day)})
    if not day_schedule:
        print("No schedule available for", the_day)
        return []

    for block in day_schedule.find_all('div', class_="item"):
        # Check if the block contains information
        if not block.find("span"):
            continue
        
        start_time = block.find("span").text
        title = block.text.replace(start_time, '').strip()

        starts = datetime.datetime.strptime("{} {} -0400".format(the_date.strftime("%Y-%m-%d"), start_time.strip()), "%Y-%m-%d (%I:%M%p) %z")

       

        duration = 30

        programs.append(
            {
                "starts": starts.strftime("%H%M"),
                "duration": duration,
                "program_name": title,
            }
        )

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs
    


class TrawlerGEB(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
