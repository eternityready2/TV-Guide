from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date, site):
    central_tz = timezone('America/Chicago')
    try:
        url = f"https://www.tct.tv/watch-tct/tct-{site}/tct-{site}-weekly/"
        response = requests.get(url)
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for tr in soup.find_all("tr"):
        try:
            starts = datetime.datetime.strptime(
                "{} {} -0500".format(tr.contents[1].text, tr.contents[2].text),
                "%m/%d/%Y %I:%M%p %z"
            )
        except:
            continue

        starts = starts.astimezone(central_tz)
        if starts.date() == the_date:
            if tr.contents[4].text == "":
                continue

            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": 30,
                    "program_name": tr.contents[4].text,
                }
            )

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    
    return programs


class Trawlertct(Trawler):
    @staticmethod
    def get_info_for_days(days, site):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day, site)})

        return schedule
