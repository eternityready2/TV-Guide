from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        response = requests.get("https://www.glc.us.com/schedule")
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    day_elements = soup.find_all("li", class_="accordion-item")
    the_day = the_date.strftime("%A")
    for day in day_elements:
        day_name = day.find('span', class_="accordion-item__title").text.strip()
        
        if  day_name ==  the_day:
            program_items = day.find_all('p')
            for item in program_items:
                item_contnt = str(item.text.strip())
                
                program_time = item_contnt[:19]

                program_name = item_contnt[22:]

                start_time, end_time = program_time.split(' - ')
                
                starts = datetime.datetime.strptime("{} {} -0500".format(the_date.strftime('%Y-%m-%d'), start_time), "%Y-%m-%d %I:%M %p %z")
                
                
                programs.append({
                        "starts": starts.strftime("%H%M"),
                        "duration": 60,
                        "program_name": program_name
                    })
    for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs
                   


class TrawlerGLC(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
