from .common import Trawler
import datetime
import requests
import re
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date,site):
    central_tz = timezone('America/Chicago')
    try:
        url =  "http://proweb.myersinfosys.com/{}/day?date={}&time_zone=America%2FChicago&nocache=7hmsl".format(site,the_date.strftime("%Y-%m-%d"))
        response = requests.get(url)
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for block in soup.find_all('div', class_="channel-row__block"):
        start_time = block.find("div", class_="channel-row__block--time").text
        starts = datetime.datetime.strptime("{} {} -0500".format(the_date.strftime("%Y-%m-%d"), start_time.strip()), "%Y-%m-%d %I:%M%p %z")

        duration   = int(int(block.find("div", attrs={'data-duration': True})['data-duration'])/60)
        title      = block.find("h3").text

        starts = starts.astimezone(central_tz)

        if starts.date() == the_date:
            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": duration,
                    "program_name": title,
                }
            )
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs


class TrawlerMyersInfoSys(Trawler):
    @staticmethod
    def get_info_for_days(days, site):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day, site)})

        return schedule
