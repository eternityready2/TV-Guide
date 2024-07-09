from .common import Trawler
import datetime
import requests
import re
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get(
            "http://llbnsouthasia.hostedbroadcasting.com/external_schedule/select_calendar_view_day/1?day={}&month={}&year={}".format(the_date.day, the_date.month, the_date.year),
            headers={"Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"}
        )
        response.raise_for_status()
    except:
        return []

    programs = []

    match = re.search(r'(<table class=\\"bigtable\\".*<\\/table>)', response.content.decode('utf8'))
    html = match.group(1).encode('latin1', errors='backslashreplace').decode('unicode_escape').replace('<\\/t', '</t')

    soup = BeautifulSoup(html, 'html.parser')

    for tr in soup.find_all('tr'):
        children = list(tr.children)

        try:
            start_time = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), children[1].text.strip()), "%Y-%m-%d %I:%M %p")
        except:
            continue

        durations = children[5].text.split(":")
        duration = int((int(durations[0]) * 60) + int(durations[1]) + (int(durations[2]) / 60))

        programs.append(
            {
                "starts": start_time.strftime("%H%M"),
                "duration": duration,
                "program_name": children[3].text.strip(),
            }
        )
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class Trawlerllbnsouthasia(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
