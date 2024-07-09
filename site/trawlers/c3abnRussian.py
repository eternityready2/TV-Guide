from .common import Trawler
from bs4 import BeautifulSoup
import requests
import datetime

def get_data(the_date):
    
    base_url = "https://www.3angels.ru/ajx/tvschedule/site/3/{}/0.1".format(the_date.strftime("%Y/%m/%d"))
    
    response = requests.get(base_url)
    response.raise_for_status()

    
    soup = BeautifulSoup(response.content, 'html.parser')

    
    rows = soup.find_all('tr')
    

    programs = []

    for row in rows:
        try:
            time_element = row.find('td', class_='scheduleTime')
            program_element = row.find('td', class_='schedulePName')
            
            if program_element:
                program_name = program_element.find('br').next_sibling.strip()
            if time_element: 
                time_1 =  time_element.text.strip().replace(':', '')
                # Padding single digit hour with zero
                if len(time_1) == 3:
                    time_1 = '0' + time_1
                start = datetime.datetime.strptime("{} {}".format(the_date.strftime("%Y-%m-%d"), time_1), "%Y-%m-%d %H%M")               

                programs.append({
                    'starts': start.strftime("%H%M"),
                    'program_name': program_name,
                    'duration': 40  
                })
        except Exception as e:
            print(f"Error: {e}")
    for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
     
            programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlercRussian(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule