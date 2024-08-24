from .common import Trawler
import datetime
import pandas as pd
from pytz import timezone

def get_data(the_date):
    try:
        dfs = pd.read_html('https://gospel.tv/watch/europe/schedule/')
    except:
        return []

    programs = []
    program = {}
    # table starts at sunday = 1, monday = 2, ...
    weekday = ( (the_date.weekday()+1) % 7 ) + 1

    for i,row in dfs[0].iterrows():
        if "program_name" in program:
            if program["program_name"] == row[weekday]:
                program["duration"] += 30
                continue
            else:
                programs.append(program)

        starts = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), row[0]), "%Y-%m-%d %I:%M %p")
        starts = timezone('Europe/London').localize(starts).astimezone(timezone('US/Pacific'))

        if starts.date() != the_date:
            continue

        program = {
            "starts": starts.strftime("%H%M"),
            "duration": 30,
            "program_name": row[weekday],
        }

    if "program_name" in program:
        programs.append(program)
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerGospelTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
