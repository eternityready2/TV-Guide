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
        # Request the page
        response = requests.get(
            f"https://ctvn.org/schedule/?_program_guide_date_controls={the_date.strftime('%Y-%m-%d')}",
            headers=headers
        )
        response.raise_for_status()

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        program_elements = soup.find_all('div', class_="wpgb-card-wrapper")
        programs = []

        for program in program_elements:
            program_name_element = program.find('h2', style="font-weight: 500;font-size: 24px;line-height: 36px;")
            program_name = program_name_element.text.strip() if program_name_element else ""

            time_element = program.find('div', class_="ctvn-wpgb-episode-card_meta time-meta")
            if time_element:
                time_text = time_element.text.strip()
                # Extract start time and duration
                if '-' in time_text:
                    start_time_str, duration_str = time_text.split('-')
                    start_time_str = start_time_str.strip()
                    duration_str = duration_str.replace(' minutes', '').strip()

                    try:
                        starts = datetime.datetime.strptime(f"{the_date.strftime('%Y-%m-%d')} {start_time_str} -0400", "%Y-%m-%d %I:%M %p %z")
                        starts = starts.astimezone(central_tz)
                        duration = int(duration_str)
                        
                        if starts.date() == the_date:
                            programs.append({
                                "starts": starts.strftime("%H%M"),
                                "duration": duration,
                                "program_name": program_name
                            })

                    except ValueError as ve:
                        print(f"Error parsing time or duration: {ve}")

        # Calculate durations between programs
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        
        # Set a default duration for the last program if needed
        if programs:
            programs[-1]['duration'] = 30  # Or another appropriate value

        return programs
                     
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

class TrawlerCornerstone(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule[day.strftime("%Y-%m-%d")] = get_data(day)
        return schedule
