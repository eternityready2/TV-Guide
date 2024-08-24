from .common import Trawler
import datetime
import requests
import re
from xml.etree import ElementTree
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        response = requests.get(
            "https://www1.cbn.com/app_feeds/cbnFamily/liveschedule.php?channel=newsChannel&numHours=400"
        )
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []

    root = ElementTree.fromstring(response.content)
    for program in root[0][0]:
        starts = datetime.datetime.strptime(program.get('time'), "%Y-%m-%dT%H:%M:%S%z")
        starts = starts.astimezone(central_tz)

        if starts.date() == the_date:
            m = re.search(r'([0-9]+)H([0-9]+)M', program.get('duration'))
            hour = int(m.group(1))
            minute = int(m.group(2))
            duration = hour * 60 + minute

            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": duration,
                    "program_name": str(program[0].text),
                }
            )
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlerCBN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
