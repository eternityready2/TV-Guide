from .common import Trawler
import datetime
import json
import requests
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    programs = []

    # Fetch data for the given date
    try:
        response = requests.get("https://www.rt.com/schedulejson/news/{}".format(the_date.strftime("%d-%m-%Y")))
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {the_date}: {e}")
        return []

    for show in response.json():
        try:
            starts = datetime.datetime.strptime("{} {} +0300".format(the_date.strftime("%Y-%m-%d"), show['timeLabel']), "%Y-%m-%d %H:%M %z")
            title = show['programTitle']
            if 'telecastTitle' in show:
                title += ": " + show['telecastTitle']
            starts = starts.astimezone(central_tz)
            if starts.date() == the_date:
                programs.append({
                    "starts": starts.strftime("%H%M"),
                    "duration": 30,
                    "program_name": title,
                })
        except KeyError as e:
            print(f"Missing data in show: {e}")
            continue

    # Fetch data for the next day
    next_day = the_date + datetime.timedelta(days=1)
    try:
        response2 = requests.get("https://www.rt.com/schedulejson/news/{}".format(next_day.strftime("%d-%m-%Y")))
        response2.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {next_day}: {e}")
        return programs

    for show2 in response2.json():
        try:
            starts2 = datetime.datetime.strptime("{} {} +0300".format(next_day.strftime("%Y-%m-%d"), show2['timeLabel']), "%Y-%m-%d %H:%M %z")
            title2 = show2['programTitle']
            if 'telecastTitle' in show2:
                title2 += ": " + show2['telecastTitle']
            starts2 = starts2.astimezone(central_tz)
            if starts2.date() == the_date:
                programs.append({
                    "starts": starts2.strftime("%H%M"),
                    "duration": 30,
                    "program_name": title2,
                })
        except KeyError as e:
            print(f"Missing data in show2: {e}")
            continue

    # Adjust the duration of programs
    for i in range(len(programs) - 1):
        try:
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        except ValueError as e:
            print(f"Error calculating duration: {e}")
            continue

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs

class TrawlerRT(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})
        return schedule
