from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get("https://tbn.uk/tv-guide/{}/".format(the_date.strftime("%Y-%m-%d")), headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        program_elements = soup.find_all('div', class_="flex flex-wrap items-center")
        time_elements = soup.find_all('div', class_="row-span-6")
        
        programs = []
        
        for time_element, program in zip(time_elements, program_elements):
            time_text_element = time_element.find('time')
            if time_text_element:
                time_text = time_text_element.text.strip()
                program_name = program.find('a', class_="inline-block font-demi text-base title mr-4").text.strip()
                duration = program.find('div', class_="text-xs md:mr-4").text.strip()
                duration = duration.replace(' minutes', '').strip()

                starts = datetime.datetime.strptime("{} {} -0000".format(the_date.strftime("%Y-%m-%d"), time_text), "%Y-%m-%d %I:%M %p %z")
      
                starts = starts.astimezone(central_tz)
                
                if starts.date() == the_date:

                    programs.append({
                        "starts": starts.strftime("%H%M"),
                        "duration": duration,
                        "program_name": program_name,
                    })
            else:
                print("Time text element not found for program:", program.find('a', class_="inline-block font-demi text-base title mr-4").text.strip())


        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs
                     
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    
class TrawlerNjetaTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule