from .common import Trawler

import datetime
import json
import requests
from pytz import timezone


def get_data(the_date):
    try:
        response = requests.get("https://www.presstv.ir/default/GetSchedule?date={}".format(the_date.strftime("%Y-%m-%d")))
        response.raise_for_status()
    except:
        return []

    programs = []

    for show in response.json():
        starts = datetime.datetime.strptime("{} +0000".format(show['gmt']), "%Y-%m-%dT%H:%M:%S %z").astimezone(timezone('US/Pacific'))

        programs.append({
            "starts": starts.strftime("%H%M"),
            "duration": 30,
            
            "program_name": show['prog'].strip(),
        })


    for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerPressTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
