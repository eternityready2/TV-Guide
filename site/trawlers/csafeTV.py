from .common import Trawler  
import json
import datetime
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    
    day_of_week = the_date.strftime("%A")
    
    with open('./data/SafeTV_Data.json', 'r') as file:
        data = json.load(file)
    
    programs = []
    
    # Find the schedule for the specific day
    for day_data in data["schedule"]:
        if day_data.get(day_of_week):
            Day = day_data[day_of_week]
            break
    else:
        return programs

    # Extract program details
    for program in Day:
        time_str = program.get("starttime")
        program_name = program.get("program_name")

        if not time_str or not program_name:
            continue  # Skip if any necessary data is missing

        starts = datetime.datetime.strptime(f"{the_date.strftime('%m/%d/%Y')} {time_str} -0500", "%m/%d/%Y %I:%M %p %z")
        starts = starts.astimezone(central_tz)

        if starts.date() == the_date:
            programs.append({
                "starts": starts.strftime("%H%M"),
                "program_name": program_name,
                "duration": 30  # Default duration
            })

    # Calculate duration for each program except the last one
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

    # Sort programs by start time
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs 
        
class TrawlerSafeTv(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
