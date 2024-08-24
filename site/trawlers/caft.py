from .common import Trawler
from pytz import timezone
import requests
import datetime
from bs4 import BeautifulSoup

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    try:
        # Format URLs
        url1_date_str = the_date.strftime('%Y-%m-%d')
        url2_date_str = (the_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        
        week_number1 = the_date.strftime("%W")
        day_of_week_number1 = the_date.strftime("%w")
        
        week_number2 = (the_date - datetime.timedelta(days=1)).strftime("%W")
        day_of_week_number2 = (the_date - datetime.timedelta(days=1)).strftime("%w")

        url1 = f"https://www.amazingfacts.org/media-library/program-schedule/d/{day_of_week_number1}/w/{week_number1}{the_date.year}"
        url2 = f"https://www.amazingfacts.org/media-library/program-schedule/d/{day_of_week_number2}/w/{week_number2}{the_date.year}"
        
        # Fetch data from both URLs
        response1 = requests.get(url1)
        response1.raise_for_status()
        response2 = requests.get(url2)
        response2.raise_for_status()

        programs = []

        # Process response from URL1
        soup1 = BeautifulSoup(response1.content, 'html.parser')
        table1 = soup1.find('tbody')
        table_rows1 = table1.find_all('tr') if table1 else []
        
        for tr in table_rows1:
            try:
                start_time_str = tr.find_all('td')[0].text.strip()
                starts = datetime.datetime.strptime(f"{the_date.strftime('%Y-%m-%d')} {start_time_str} -0800", "%Y-%m-%d %I:%M %p %z")
                starts = starts.astimezone(central_tz)

                program_name = tr.find_all('td')[1].get_text(strip=True)

                if starts.date() == the_date:
                    programs.append({
                        "starts": starts.strftime("%H%M"),
                        "duration": 30,  # Placeholder duration
                        "program_name": program_name
                    })

            except Exception as e:
                print(f"Error parsing row from URL1: {e}")

        # Process response from URL2
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        table2 = soup2.find('tbody')
        table_rows2 = table2.find_all('tr') if table2 else []
        
        for tr in table_rows2:
            try:
                start_time_str = tr.find_all('td')[0].text.strip()
                starts = datetime.datetime.strptime(f"{(the_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')} {start_time_str} -0800", "%Y-%m-%d %I:%M %p %z")
                starts = starts.astimezone(central_tz)

                program_name = tr.find_all('td')[1].get_text(strip=True)

                if starts.date() == the_date:
                    programs.append({
                        "starts": starts.strftime("%H%M"),
                        "duration": 30,  # Placeholder duration
                        "program_name": program_name
                    })

            except Exception as e:
                print(f"Error parsing row from URL2: {e}")
       
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
