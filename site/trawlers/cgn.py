from .common import Trawler
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_data(the_date):
    url = "https://loveworldsat.org/schedule/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    day = the_date.strftime("%A")

    block = soup.find('tbody')
    if block is None:
        return []

    rows = block.find_all('tr')
    programs = []

    for row in rows:
        try:
            if day == 'Monday':
                elements= row.find('td', {"data-column-id": "842"})
            elif day == 'Tuesday':
                elements = row.find('td', {"data-column-id": "851"})
            elif day == 'Wednesday':
                elements = row.find('td', {"data-column-id": "852"})
            elif day == 'Thursday':
                elements = row.find('td', {"data-column-id": "853"})
            elif day == 'Friday':
                elements = row.find('td', {"data-column-id": "854"})
            elif day == 'Saturday':
                elements = row.find('td', {"data-column-id": "857"})
            elif day == 'Sunday':
                elements = row.find('td', {"data-column-id": "858"})
            
            if elements:
                program_name = elements.find('a', class_="event-title")
                if program_name:
                    program_name = program_name.text.strip()
                time_starts = elements.find('time', class_="timeslot-start")
                if time_starts:
                    time_starts = time_starts.get("datetime")
                    time_starts = time_starts.replace(':','')
                    start = datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), time_starts), "%Y-%m-%d %H%M")
                
                    programs.append({
                        'starts':  start.strftime("%H%M"),
                        'program_name': program_name,
                        'duration': 40  
                    })
        except Exception as e:
            print(f"Error: {e}")
    
    # Calculate duration between programs
    for i in range(len(programs) - 1):
            start_time_next = datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlerLoveWorld(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule