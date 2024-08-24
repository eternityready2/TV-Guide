from .common import Trawler
import datetime
import requests
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago') 
    try:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': 'https://harvesttv.in/schedule/',
            'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.get("https://harvesttv.in/wp-admin/admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=7755&target_action=get-all-data&default_sorting=new_first", headers=headers)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching data:", e)
        return []

    programs = []

    the_day = the_date.strftime("%A").lower()

    for item in response.json():
        show = item['value']
        program_name = show[the_day]
        ist_time = show['ist_time']
        ist_time = ist_time.replace('.', ':')

        # Convert IST time to Central Time
        start_time_str = f"{the_date} {ist_time} +05:30"
        ist_start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %I:%M %p %z")
        starts = ist_start_time.astimezone(central_tz)

        if starts.date() == the_date:
            programs.append({
                "starts": starts.strftime("%H%M"),
                "duration": 30,  
                "program_name": program_name,
            })

    # Handling programs after midnight (next day)
    next_day = the_date + datetime.timedelta(days=1)
    next_the_day = next_day.strftime("%A").lower()
    
    for item2 in response.json():
        show2 = item2['value']
        program_name2 = show2[next_the_day]
        ist_time2 = show2['ist_time']
        ist_time2 = ist_time2.replace('.', ':')

        # Convert IST time to Central Time for the next day
        start_time_str2 = f"{next_day} {ist_time2} +05:30"
        ist_start_time2 = datetime.datetime.strptime(start_time_str2, "%Y-%m-%d %I:%M %p %z")
        starts2 = ist_start_time2.astimezone(central_tz)

        if starts2.date() == the_date:
            programs.append({
                "starts": starts2.strftime("%H%M"),
                "duration": 30,  
                "program_name": program_name2,
            })
            
    # Calculate durations between consecutive programs
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes

    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
 
    return programs

class TrawlerHarvestTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
