from .common import Trawler
import datetime
import requests
import re
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date,site):
    central_tz = timezone('America/Chicago')
    url = "http://{}.hostedbroadcasting.com/external_schedule/select_calendar_view_day/1?day={}&month={}&year={}".format(site, the_date.day, the_date.month, the_date.year)
    
    try:
        response = requests.get( url,
            headers={"Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"}
        )
        response.raise_for_status()
    except:
        return []
    
    programs = []

    match = re.search(r'(<table class=\\"bigtable\\".*<\\/table>)', response.content.decode('utf8'))
    html = match.group(1).encode('latin1', errors='replace').decode('unicode_escape').replace('<\\/t', '</t')

    soup = BeautifulSoup(html, 'html.parser')
    
    for tr in soup.find_all('tr'):
        children = list(tr.children)
        start = children[1].text.strip().replace(" (previous day)", "")
        
        # Skip the first row if it contains "Time"
        if start.lower() == "time":
            continue
        
        start_time = datetime.datetime.strptime("{} {} -0700".format(the_date.strftime("%Y-%m-%d"), start), "%Y-%m-%d %I:%M %p %z")
        
        durations = children[5].text.split(":")
        duration = int((int(durations[0]) * 60) + int(durations[1]) + (int(durations[2])/60))
        
        starts = start_time.astimezone(central_tz)
        
        if starts.date() == the_date:
            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": duration,
                    "program_name": children[3].text.strip(),
                }
            )
    
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs

class TrawlerCLLBN(Trawler):
    @staticmethod
    def get_info_for_days(days, site):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day, site)})

        return schedule