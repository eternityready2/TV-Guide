from .common import Trawler

import datetime
import requests
import re
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "https://cycnow.com/weekly-schedule/"
        )
        response.raise_for_status()
    except HTTPError as http_err:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for li in soup.find_all('li', attrs={'itemscope': True}):
        start_span = li.find('span', class_='simcal-event-start')
        starts = datetime.datetime.strptime(start_span['content'].replace('-04:00', '-0400'), "%Y-%m-%dT%H:%M:%S%z")
        starts_pacific = starts.astimezone(timezone('US/Pacific'))
        if starts_pacific.date() != the_date:
            continue

        title = li.find('span', class_='simcal-event-title').text.strip()

        programs.append(
            {
                "date": starts_pacific.strftime("%Y-%m-%d"),
                "starts": starts_pacific.strftime("%H%M"),
                "program_name": title,
                "epoch": int(start_span['data-event-start']),
                "duration": 60
            }
        )

    length = len(programs)
    for i in range(length):
        if i < length-1:
            programs[i]['duration'] = (programs[i+1]['epoch'] - programs[i]['epoch'])/60
        del programs[i]['epoch']

    return programs


class TrawlerCYC(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
