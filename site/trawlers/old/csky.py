from .common import Trawler

from bs4 import BeautifulSoup
import requests
import urllib
import re
import json
import datetime
from datetime import date, time


def total_secs(delta):
    return (delta.microseconds + (delta.seconds +
                                  delta.days * 24 * 3600) * 10**6) / 10**6


# URL="http://www.churchchannel.tv/watch/schedule_view.php?date="
# URL="http://www.sky.com/tv/api/search/movie?"
URL="http://www.sky.com/tv/api/search/movie"


def get_sky_index():
    encoded = urllib.parse.urlencode({
        'duration': duration,
        'detail': detail,
        'time': time,
        'channels': ','.join(channelFilter)
    })
    print(URL + encoded)
    try:
        r = requests.get(URL).json()
        print(r)
        return r
    except Exception():
        return JSON.loads([])


def find_sky_internal_num(index, num):
    for chan in index["init"]["channels"]:
        pub_num = chan["c"][1]
        if int(num) == int(pub_num):
            return chan["c"][0]
    print("Sky - No internal number available")
    return 0


def get_sky_temp_programs(the_date, internal_num):
    date_string = the_date.strftime("%Y-%m-%d")
    url_base = "http://tv.sky.com/programme/channel/" + \
        str(internal_num) + "/" + date_string + "/"
    temp_programs = []
    for i in range(0, 4):

        try:
            response = urllib3.urlopen(url_base + str(i) + ".json")
            data = json.loads(response.read())
        except urllib.error.URLError:
            data = json.loads([])

        temp_programs.extend(data["listings"][str(internal_num)])
    return temp_programs


def get_sky_date(the_date, channel_num):

    channels = get_sky_index()
    internal_num = find_sky_internal_num(channels, channel_num)

    temp_progs = get_sky_temp_programs(the_date, internal_num)

    programs = []

    for temp in temp_progs:
        # starts =
        # ptime = datetime.datetime.combine(the_date, datetime.datetime.strptime( starts  ,  "%I:%M%p"    ).time())
        starts = datetime.datetime.utcfromtimestamp(temp["s"])
        starts = starts - datetime.timedelta(hours=2)
        if starts.date() < the_date:
            continue

        time_str = starts.strftime("%H%M")

        # link = cols[1].findAll("a")[0].text

        programs.append(
            {
                "date": the_date.strftime("%Y-%m-%d"),
                "starts": time_str,
                "starts_datetime": starts,
                "program_name": temp["t"]
            }
        )

    length = len(programs)
    for index, prog in enumerate(programs):
        if index == length - 1:
            next_prog = {
                "starts_datetime": datetime.datetime.combine(
                    the_date +
                    datetime.timedelta(
                        days=1),
                    datetime.datetime.min.time())}
        else:
            next_prog = programs[index + 1]

        duration = next_prog["starts_datetime"] - prog["starts_datetime"]
        durmins = int(total_secs(duration) / 60)
        # print "this: " + str(prog["starts_datetime"]) + ", next: " + str(next_prog["starts_datetime"])
        # print durmins
        programs[index]["duration"] = durmins

    for prog in programs:
        del prog["starts_datetime"]

    return programs


class TrawlerSky(Trawler):
    @staticmethod
    def get_info_for_days(days, channel_num):
        schedule = {}
        for day in days:
            schedule.update(
                {day.strftime("%Y-%m-%d"): get_sky_date(day, channel_num)})

        # print schedule
        return schedule
