from .common import Trawler

import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.post(
            "https://daystar.tv/ajax/epg_request.php",
            data={"schedule": 1, "time_zone": "America/Los_Angeles", "type": "livestream"}
        )
        response.raise_for_status()
        schedule_data = response.json()
    except Exception as e:
        print("Error fetching schedule:", e)
        return None

    matching_index = None
    for index, data in enumerate(schedule_data):
        if data['id'] == the_date.strftime("%m-%d-%Y"):
            matching_index = index
            break

    if matching_index is None:
        print("No matching date found in schedule.")
        return []

    programs = []
    for event in schedule_data[matching_index]['events']:
        st = event['datetime']
        st_1 = st.replace('<small>', '').strip()

        

        start_time = datetime.datetime.strptime(st_1, "%I:%M %p").time()
        
        
        
        
        start_time = start_time.strftime("%H%M")
        

        

        programs.append({
            "starts": start_time,
            "program_name": event['name'],
            "duration": 30
        })

    for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerDayStar(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
