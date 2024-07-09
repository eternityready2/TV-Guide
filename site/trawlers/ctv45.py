from .common import Trawler
import datetime
import requests
import re
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "https://www.tv45.org/{}".format(the_date.strftime("%A").lower())
        )
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for block in soup.find_all("div", class_="sp-menu-item"):
        start_time = block.find("div", class_="sp-menu-item-price").text
        
        start_time = re.sub(r';', ':', start_time)
        starts = datetime.datetime.strptime("{} {} -0400".format(the_date.strftime("%Y-%m-%d"), start_time.strip()), "%Y-%m-%d %I:%M%p %z")
        title = block.find("div", class_="sp-menu-item-title").text


        programs.append(
            {
                "starts": starts.strftime("%H%M"),
                "duration": 30,
                
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


class TrawlerTV45(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
