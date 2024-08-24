from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago') 
    try:
        response = requests.get(
            "https://hischannel.com/schedule/tv/{}-schedule.html".format(the_date.strftime("%A").lower())
        )
        response.raise_for_status()
    except:
        return []
    
    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for block in soup.find_all("tr"):
        try:
            starts = datetime.datetime.strptime("{} {} -0700".format(the_date.strftime("%Y-%m-%d"), block.contents[1].text.strip()), "%Y-%m-%d %I:%M %p %z")
        except:
            continue 
        starts = starts.astimezone(central_tz)

        if starts.date() == the_date:

            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": 60,
                
                    "program_name": block.contents[3].text.split('\xa0')[0],
                }
            )

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerHisChannel(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
