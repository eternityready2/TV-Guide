from .common import Trawler
import datetime
import json
import requests
import pytz

def get_data(the_date):
    # Convert the_date to US/Central time zone
    the_date_us_central = pytz.timezone('US/Central').localize(datetime.datetime.combine(the_date, datetime.datetime.min.time()))

    # Get ts_start 1 day before the_date_us_central
    ts_start = int((the_date_us_central - datetime.timedelta(days=1)).timestamp())

    # Get ts_end 3 days after the_date_us_central
    ts_end = int((the_date_us_central + datetime.timedelta(days=3)).timestamp())

    # Format the URL with the Unix timestamps
    url = f"https://sat7.faulio.com/api/v1/pageblocks/vod_program_grid_page/?ts_start={ts_start}&ts_end={ts_end}"
    
    # Fetch data
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []
    except json.JSONDecodeError as e:
        print("Error parsing JSON data:", e)
        return []

    programs = []

    # Process data
    try:
        for grid_item in data[0]['programgriditemsobjects'][1].get('grid', []):
            timestamp = grid_item.get('dt_stamp')
            utc_datetime = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
            local_date_us_central = utc_datetime.astimezone(pytz.timezone('US/Central')).date()

            if local_date_us_central == the_date:
                starts = utc_datetime.strftime("%H%M")
                duration = int(grid_item.get('duration', 0)) // 60  # Convert duration to minutes
                program_name = grid_item.get('title')

                programs.append({
                    "starts": starts,
                    "duration": duration,
                    "program_name": program_name
                })
    except (KeyError, ValueError) as e:
        print("Error processing data:", e)

    # Sort programs by start time
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs

class TrawlerSAT_7_PARS(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
