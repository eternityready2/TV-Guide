from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    programs = []
    wanted_date = the_date
    s = requests.Session()

    for i in range(2):
        the_date = wanted_date + datetime.timedelta(days=i)
        try:
            data={
                'event_schedule_additional[ed_date]': the_date.strftime("%d/%m/%Y"),
                'event_schedule[keywords]': '',
                'event_schedule[desktop_go]': 'Search',
                'event_schedule[advanced]': 1,
                'event_schedule_controls[contains_all]': 'yes',
                'event_schedule[e_series_id]': 0
            }
            response = s.post(
                "https://www.firstlight.org.nz/schedule/?format=listing&advanced=0",
                data=data,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/86.0.4240.75 Safari/537.36',
                },
            )
            response.raise_for_status()
        except:
            return []


        soup = BeautifulSoup(response.content, 'html.parser')
        for block in soup.find_all('tr', class_="scheduled_event"):
            event_time = block.find('td', class_='event_time')

            starts = datetime.datetime.strptime("{} {} +1200".format(the_date.strftime("%Y-%m-%d"), event_time.text.strip()), "%Y-%m-%d %I:%M %p %z")
            
            if starts.date() != wanted_date:
                continue

            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": 30,
                    
                    "program_name": block.find('td', class_='event_series').text.strip(),
                }
            )

    for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerFirstLight(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
