from .common import Trawler
from urllib.error import HTTPError
import datetime
import json
import requests
from pytz import timezone


def get_data(the_date):
    try:
        response = requests.post("https://tvlistings.gracenote.com/api/sslgrid", {
            'aid': 'loveworld',
            'prgsvcid': '105349',
            'timespan': '336',
            'timestamp': int((datetime.datetime.today() - datetime.timedelta(days=1)).timestamp()),
            'headendId': 'NY65256',
            'countryCode': 'USA',
        })
        response.raise_for_status()
    except HTTPError as http_err:
        return []

    programs = []

    for key in response.json().keys():
        for show in response.json()[key]:
            starts = datetime.datetime.strptime(show['org'], "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone('US/Pacific'))
            if starts.date() != the_date:
                continue

            programs.append({
                "date": starts.strftime("%Y-%m-%d"),
                "starts": starts.strftime("%H%M"),
                "duration": int((show['endTime'] - show['startTime'])/60),
                "program_name": show['program']['title'],
            })

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerLoveWorld(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
