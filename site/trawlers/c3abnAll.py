from .common import Trawler
import datetime
import json
import requests
from pytz import timezone

def get_data(the_date, site):
    central_tz = timezone('America/Chicago')
    
    try:
        # Format URLs
        url1_date_str = the_date.strftime('%Y-%m-%d')
        url1 = f"https://api2-test.3abn.org/sched/daily/{site}/{url1_date_str}/-420"
        
        # Calculate the date for url2 (the day after)
        url2_date_str = (the_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        url2 = f"https://api2-test.3abn.org/sched/daily/{site}/{url2_date_str}/-420"
        
        # Fetch data from both URLs
        response1 = requests.get(url1)
        response1.raise_for_status()
        response2 = requests.get(url2)
        response2.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []

    try:
        # Combine JSON responses from both URLs
        responses = [response1.json(), response2.json()]
        for response in responses:
            for item in response.get('schedule', []):
                date_str = item['date']
                
                starts_datetime = datetime.datetime.fromisoformat(date_str)
                
                # Convert start time to Central Time
                starts_datetime = starts_datetime.astimezone(central_tz)
                
                if starts_datetime.date() == the_date:
                    starts = starts_datetime.strftime('%H%M')
                    duration = item['duartion'].split(':')[1]

                    programs.append({
                        "starts": starts,
                        "duration": duration,
                        "program_name": item.get("series_title", "Unknown"),
                    })
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # Sort programs by start time
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class Trawlerc3abnLll(Trawler):
    @staticmethod
    def get_info_for_days(days, site):
        schedule = {}
        for day in days:
            schedule[day.strftime("%Y-%m-%d")] = get_data(day, site)
        return schedule

