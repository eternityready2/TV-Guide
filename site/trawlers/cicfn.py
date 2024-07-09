from .common import Trawler

import datetime
import pandas as pd
from pytz import timezone

def get_data(the_date):
    try:
        dfs = pd.read_html('https://www.icfn.tv/tv-schedule/')
    except:
        return []

    programs = []
    program = {}
    weekday = the_date.weekday() + 1

    for i,row in dfs[0].iterrows():
        if "program_name" in program:
            if program["program_name"] == row.iloc[weekday]:
                program["duration"] += 30
                continue
            else:
                programs.append(program)

        starts = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), row.iloc[0]), "%Y-%m-%d %I:%M %p")
        program = {
            "starts": starts.strftime("%H%M"),
            "duration": 30,
            "program_name": row.iloc[weekday],
        }

    if "program_name" in program:
        programs.append(program)
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerICFN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
