from .common import Trawler
import datetime
import requests
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        response = requests.get(
            "https://www1.cbn.com/app_feeds/cbnFamily/liveschedule.php?channel=iptv1&numHours=168&format=json"
        )
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []

    data = response.json()
    for program in data['channel']['programs']:
        # Parse the ISO timestamp and convert it to Central Time
        starts = datetime.datetime.strptime(program.get('isoTimestamp'), "%Y-%m-%dT%H:%M:%S%z")
        starts = starts.astimezone(central_tz)
       
        if starts.date() == the_date:
            program_name = program.get('showName')
            duration = int(program.get('showLengthMinutes', 0))
            
            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": duration,
                    "program_name": program_name,
                }
            )

    # Sort programs by their start time
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs

class TrawlerCBNFamily(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
