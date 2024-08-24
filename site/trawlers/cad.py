from .common import Trawler
import datetime
import requests
import time  

def get_data(the_date):
    try:
        url = ('https://new.amazingdiscoveries.org/api/programs?scheduled_date={}&timezone=America%2FChicago').format(the_date.strftime("%Y-%m-%d"))
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Ad-Authorization": "",  
            "Cache-Control": "no-cache",
            "Cookie": "_hjSessionUser_1958449=eyJpZCI6IjQ4MGY5NmQwLWNkN2ItNTZiYy05ODQ1LWJhM2MzYTkzYjk0ZCIsImNyZWF0ZWQiOjE3MTIzNDQxMTk4MTcsImV4aXN0aW5nIjp0cnVlfQ==; _amazing_discoveries_session_main=7faafc2c3ead649878e56392f644971e; _gid=GA1.2.809160205.1712518480; _ga=GA1.1.778747664.1712344118; _ga_3WH7Q5BFNG=GS1.1.1712518480.3.0.1712518480.60.0.0; _iub_cs-80077547=%7B%22timestamp%22%3A%222024-04-05T19%3A10%3A47.590Z%22%2C%22version%22%3A%221.57.1%22%2C%22consent%22%3Atrue%2C%22id%22%3A80077547%7D; _hjSession_1958449=eyJpZCI6IjY0ZWM4MDAyLTY5NTUtNDBkMi1iZTBiLTRkOTcxY2YxZmI3YiIsImMiOjE3MTI1MTg0ODIwOTMsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _hjShownFeedbackMessage=true; _ga_B1K8E7GJN7=GS1.1.1712518480.3.1.1712518508.0.0.0",
            "Pragma": "no-cache",
            "Referer": "https://new.amazingdiscoveries.org/schedule",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        programs = []

        for item in response.json()["programs"]:
            starts = item['scheduled_at'].split('T')[1][:5].replace(':', '')  
            programs.append({
                "starts": starts,
                "duration": 30,
                "program_name": item["program_name"],
            })

        for i in range(len(programs) - 1):
            start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
            start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
            duration_minutes = (start_time_next - start_time_current).seconds // 60
            programs[i]['duration'] = duration_minutes
        programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
        return programs

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        raise  

class Trawlercad(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule