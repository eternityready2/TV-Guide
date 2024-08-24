from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    try:
        response = requests.post(
            "https://www.govictory.com/wp-admin/admin-ajax.php",
            data={
                'action': 'get_schedule_day',
                'data': the_date.strftime("%Y-%m-%d"),
            },
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            },
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

    programs = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for block in soup.find_all("div", class_="row"):
        try:
            time_block = block.find('div', class_='convert-time')
            starts = datetime.datetime.strptime(time_block.attrs['data-date'], "%Y-%m-%d %H:%M:%S")
            title_elem = block.find('div', class_="program")
            if title_elem:
                title = title_elem.text.strip()  
        except (KeyError, ValueError) as e:
            print("Error parsing program:", e)

        
        if starts.date() == the_date:
            programs.append({
                "starts": starts.strftime("%H%M"),
                "program_name": title,
                "duration" : 30
            })
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs


class TrawlerBVOV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
