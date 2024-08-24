from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago') 
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        response = requests.get(
            "https://wht.tv/tv-guide/?time_zone=CT",
            headers=headers
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    blocks = soup.find_all("li", {"data-showdate": the_date.strftime("%Y%m%d")})
    
    for block in blocks:
        starts_value = block.find("span", class_="large-date").text
        # Replace "a PT" or "p PT" with "am" or "pm"
        starts = starts_value.replace("a CT", "am").replace("p CT", "pm")
        
        # Add the time format if it's missing
        if ':' not in starts:
            starts += ':00'


        starts_formatted = starts.replace("am:00", ":00am").replace("pm:00", ":00pm")
        
        starts = datetime.datetime.strptime("{} {} -0500".format(the_date.strftime("%Y-%m-%d"), starts_formatted), "%Y-%m-%d %I:%M%p %z")
      
        program_name = block.find('div', class_="title").text.strip()
        starts = starts.astimezone(central_tz)
        
        if starts.date() == the_date:
            programs.append(
                {
                    "starts": starts.strftime("%H%M"),
                    "duration": 30,  # Default duration, you might need to update this
                    "program_name": program_name,
                }
            )

    # Calculate program durations
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlerWorldHarvestTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
