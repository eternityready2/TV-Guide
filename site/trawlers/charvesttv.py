from .common import Trawler

import datetime
import json
import requests
from pytz import timezone

def get_data(the_date):
    try:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': 'https://harvesttv.in/schedule/',
            'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.get("https://harvesttv.in/wp-admin/admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=7755&target_action=get-all-data&default_sorting=new_first", headers=headers)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []

    the_day = the_date.strftime("%A").lower()

    for item in response.json():
        show = item['value']
        program_name = show[the_day]
        ist_time = show['ist_time']
        ist_time = ist_time.replace('.', ':')
        
        # Convert IST time to UTC time
        start_time_str = f"{the_date} {ist_time} +05:30"
        ist_start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %I:%M %p %z")
        utc_start_time = ist_start_time.astimezone(timezone('UTC'))
        
        # Convert UTC time to US/Pacific time
        pacific_start_time = utc_start_time.astimezone(timezone('US/Pacific'))
        
        programs.append({
            "starts": pacific_start_time.strftime("%H%M"),
            "duration": 30,  # Assuming each program is 30 minutes long, you can adjust this based on your data
            "program_name": program_name,
        })
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerHarvestTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
