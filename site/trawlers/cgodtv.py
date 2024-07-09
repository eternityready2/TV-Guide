from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone
import re

def parse_date_string(date_str):
    # Define a dictionary to convert month names to numbers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Extract day and month using regular expressions
    match = re.search(r'(\d+)(?:st|nd|rd|th)? of (\w+)', date_str)
    if match:
        day = int(match.group(1))
        month = month_map[match.group(2)]
        year = datetime.datetime.now().year  # Use current year
        return datetime.datetime(year, month, day).date()
    elif "Today" in date_str:
        return datetime.datetime.now().date()
    else:
        return None

def get_data(the_date, site):
    try:
        response = requests.get(f'https://ott.god.tv/schedule.php?r={site}')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
    except Exception as e:
        print("Error:", e)
        return []

    programs = []

    schedule_days = soup.find_all('div', class_='col-xs-12 lighter-grey border-bottom-3-white')

    for schedule_day in schedule_days:
        program_divs = schedule_day.find_all('div', class_="container border-bottom-1-light-grey")
        day = schedule_day.find('h3', class_="text-black").text.strip()
        parsed_date = parse_date_string(day)
        
        if parsed_date == the_date:
            for program_div in program_divs:
                starts_p_element = program_div.find('p', class_="text-black font-size-48 line-height-48")
                if starts_p_element:
                    starts_text = starts_p_element.text.strip()
                    starts_text = starts_text.replace('PM', '').replace('AM', '').replace(':', '').strip()
                    
                    program_name = program_div.find('h3', class_="text-black font-size-18").text.strip()
                    programs.append({
                        "starts": starts_text,
                        "duration": 30,
                        "program_name": program_name,
                    })

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs
class TrawlerGodTV(Trawler):
    @staticmethod
    def get_info_for_days(days, site):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day, site)})

        return schedule
