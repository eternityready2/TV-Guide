from .common import Trawler
from bs4 import BeautifulSoup
import requests
import datetime
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')
    
    try:
        # Format URLs
        url1_date_str = the_date.strftime('%Y/%m/%d')
        url1 = f"https://www.3angels.ru/ajx/tvschedule/site/3/{url1_date_str}/0.1"
        
        # Calculate the date for url2 (the day after)
        url2_date_str = (the_date + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        url2 = f"https://www.3angels.ru/ajx/tvschedule/site/3/{url2_date_str}/0.1"
        
        # Fetch data from both URLs
        response1 = requests.get(url1)
        response1.raise_for_status()
        response2 = requests.get(url2)
        response2.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    programs = []

    soup1 = BeautifulSoup(response1.content, 'html.parser')
    soup2 = BeautifulSoup(response2.content, 'html.parser')

    # Extract rows from both soups
    rows1 = soup1.find_all('tr')
    rows2 = soup2.find_all('tr')
    for row in rows1:
        try:
            time_element = row.find('td', class_='scheduleTime')
            program_element = row.find('td', class_='schedulePName')
            
            if time_element and program_element:
                program_name = program_element.find('br').next_sibling if program_element.find('br') else 'Unknown'
                time_1 = time_element.text.replace(':', '').replace('\n', '').strip()

                # Padding single digit hour with zero
                if len(time_1) == 3:
                    time_1 = '0' + time_1
                    
                # Create a datetime object in Central Time
                # print(time_1)
                start = datetime.datetime.strptime("{} {} +0300".format(the_date.strftime("%Y-%m-%d"),  time_1), "%Y-%m-%d %H%M %z")
                start = start.astimezone(central_tz)  # Convert to Central Time
               
                if start.date() == the_date:
                    programs.append({
                        'starts': start.strftime("%H%M"),
                        'program_name': program_name,
                        'duration': 40  # Default duration
                    })
        except Exception as e:
            print(f"Error processing row: {e}")

    for row in rows2:
        try:
            time_element2 = row.find('td', class_='scheduleTime')
            program_element2 = row.find('td', class_='schedulePName')
            
            if time_element2 and program_element2:
                program_name2 = program_element2.find('br').next_sibling if program_element2.find('br') else 'Unknown'
                time_2 = time_element2.text.strip().replace(':', '').replace('\n', '')
                
                # Padding single digit hour with zero
                if len(time_2) == 3:
                    time_2 = '0' + time_2
                    
                # Create a datetime object in Central Time
                start2 = datetime.datetime.strptime("{} {} +0300".format((the_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), time_2), "%Y-%m-%d %H%M %z")
                start2 = start2.astimezone(central_tz)  # Convert to Central Time
                
                if start2.date() == the_date:
                    programs.append({
                        'starts': start2.strftime("%H%M"),
                        'program_name': program_name2,
                        'duration': 40  # Default duration
                    })
        except Exception as e:
            print(f"Error processing row: {e}")

    # Calculate durations
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
        
    return programs

class TrawlercRussian(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})
        return schedule
