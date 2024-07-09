from .common import Trawler
import datetime
import pandas as pd
from pytz import timezone

def get_data(the_date):
    try:
        dfs = pd.read_html('http://thewalk.tv/schedule/')
    except:
        return []

    programs = []

    # site uses sun-sat, python does mon-sun
    day_index = (the_date.weekday()+1)%7

    program = {}

    for i in range(4,len(dfs[0][0])-2):
        if "program_name" in program:
            if program["program_name"] == dfs[0][4+day_index][i]:
                program["duration"] += 30
                continue
            else:
                programs.append(program)

        starts = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), dfs[0][0][i]), "%Y-%m-%d %I:%M %p")
        program = {
            "starts": starts.strftime("%H%M"),
            "duration": 30,
            "program_name": dfs[0][4+day_index][i],
        }

    if "program_name" in program:
        programs.append(program)
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerTheWalk(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
