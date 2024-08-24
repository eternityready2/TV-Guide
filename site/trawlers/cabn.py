from .common import Trawler
import datetime
import requests
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    central_tz = timezone('America/Chicago')

    try:
        response = requests.get("https://www.abnchannel.net/schedule.php")
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

    programs = []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the swiper slides corresponding to the days of the week
        swiper_divs = soup.find_all('div', class_='swiper-slide')

        # print('current: ', len(swiper_divs), the_date.weekday())
        current_day_div = swiper_divs[the_date.weekday()]
        for li in current_day_div.find_all('li'):
            try:
                start_time_str = li.find('div', string=lambda s: s and s.startswith('Start')).text.replace('Start: ', '').strip()
                end_time_str = li.find('div', string=lambda s: s and s.startswith('End')).text.replace('End: ', '').strip()
                program_name_unfiltered = li.find('div', class_='cell-s-6').text.strip()
                program_name = program_name_unfiltered.replace('Programme: ', '').strip()
                program_name = program_name.split('/')[0].strip()  # Clean program name

                # Replace periods with colons in time strings
                start_time_str = start_time_str.replace('.', ':')
                end_time_str = end_time_str.replace('.', ':')

                start_time_str = start_time_str.replace('00.00AM', '12:00AM')
                start_time_str = start_time_str.replace('00:00AM', '12:00AM')
                start_time_str = start_time_str.replace('00:30AM', '12:30AM')
                end_time_str = end_time_str.replace('00:30AM', '12:30AM')

                # Parse datetime objects
                start_datetime = datetime.datetime.strptime("{} {} +0100".format((the_date).strftime("%Y-%m-%d"), start_time_str), "%Y-%m-%d %I:%M%p %z")
                end_datetime = datetime.datetime.strptime("{} {} +0100".format((the_date).strftime("%Y-%m-%d"), end_time_str), "%Y-%m-%d %I:%M%p %z")
                
                # Convert to Central Time
                start_datetime = start_datetime.astimezone(central_tz)
                end_datetime = end_datetime.astimezone(central_tz)

                duration = int((end_datetime - start_datetime).total_seconds() / 60)
                if start_datetime.date() == the_date:
                    
                    # Append the program details
                    programs.append({
                        "starts": start_datetime.strftime("%H%M"),
                        "duration": duration,
                        "program_name": program_name,
                    })
            except Exception as e:
                print("Error parsing program:", e)


        # print('next: ', len(swiper_divs), (the_date.weekday() + 1) if the_date.weekday() + 1 < 7 else 0)
        next_day_div = swiper_divs[(the_date.weekday() + 1) if the_date.weekday() + 1 < 7 else 0]
        for li2 in next_day_div.find_all('li'):
            try:
                start_time_str2 = li2.find('div', string=lambda s: s and s.startswith('Start')).text.replace('Start: ', '').strip()
                end_time_str2 = li2.find('div', string=lambda s: s and s.startswith('End')).text.replace('End: ', '').strip()
                program_name_unfiltered2 = li2.find('div', class_='cell-s-6').text.strip()
                program_name2 = program_name_unfiltered2.replace('Programme: ', '').strip()
                program_name2 = program_name2.split('/')[0].strip()  # Clean program name

                # Replace periods with colons in time strings
                start_time_str2 = start_time_str2.replace('.', ':')
                end_time_str2 = end_time_str2.replace('.', ':')

                start_time_str2 = start_time_str2.replace('00.00AM', '12:00AM')
                start_time_str2 = start_time_str2.replace('00:00AM', '12:00AM')
                start_time_str2 = start_time_str2.replace('00:30AM', '12:30AM')
                end_time_str2 = end_time_str2.replace('00:30AM', '12:30AM')

                # Parse datetime objects
                start_datetime2 = datetime.datetime.strptime("{} {} +0100".format((the_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), start_time_str2), "%Y-%m-%d %I:%M%p %z")
                end_datetime2 = datetime.datetime.strptime("{} {} +0100".format((the_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), end_time_str2), "%Y-%m-%d %I:%M%p %z")

                # Convert to Central Time
                start_datetime2 = start_datetime2.astimezone(central_tz)
                end_datetime2 = end_datetime2.astimezone(central_tz)

                duration2 = int((end_datetime2 - start_datetime2).total_seconds() / 60)
                if start_datetime2.date() == the_date:
                    # Append the program details
                    programs.append({
                        "starts": start_datetime2.strftime("%H%M"),
                        "duration": duration2,
                        "program_name": program_name2,
                    })
            except Exception as e:
                print("Error parsing program:", e)

        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))

    except Exception as e:
        print("Error parsing HTML:", e)             
    return programs

class TrawlerABN(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule[day.strftime("%Y-%m-%d")] = get_data(day)
        return schedule
