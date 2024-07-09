from .common import Trawler
import datetime
import json
import requests
from pytz import timezone

def get_data(the_date, site):
    try:
        url = f"https://api2-test.3abn.org/sched/daily/{site}/{the_date.strftime('%Y-%m-%d')}/-420"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []

    try:
        data = response.json()
        for item in response.json()['schedule']:
            date_str = item['date']
            starts_datetime = datetime.datetime.fromisoformat(date_str)

            starts = starts_datetime.strftime('%H%M')
            duration = item['duartion'].split(':')[1]

            programs.append({
                "starts": starts,
                "duration": duration,
                "program_name": item["series_title"],
                    })
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class Trawlerc3abnLll(Trawler):
    @staticmethod
    def get_info_for_days(days, site):
        schedule = {}
        for day in days:
            schedule[day.strftime("%Y-%m-%d")] = get_data(day, site)
        return schedule
