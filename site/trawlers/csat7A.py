from .common import Trawler
import datetime
import json
import requests
import pytz

def get_data(the_date):
    # Convert the_date to US/Pacific time zone
    the_date_us_pacific = pytz.timezone('US/Pacific').localize(datetime.datetime.combine(the_date, datetime.datetime.min.time()))

    # Get ts_start 3 days before the_date_us_pacific
    ts_start = int((the_date_us_pacific - datetime.timedelta(days=1)).timestamp())

    # Get ts_end 3 days after the_date_us_pacific
    ts_end = int((the_date_us_pacific + datetime.timedelta(days=3)).timestamp())

    # Format the URL with the Unix timestamps
    url = f"https://sat7.faulio.com/api/v1/pageblocks/vod_program_grid_page/?ts_start={ts_start}&ts_end={ts_end}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    data = response.json()

    programs = []

    try:
        for grid_item in data[0]['programgriditemsobjects'][0].get('grid', []):
            
            timestamp = grid_item.get('dt_stamp')
            utc_datetime = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
            local_date = utc_datetime.astimezone(pytz.timezone('US/Pacific')).date()

            if local_date == the_date:
                starts = utc_datetime.strftime("%H%M")
                duration = int(grid_item.get('duration', 0)) // 60  # Convert duration to minutes and remove decimals
                program_name = grid_item.get('title')

                programs.append({
                    "starts": starts,
                    "duration": duration,
                    "program_name": program_name
                })
    except Exception as e:
        print("Error processing data:", e)
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs



class TrawlerSAT_7_ARABIC(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
