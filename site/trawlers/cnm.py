from .common import Trawler

import datetime
import json
import requests
from pytz import timezone
import urllib3

def get_data(the_date):
    try:
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        response = requests.get("https://api.newsmaxtv.com/api/wideorbittimeline/1011/schedule", verify=False)
        response.raise_for_status()
    except:
        return []

    programs = []

    for show in response.json():
        starts = datetime.datetime.strptime("{} -0400".format(show['ShowDateTime']), "%Y-%m-%dT%H:%M:%S %z")
        if starts.date() != the_date:
            continue

        programs.append({
            "starts": starts.strftime("%H%M"),
            "duration": int(show['ShowDuration']/60),
            "program_name": show['Program'],
        })
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerNewsMax(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
