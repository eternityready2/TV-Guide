from .common import Trawler
import datetime
import json
import requests
import re
from pytz import timezone

def get_data(the_date):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Origin": "https://www.gospeltruth.tv",
            "Pragma": "no-cache",
            "Referer": "https://www.gospeltruth.tv/browse/?list=5fa2ef56dbd8260001e0c1a6",
            "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }


        

        response = requests.get( 
            f"https://api.zype.com/program_guides/6688744bf7eaf50011fe9f88/entries?api_key=GiD2nuFEeFeJgx5y-TOhYaglOM5-UsgqLlX8tMzHpx8w1mEtKRtVDWaWp_ez6pdX&disable_pagination=true",
            headers=headers
        )
        

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return []

    programs = []

    for item in response.json()['response']:
        this = item['start_time']
        this_date = datetime.datetime.strptime(this, "%Y-%m-%dT%H:%M:%S.%f%z")
        pacific_tz = timezone('US/Pacific')
        this_date_pacific = this_date.astimezone(pacific_tz)
        if this_date_pacific.date() == the_date:
            programs.append(
                {
                    "starts": this_date_pacific.strftime("%H%M"),
                    "duration": int(item['duration']/60),
                    "program_name": item['title']
                }
            )
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs

class TrawlerGospelTruthTV(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
