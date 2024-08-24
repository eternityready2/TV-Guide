from .common import Trawler
import datetime
import json
import requests
import pytz


def get_data(the_date):
    # Convert the_date to datetime.datetime object with default time (midnight)
    datetime_with_default_time = datetime.datetime.combine(the_date, datetime.time.min)

    url = "https://tvlistings.gracenote.com/api/sslgrid"

    # Define the payload with the parameters you provided
    payload = {
        "timespan": 336,
        "timestamp": int(datetime_with_default_time.timestamp()),
        "prgsvcid": 74978,
        "headendId": "NY65256",
        "countryCode": "USA",
        "postalCode": "70810",
        "device": "X",
        "userId": "-",
        "aid": "shalomtv",
        "DSTUTCOffset": -240,
        "STDUTCOffset": -300,
        "DSTStart": "2024-03-10T02:00Z",
        "DSTEnd": "2024-11-03T02:00Z",
        "languagecode": "en-us"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()
        a = the_date.strftime("%Y-%m-%d")

        programs = []

        for program in data[a]:
            # Extract relevant information for each program
            start_time_utc = program.get("startTime", 0)
            end_time_utc = program.get("endTime", 0)

            # Convert UTC start and end times to US/Pacific timezone

            start_time = datetime.datetime.fromtimestamp(start_time_utc, pytz.utc).astimezone(pytz.timezone('US/Central'))
            end_time = datetime.datetime.fromtimestamp(end_time_utc, pytz.utc).astimezone(pytz.timezone('US/Central'))

            local_date_us_central = start_time.date()

            if local_date_us_central == the_date:
                starts = start_time.strftime("%H%M")
                duration = int((end_time - start_time).total_seconds() / 60)

                program_name = program.get("program", {}).get("title", "")
                    
                programs.append({
                    "starts": starts,
                    "duration": duration,
                    "program_name": program_name
                })
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))      
        return programs

    except requests.RequestException as e:
        print("Request failed for date: %s\nwith error:%s" % (the_date, e))
        return None

class TrawlerJewishB(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
