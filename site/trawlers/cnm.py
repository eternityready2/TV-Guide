from .common import Trawler
import datetime
import requests
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        
        # Fetch schedule data from API
        response = requests.get("https://api.newsmaxtv.com/api/wideorbittimeline/1011/schedule", verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []

    try:
        data = response.json()
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return []

    for show in data:
        try:
            starts = datetime.datetime.strptime("{} -0400".format(show['ShowDateTime']), "%Y-%m-%dT%H:%M:%S %z")
            starts = starts.astimezone(central_tz)
            if starts.date() == the_date:
                programs.append({
                    "starts": starts.strftime("%H%M"),
                    "duration": int(show['ShowDuration'] / 60),
                    "program_name": show['Program'],
                })
        except (KeyError, ValueError) as e:
            print(f"Error processing show data: {e}")
            continue

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerNewsMax(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
