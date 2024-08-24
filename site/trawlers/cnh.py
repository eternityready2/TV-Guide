from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        response = requests.get("https://newhopetv.org/program-guide/")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tabs = soup.find_all('div', class_="sp-tab__tab-pane")
    
    # Determine the tab index for the given date
    day_tab = (the_date.weekday() + 1) % 7
    day_programs = tabs[day_tab].find_all('tr')

    for tr in day_programs:
        try:
            time_element = tr.find('td')
            time = time_element.text.strip().replace(' :', ':').replace('\n', '')
            program_name = tr.find_all('td')[1].text.strip()
            starts = datetime.datetime.strptime( "{} {} +0530".format(the_date.strftime("%m/%d/%Y"), time), "%m/%d/%Y %I:%M %p %z" )
        except Exception as e:
            print(f"Error parsing time or program name: {e}")
            continue

        starts = starts.astimezone(central_tz)
        if starts.date() == the_date:
            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": 30,
                    "program_name": program_name,
                }
            )
    
    # Handle next day's programs
    day_tab2 = (the_date.weekday() + 2) % 7
    next_day = the_date + datetime.timedelta(days=1)
    day_program2 = tabs[day_tab2].find_all('tr')

    for tr2 in day_program2:
        try:
            time_element2 = tr2.find('td')
            time2 = time_element2.text.strip().replace(' :', ':').replace('\n', '')
            program_name2 = tr2.find_all('td')[1].text.strip()
            starts2 = datetime.datetime.strptime(
                "{} {} +0530".format(next_day.strftime("%m/%d/%Y"), time2),
                "%m/%d/%Y %I:%M %p %z"
            )
        except Exception as e:
            print(f"Error parsing time or program name for next day: {e}")
            continue

        starts2 = starts2.astimezone(central_tz)
        if starts2.date() == the_date:
            programs.append(
                {
                    "starts": starts2.strftime("%H%M"),
                    "duration": 30,
                    "program_name": program_name2,
                }
            )

    # Calculate durations
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
