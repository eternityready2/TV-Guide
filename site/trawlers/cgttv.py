from .common import Trawler

import datetime
import json
import requests
import re
from pytz import timezone


def get_data(the_date):
    try:
        response = requests.get(
            "https://www.gospeltruth.tv/wp-content/plugins/ott/extensions/optional/schedule/schedule.js"
        )
        response.raise_for_status()
    except HTTPError as http_err:
        return []

    programs = []

    # get the titles
    titles = []
    m = re.search(r'let titles = \[(.+?)\];', response.text)
    for t in m.group(1).split(', '):
        titles.append(t.strip("'").replace("\\'","'"))

    # get startTimesU
    m = re.search(r'let startTimesU = (\[.+?\]);', response.text)
    start_times = json.loads(m.group(1).replace("'", ''))

    # get endTimesU
    m = re.search(r'let endTimesU = (\[.+?\]);', response.text)
    end_times = json.loads(m.group(1).replace("'", ''))

    for i in range(len(start_times)):
        if titles[i] == "":
            continue

        this_date = datetime.datetime.fromtimestamp(start_times[i])
        this_date_pacific = this_date.astimezone(timezone('US/Pacific'))
        if this_date_pacific.date() != the_date:
            continue
        programs.append(
            {
                "date": this_date_pacific.strftime("%Y-%m-%d"),
                "starts": this_date_pacific.strftime("%H%M"),
                "duration": int((end_times[i] - start_times[i])/60),
                "program_name": titles[i],
            }
        )

    return programs


class TrawlerGospelTruthTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
