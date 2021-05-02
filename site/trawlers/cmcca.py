from .common import Trawler

import datetime
import requests
import re
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "https://miraclechannel.ca/schedule/"
        )
        response.raise_for_status()
    except HTTPError as http_err:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    wanted_weekday = the_date.weekday()
    skip = [0,0,0,0,0,0,0]
    for row in soup.find_all('table', class_="tt_timetable")[1].find_all('tr'):
        # cells contains
        # [time] - mon, tue, wed, thu, fri, sat, sun
        cells = row.find_all('td')

        index = 1
        for day in range(7):
            if skip[day] > 0:
                skip[day] -= 1
                continue

            if cells[index].has_attr('rowspan'):
                skip[day] = int(cells[index]['rowspan'])-1

            if wanted_weekday == day:
                starts = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), cells[0].text.strip()), "%Y-%m-%d %I:%M %p")
                starts = timezone('MST').localize(starts).astimezone(timezone('US/Pacific'))
                duration = 30
                if cells[index].has_attr('rowspan'):
                    duration = 30 * int(cells[index]['rowspan'])

                if starts.date() != the_date:
                    continue

                programs.append({
                    "date": starts.strftime("%Y-%m-%d"),
                    "starts": starts.strftime("%H%M"),
                    "duration": duration,
                    "program_name": cells[index].find('a', class_='event_header').text.strip()
                })

            index += 1

    return programs


class TrawlerMiracleChannel(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
