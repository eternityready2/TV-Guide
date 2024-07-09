from .common import Trawler

import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get("https://www.insp.com/schedule/")
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the correct tab
    tab_id = None
    for span in soup.find('div', class_='list-schedule-top').find_all('span', class_='date'):
        if span.text.strip() == the_date.strftime('%-m-%-d'):
            tab_id = span.parent.attrs['href'].replace('#', '')
            break


    schedule = soup.find('div', id=tab_id)
    for block in schedule.find_all("div", class_="schedule-entry"):
        starts = datetime.datetime.strptime("{} {}m".format(the_date.strftime("%Y-%m-%d"), block.find('div', class_='schedule-time').text.strip()), "%Y-%m-%d %I:%M%p")
        starts = timezone('EST').localize(starts).astimezone(timezone('US/Pacific'))

        if starts.date() != the_date:
            continue

        programs.append({
            "starts": starts.strftime("%H%M"),
            "duration": 30,
            "epoch": int(starts.timestamp()),
            "program_name": block.find('div', class_="episode-title").text.strip()
        })

    for i in range(len(programs)):
        if i < len(programs)-1:
            programs[i]['duration'] = int((programs[i+1]['epoch'] - programs[i]['epoch'])/60)
        del programs[i]['epoch']
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerInsp(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
