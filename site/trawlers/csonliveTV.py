
from .common import Trawler
import datetime
import json
import requests
import pytz
from datetime import datetime, timezone, time



def get_data(the_date):
    
    datetime_with_default_time = datetime.combine(the_date, time.min)

    url = "https://tvlistings.gracenote.com/api/sslgrid"

   
    payload = {
        "timespan": 336,
        "timestamp": int(datetime_with_default_time.timestamp()),
        "prgsvcid": 42745,
        "headendId": "NY65256",
        "countryCode": "USA",
        "postalCode": "70810",
        "device": "X",
        "userId": "-",
        "aid": "sonlifejsm",
        "DSTUTCOffset": -300,
        "STDUTCOffset": -360,
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
           
            start_time_utc = program.get("startTime", 0)
            end_time_utc = program.get("endTime", 0)

           
            start_time = datetime.fromtimestamp(start_time_utc, pytz.utc).astimezone(pytz.timezone('US/Pacific'))
            end_time = datetime.fromtimestamp(end_time_utc, pytz.utc).astimezone(pytz.timezone('US/Pacific')) 
            
            starts = start_time.strftime("%H%M")
            duration = int((end_time - start_time).total_seconds() / 60)

            program_name = program.get("program", {}).get("title", "")
                
            programs.append({
                "starts": starts,
                "duration": duration,
                "program_name": program_name
            })
        programs.sort(key=lambda x: datetime.strptime(x['starts'], "%H%M"))     
        return programs

    except requests.RequestException as e:
        print("Request failed:", e)
        return None

class TrawlercsonliveTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
