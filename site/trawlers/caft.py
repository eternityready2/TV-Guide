from .common import Trawler

from pytz import timezone
import requests
import datetime
from bs4 import BeautifulSoup

def get_data(the_date):
    try:
        
        week_number = the_date.strftime("%W")
        day_of_week_number = the_date.strftime("%w")
        
        base_url = f"https://www.amazingfacts.org/media-library/program-schedule/d/{day_of_week_number}/w/{week_number}{the_date.year}"
        
        
        response = requests.get(base_url)
        response.raise_for_status()

        
        programs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('tbody')
        table_rows = table.find_all('tr')
        
        for tr in table_rows:
            try:
                
                start_time_str = tr.find_all('td')[0].text
                starts = datetime.datetime.strptime("{} {} -0800".format(the_date.strftime("%Y-%m-%d"), start_time_str), "%Y-%m-%d %I:%M %p %z").astimezone(timezone('US/Pacific'))
                starts = datetime.datetime.strptime("{} {} -0800".format(the_date.strftime("%Y-%m-%d"), start_time_str), "%Y-%m-%d %I:%M %p %z").astimezone(timezone('US/Pacific'))
                
                program_name = tr.find_all('td')[1].get_text(strip=True)

                programs.append({
                    "starts": starts.strftime("%H%M"),
                    "duration": 30,  
                    "program_name": program_name
                })

            except Exception as e:
                print("Error:", e)

              

       
        for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = ( start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs

    except Exception as e:
        print("Error:", e)
        return None
                

class TrawlerAmazingFactsTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
