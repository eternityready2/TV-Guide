from .common import Trawler
import datetime
import requests


def get_data(the_date):
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.titantvguide.com",
        "Pragma": "no-cache",
        "Referer": "https://www.titantvguide.com/?siteid=77961&hamburger=F",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get("https://www.titantvguide.com/data/eventspage/77961/c530e3b0-0143-4fda-9c99-44b61bbdf2eb/{}0000/1440/24/5".format(the_date.strftime("%Y%m%d")), headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error:", e)

    data = response.json()

    programs = []
    if "Json" in data and "Channels" in data["Json"] and len(data["Json"]["Channels"]) > 0:
        channel = data["Json"]["Channels"][0]  # Selecting the first channel
        if "Days" in channel:
            for day in channel["Days"]:
                for show in day["Shows"]:
                    starts = datetime.datetime.strptime(show["StartTime"], "%Y-%m-%dT%H:%M:%S%z")
                    if starts.date() == the_date:
                        program_name = show["Title"][0]["Text"] if show["Title"] else ""
                        programs.append({
                            "starts": starts.strftime("%H%M"),
                            "duration": 40,  # Default duration, will be updated later
                            "program_name": program_name
                        })

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlerWGNchicago(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule