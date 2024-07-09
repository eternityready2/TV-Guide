from .common import Trawler

import datetime
import json
import requests
from pytz import timezone


def get_data(the_date):
    try:
        response = requests.get("https://www.rt.com/schedulejson/news/{}".format(the_date.strftime("%d-%m-%Y")))
        response.raise_for_status()
    except:
        return []

    programs = []

    for show in response.json():
        starts = datetime.datetime.strptime("{} {} +0000".format(the_date.strftime("%Y-%m-%d"), show['timeLabel']), "%Y-%m-%d %H:%M %z").astimezone(timezone('US/Pacific'))
        

        title = show['programTitle']
        if 'telecastTitle' in show:
            title += ": " + show['telecastTitle']

        programs.append({
            "starts": starts.strftime("%H%M"),
            "duration": 30,
            "program_name": title,
        })

    # Adjusting the duration of programs
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerRT(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
