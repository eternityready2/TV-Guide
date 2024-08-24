from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone
import re


def get_data(the_date, site):
    central_tz = timezone('America/Chicago') 
    try:

        response = requests.get(f'https://ott.god.tv/schedule.php?r={site}')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
    except Exception as e:
        print("Error:", e)
        return []

    programs = []

    schedule_days = soup.find_all('div', class_='col-xs-12 lighter-grey border-bottom-3-white')
    if site == "as":
        timezone_str = "+0530"
    elif site == "af":
        timezone_str = "+0200"
    elif site == "uk":
        timezone_str = "+0000"
    elif site == "us":
        timezone_str = "-0400"
    elif site == "au":
        timezone_str = "+1000"
    else:
        print(f"Unknown site: {site}")
        return []

    for schedule_day in schedule_days:
        program_divs = schedule_day.find_all('div', class_="container border-bottom-1-light-grey")
        day = str(schedule_day.find('h3', class_="text-black").text.replace("(Today)", "").replace("Timezone: Asia/Colombo", "").replace("Timezone: Africa/Johannesburg", "").replace("Timezone: Australia/Sydney", "").replace("Timezone: America/New_York", "").replace("Timezone: Europe/London", "").strip())

        # Extract the day part (e.g., "9th") and remove the suffix
        day_part = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', day)
        
        # Reconstruct the date string using the cleaned day part and the rest of the original string
        full_date_str = day_part + " 2024"
        
        # Convert to datetime object
        date_object = datetime.datetime.strptime(full_date_str, '%d of %B %Y')
        
        # Format to desired output
        formatted_date = date_object.strftime('%Y-%m-%d')
        for program_div in program_divs:
                starts_p_element = program_div.find('p', class_="text-black font-size-48 line-height-48")
                if starts_p_element:
                    starts_text = starts_p_element.text.strip()
                    starts_text = starts_text.replace('PM', '').replace('AM', '').replace(':', '').strip()
                    starts = datetime.datetime.strptime("{} {} {}".format(formatted_date, starts_text, timezone_str), "%Y-%m-%d %H%M %z")
                   
                    starts = starts.astimezone(central_tz)
                    
                    if starts.date() == the_date:
                        program_name = program_div.find('h3', class_="text-black font-size-18").text.strip()
                        programs.append({
                            "starts": starts.strftime("%H%M"),
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
