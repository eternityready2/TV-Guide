from .common import Trawler

import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "https://www.family.ca/watch/?d={}".format(the_date.strftime("%Y-%m-%d"))
        )
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for article in soup.find_all("article", class_="ditdw-horizontal-item"):
        start_time = article.find("div", class_="ditdw-show-time").text
        starts = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), start_time.strip()), "%Y-%m-%d %I:%M%p")
        title = article.find("h3").text

        if starts.date() != the_date:
            continue

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


class TrawlerFamilyTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
