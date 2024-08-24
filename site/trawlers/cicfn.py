from .common import Trawler
import datetime
import pandas as pd
from pytz import timezone


def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        dfs = pd.read_html('https://www.icfn.tv/tv-schedule/')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []
    program = {}
    weekday = the_date.weekday() + 1

    for i, row in dfs[0].iterrows():
        # Check if the program is the same as the previous one to combine durations
        if "program_name" in program:
            if program["program_name"] == row.iloc[weekday]:
                program["duration"] += 30
                continue
            else:
                programs.append(program)
                program = {}  # Reset program for the next entry

        # Parse and convert time to Central Time
        starts = datetime.datetime.strptime(f"{the_date.strftime('%Y-%m-%d')} {row.iloc[0]} -0700", "%Y-%m-%d %I:%M %p %z")
        starts = starts.astimezone(central_tz)

        if starts.date() == the_date:
            program = {
                "starts": starts.strftime("%H%M"),
                "duration": 30,
                "program_name": row.iloc[weekday],
            }

    if "program_name" in program:
        programs.append(program)
        
    # Sort programs by start time
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    
    return programs

class TrawlerICFN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule[day.strftime("%Y-%m-%d")] = get_data(day)
        return schedule
