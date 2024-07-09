from .common import Trawler
import datetime
import json
import requests
from pytz import timezone
from datetime import timedelta
from bs4 import BeautifulSoup

def get_data(the_date):
    try:
        
        start_date = the_date.strftime("%Y-%m-%d")
        end_date = (the_date + timedelta(days=1)).strftime("%Y-%m-%d")
        url = "https://clients6.google.com/calendar/v3/calendars/a2cq41ksipvqgcl0u3pqsuc72g@group.calendar.google.com/events?calendarId=a2cq41ksipvqgcl0u3pqsuc72g%40group.calendar.google.com&singleEvents=true&timeZone=America%2FWinnipeg&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin={}T00%3A00%3A00-05%3A00&timeMax={}T00%3A00%3A00-05%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"
        
        response = requests.get(url.format(start_date, end_date))
        response.raise_for_status()
       
    except requests.exceptions.RequestException as e:
        print("Error fetching calendar events:", e)
        return []

    programs = []

    for item in response.json()["items"]:
        starts = item['start']['dateTime']
        starts = datetime.datetime.strptime(starts, "%Y-%m-%dT%H:%M:%S%z")
        

        
                                    
        programs.append({
            "starts": starts.strftime("%H%M"),
            "duration": 60,
            "program_name": item["summary"],
        })
    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs



class TrawlerFFE(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
