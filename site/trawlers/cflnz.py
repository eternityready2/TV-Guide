from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    programs = []
    central_tz = timezone('America/Chicago') 
    
    # Request for the current date
    try:
        data = {
            'event_schedule_additional[ed_date]': the_date.strftime("%d/%m/%Y"),
            'event_schedule[keywords]': '',
            'event_schedule[desktop_go]': 'Search',
            'event_schedule[advanced]': 1,
            'event_schedule_controls[contains_all]': 'yes',
            'event_schedule[e_series_id]': 0
        }
        response1 = requests.post(
            "https://www.firstlight.org.nz/schedule/?format=listing&advanced=0",
            data=data,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/86.0.4240.75 Safari/537.36',
            },
        )
        response1.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {the_date}: {e}")
        return []
    
    # Request for the next day
    next_day = the_date + datetime.timedelta(days=1)
    try:
        data = {
            'event_schedule_additional[ed_date]': next_day.strftime("%d/%m/%Y"),
            'event_schedule[keywords]': '',
            'event_schedule[desktop_go]': 'Search',
            'event_schedule[advanced]': 1,
            'event_schedule_controls[contains_all]': 'yes',
            'event_schedule[e_series_id]': 0
        }
        response2 = requests.post(
            "https://www.firstlight.org.nz/schedule/?format=listing&advanced=0",
            data=data,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/86.0.4240.75 Safari/537.36',
            },
        )
        response2.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {next_day}: {e}")
        return []

    # Process the first response
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    for block in soup1.find_all('tr', class_="scheduled_event"):
        try:
            event_time = block.find('td', class_='event_time')
            program_name = block.find('td', class_='event_series').text.strip()

            if event_time:
                start_time_str = event_time.text.strip()
                starts = datetime.datetime.strptime(f"{the_date.strftime('%Y-%m-%d')} {start_time_str} +1200", "%Y-%m-%d %I:%M %p %z")
                starts = starts.astimezone(central_tz)

                if starts.date() == the_date:
                    programs.append({
                        "starts": starts.strftime("%H%M"),
                        "duration": 30,  # Placeholder duration, will be updated later
                        "program_name": program_name,
                    })
        except Exception as e:
            print(f"Error parsing event for {the_date}: {e}")

    # Process the second response
    soup2 = BeautifulSoup(response2.content, 'html.parser')
    for block2 in soup2.find_all('tr', class_="scheduled_event"):
        try:
            event_time2 = block2.find('td', class_='event_time')
            program_name2 = block2.find('td', class_='event_series').text.strip()

            if event_time:
                start_time_str2 = event_time2.text.strip()
                starts2 = datetime.datetime.strptime(f"{next_day.strftime('%Y-%m-%d')} {start_time_str2} +1200", "%Y-%m-%d %I:%M %p %z")
                starts2 = starts2.astimezone(central_tz)

                if starts2.date() == the_date:
                    programs.append({
                        "starts": starts2.strftime("%H%M"),
                        "duration": 30,  # Placeholder duration, will be updated later
                        "program_name": program_name2,
                    })
        except Exception as e:
            print(f"Error parsing event for {next_day}: {e}")

    # Calculate the duration between programs
    for i in range(len(programs) - 1):
        try:
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        except Exception as e:
            print(f"Error calculating duration: {e}")

    # Set duration for the last program (if needed)
    if programs:
        programs[-1]['duration'] = 30  # or another appropriate default value

    # Sort programs by start time
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    return programs

class TrawlerFirstLight(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})
        return schedule
