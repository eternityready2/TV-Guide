from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get("https://newhopetv.org/program-guide/")
        response.raise_for_status()
    except:
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tabs = soup.find_all('div', class_="sp-tab__tab-pane")

    # sunday = 0
    day_tab = (the_date.weekday()+1) % 7
    
    day_programs = tabs[day_tab].find_all('tr')
   
    for tr in day_programs:
        try:
            time_element = tr.find('td')
            time = time_element.text.strip()
            program_name  = tr.find_all('td')[1].text.strip()
            starts = datetime.datetime.strptime("{} {} +0530".format(the_date.strftime("%m/%d/%Y"), time), "%m/%d/%Y %I:%M %p %z").astimezone(timezone('US/Pacific'))
        except:
            continue

        programs.append(
            {
                "starts": starts.strftime("%H%M"),
                "duration": 30,
                "program_name":program_name,
            }
        )

    for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerNewHope(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
