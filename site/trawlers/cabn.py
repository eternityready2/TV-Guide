from .common import Trawler

import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.get("https://www.abnchannel.net/schedule.php")
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    swiper_divs = soup.find_all('div', class_='swiper-slide')
    
    day_div = swiper_divs[the_date.weekday()]

   
    for li in day_div.find_all('li'):
        try:
            start_time = li.find('div', string=lambda s: s and s.startswith('Start')).text.replace('Start: ', '').strip()
            end_time = li.find('div', string=lambda s: s and s.startswith('End')).text.replace('End: ', '').strip()
            program_name_unfiltered = li.find('div', class_='cell-s-6').text.strip()
            program_name = program_name_unfiltered.replace('Programme: ', '').strip()

            start_time_1 = start_time.replace('.', ':')
            end_time_1 = end_time.replace('.', ':')

            start_time_2 = start_time_1.replace('00:', '12:')
            end_time_2 = end_time_1.replace('00:', '12:')


            

            
            start_time_3 = start_time_2.replace('AM', ' AM').replace('PM', ' PM')
            end_time_3 = end_time_2.replace('AM', ' AM').replace('PM', ' PM')

            

            starts = datetime.datetime.strptime("{} {} +0100".format(the_date.strftime('%Y-%m-%d'), start_time_3), "%Y-%m-%d %I:%M %p %z").astimezone(timezone('US/Pacific'))
            ends = datetime.datetime.strptime("{} {} +0100".format(the_date.strftime('%Y-%m-%d'), end_time_3), "%Y-%m-%d %I:%M %p %z").astimezone(timezone('US/Pacific'))

            programs.append({
                "starts": starts.strftime("%H%M"),
                "duration": int((ends - starts).total_seconds() / 60),
                "program_name": program_name,
            })
        except Exception as e:
            print("Error parsing program:", e)
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs



class TrawlerABN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
