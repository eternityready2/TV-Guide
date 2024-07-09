from .common import Trawler

import datetime
import requests
from pytz import timezone


def get_data(the_date):
    try:
        response = requests.get(
            "https://www.mnn.org/watch/api/schedule-cache?date={}".format(the_date.strftime("%m/%d/%Y"))
        )
        response.raise_for_status()
    except:
        return []

    programs = []

    for i in response.json()['ch3']:

        starts = datetime.datetime.strptime("{} {} -0400".format(the_date.strftime("%Y-%m-%d"), i['start']), "%Y-%m-%d %H-%M %z")

        

        programs.append(
            {
                "starts": starts.strftime("%H%M"),
                "duration": int(i['duration']),
                "program_name": i["title"],
            }
        )
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerMNN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
