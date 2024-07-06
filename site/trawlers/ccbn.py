from .common import Trawler

import datetime
import requests
import re

from xml.etree import ElementTree
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "https://www1.cbn.com/app_feeds/cbnFamily/liveschedule.php?channel=newsChannel&numHours=168"
        )
        response.raise_for_status()
    except HTTPError as http_err:
        return []

    programs = []

    root = ElementTree.fromstring(response.content)
    for program in root[0][0]:
        starts = datetime.datetime.strptime(program.get('time').replace('-04:00', '-0400'), "%Y-%m-%dT%H:%M:%S%z")
        starts_pacific = starts.astimezone(timezone('US/Pacific'))
        if starts.date() != the_date:
            continue

        m = re.search(r'([0-9]+)H([0-9]+)M', program.get('duration'))
        hour    = int(m.group(1))
        minute  = int(m.group(2))
        duration = hour*60 + minute

        programs.append(
            {
                "date": starts.strftime("%Y-%m-%d"),
                "starts": starts.strftime("%H%M"),
                "duration": duration,
                "program_name": program[0].text,
            }
        )

    return programs


class TrawlerCBN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
