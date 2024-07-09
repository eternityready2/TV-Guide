from .common import Trawler

import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get("https://www.revelationtv.com/schedule")
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for block in soup.find_all("div", class_="scheduleprograms-row"):
        try:
            starts = datetime.datetime.strptime("{} {} +0000".format(block.attrs['date'], block.h3.text.split(' ')[0]), "%Y-%m-%d %H:%M %z").astimezone(timezone('US/Pacific'))
        except:
            continue
        title = block.contents[5].h3.text

        if starts.date() != the_date:
            continue

        programs.append(
            {
                "starts": starts.strftime("%H%M"),
                "duration": 30,
                "epoch": int(starts.timestamp()),
                "program_name": title,
            }
        )

    for i in range(len(programs)):
        if i < len(programs)-1:
            programs[i]['duration'] = int((programs[i+1]['epoch'] - programs[i]['epoch'])/60)
        del programs[i]['epoch']
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerRevelationTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
