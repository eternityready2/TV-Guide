from .common import Trawler

import datetime
import requests
import re
import unicodedata
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "https://www.sonbroadcasting.org/{}.html".format(the_date.strftime("%A").lower())
        )
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(str(response.content).replace('<br />', "\n"), 'html.parser')

    paragraph_elements = soup.find_all('div', class_='paragraph')
    if len(paragraph_elements) < 2:
        # If there are not enough paragraph elements, return an empty list
        return []

    for block in unicodedata.normalize("NFKD", paragraph_elements[1].text).split("\n"):
        match = re.search(r'^([0-9]+:[0-9]+[ap]m)-([0-9]+:[0-9]+[ap]m)\s+(.*)', block)
        if not match:
            continue
        start_time = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), match.group(1)), "%Y-%m-%d %I:%M%p")
        start_time = timezone('America/Denver').localize(start_time).astimezone(timezone('US/Pacific'))

        if start_time.date() != the_date:
            continue

        end_time = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), match.group(2)), "%Y-%m-%d %I:%M%p")
        end_time = timezone('America/Denver').localize(end_time).astimezone(timezone('US/Pacific'))
        if end_time < start_time:
            end_time += datetime.timedelta(days=1)

        duration = end_time - start_time

        programs.append(
            {
                "starts": start_time.strftime("%H%M"),
                "duration": int(duration.total_seconds() / 60),
                "program_name": match.group(3),
            }
        )
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs



class TrawlerSB(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
