from .common import Trawler

import datetime
import json
import requests
from pytz import timezone

def get_data(the_date):
    try:
        url = ("https://api2-test.3abn.org/sched/daily/lat/{}/-420").format(the_date.strftime("%Y-%m-%d"))
        response = requests.get(url)
        response.raise_for_status()
    except:
        return []

    programs = []

    for item in response.json()["schedule"]:

        date_str = item['date']
        starts_datetime = datetime.datetime.fromisoformat(date_str)

        starts = starts_datetime.strftime('%H%M')
        duration = item['duartion'].split(':')[1]

        programs.append({
            "starts": starts,
            "duration": duration,
            "program_name": item["series_title"],
        })
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class Trawlerc3abnL(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
