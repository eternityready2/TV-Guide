from .common import Trawler
from pytz import timezone
import requests
import datetime

def get_data(the_date):
    # You should fetch program elements dynamically, instead of using a hard-coded list
    program_elements = ['Positive, encouraging music videos 24/7', 'Positive, encouraging music videos 24/7', 'Positive, encouraging music videos 24/7']
    programs = []

    for i, program_element in enumerate(program_elements):
        if program_element:
            # Extract relevant information from program_element
            program_name = program_element

            # Set start time based on index
            starts = "{:04d}".format(i * 800)

            programs.append({
                "starts": starts,
                "duration": 480,  # Assuming each program has a duration of 8 hours (480 minutes)
                "program_name": program_name
            })
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerSpiritTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
