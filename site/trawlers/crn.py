from .common import Trawler

import datetime
import requests
from bs4 import BeautifulSoup

def get_data(the_date):
    try:
        response = requests.get("https://refnet.fm/schedule")
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for li in soup.find('ol', {'id': the_date.strftime("%a").lower()}).find_all('li'):
        try:
            starts = datetime.datetime.strptime("{} {}".format(the_date.strftime("%m/%d/%Y"), li.span.text.strip()), "%m/%d/%Y %I:%M %p")
        except:
            continue

        if starts.date() != the_date:
            continue

        programs.append(
            {
                "starts": starts.strftime("%H%M"),
                "duration": 30,
                "epoch": int(starts.timestamp()),
                "program_name": li.h3.text.strip(),
            }
        )

    for i in range(len(programs)):
        if i < len(programs)-1:
            programs[i]['duration'] = (programs[i+1]['epoch'] - programs[i]['epoch'])/60
        del programs[i]['epoch']
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerRefNet(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
