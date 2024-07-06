from .common import Trawler

import datetime
import requests
import re
import time
from bs4 import BeautifulSoup
from pytz import timezone

def get_data(the_date):
    programs = []

    # this channel starts at 8am and continues to 8am the next morning,
    # so look up yesterday and today, then filter...
    the_datetime = datetime.datetime.strptime("{} 10:10:10".format(the_date.strftime("%Y-%m-%d")), "%Y-%m-%d %H:%M:%S")
    the_yesterdatetime = the_datetime - datetime.timedelta(days=1)
    for epoch in (int(the_yesterdatetime.timestamp()), int(the_datetime.timestamp())):
        day_shift_seconds = 0;
        try:
            response = requests.get(
                "https://tvmds.tvpassport.com/snippet/php/station_calendar/station_calendar.php?subscription_id=impact-tv&station_id=6230&widget_type=station_calendar&tz=EST5EDT&st={}".format(epoch)
            )
            response.raise_for_status()
        except:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        for row in soup.find_all('tr', class_='station_calendar_default_listings'):
            start_time = row.find('td', class_='station_calendar_default_starttime').text.strip()
            title = row.find('p', class_='station_calendar_default_showname').text.strip()

            if("pm" in start_time and day_shift_seconds == 0):
                day_shift_seconds = 60*60*24;

            if "am" in start_time:
                starts = datetime.datetime.strptime("{} {}".format(datetime.datetime.fromtimestamp(epoch+day_shift_seconds).strftime("%Y-%m-%d"), start_time), "%Y-%m-%d %I:%M%p")
            else:
                starts = datetime.datetime.strptime("{} {}".format(datetime.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d"), start_time), "%Y-%m-%d %I:%M%p")
            starts = timezone('EST5EDT').localize(starts).astimezone(timezone('US/Pacific'))

            programs.append({
                "date": starts.strftime("%Y-%m-%d"),
                "starts": starts.strftime("%H%M"),
                "datetime": starts,
                "program_name": title
            })


    programs_to_return = []
    for i in range(len(programs)):
        if i < len(programs)-1:
            programs[i]['duration'] = int(programs[i+1]['datetime'].timestamp() - programs[i]['datetime'].timestamp())/60
            if programs[i]['datetime'].date() == the_date:
                del programs[i]['datetime']
                programs_to_return.append(programs[i])

    return programs_to_return


class TrawlerImpactNetwork(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
