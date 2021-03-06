
from .common import Trawler

from bs4 import BeautifulSoup
import urllib
import re
import json
import datetime
from datetime import date, time


def total_secs(delta):
    return (delta.microseconds + (delta.seconds +
                                  delta.days * 24 * 3600) * 10**6) / 10**6


# URL="http://www.churchchannel.tv/watch/schedule_view.php?date="

# def get_filmon_index():
# 	response = urllib.request.urlopen("http://tv.filmon.com/channel/index/")
# 	return json.loads(response.read())

# def find_filmon_internal_num(index, num):
# 	for chan in index["init"]["channels"]:
# 		pub_num = chan["c"][1]
# 		if int(num) == int(pub_num):
# 			return chan["c"][0]
# 	print "Sky - No internal number available"
# 	return 0

# def get_filmon_temp_programs(the_date, internal_num):
# 	date_string = the_date.strftime("%Y-%m-%d")
# 	url_base = "http://tv.filmon.com/programme/channel/" + str(internal_num) + "/" + date_string + "/"
# 	temp_programs = []
# 	for i in range(0,4):
# 		response = urllib.request.urlopen(url_base + str(i) + ".json")
# 		data = json.loads(response.read())
# 		temp_programs.extend(data["listings"][str(internal_num)])
# 	return temp_programs


# def get_filmon_date(the_date, channel_num):

# 	channels = get_filmon_index()
# 	internal_num = find_filmon_internal_num(channels, channel_num)

# 	temp_progs = get_filmon_temp_programs(the_date, internal_num)

# 	programs = []

# 	for temp in temp_progs:
# 		# starts =
# 		# ptime = datetime.datetime.combine(the_date, datetime.datetime.strptime( starts  ,  "%I:%M%p"    ).time())
# 		starts = datetime.datetime.utcfromtimestamp(temp["s"])
# 		starts = starts - datetime.timedelta(hours=2)
# 		if starts.date() < the_date:
# 			continue

# 		time_str = starts.strftime("%H%M")

# 		# link = cols[1].findAll("a")[0].text

# 		programs.append(
# 			{
# 				"date": the_date.strftime("%Y-%m-%d"),
# 				"starts": time_str,
# 				"starts_datetime": starts,
# 				"program_name": temp["t"]
# 			}
# 		)


# 	length = len(programs)
# 	for index, prog in enumerate(programs):
# 		if index == length - 1:
# 			next_prog = {"starts_datetime": datetime.datetime.combine(the_date + datetime.timedelta(days=1), datetime.datetime.min.time()) }
# 		else:
# 			next_prog = programs[index+1]

# 		duration = next_prog["starts_datetime"] - prog["starts_datetime"]
# 		durmins = int(total_secs(duration)/60)
# 		# print "this: " + str(prog["starts_datetime"]) + ", next: " + str(next_prog["starts_datetime"])
# 		# print durmins
# 		programs[index]["duration"] = durmins

# 	for prog in programs:
# 		del prog["starts_datetime"]

# 	return programs

def get_filmon(num):
    # data = urllib.urlencode(values)
    progs = []
    headers = {'Accept-Encoding': 'identity', }
    req = urllib.request.Request(
        "http://www.filmon.tv/api-v2/tvguide/" +
        str(num),
        None,
        headers)

    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())["data"]
    except urllib.error.URLError:
        return []
    data = json.loads(output)

    for p in data:
        start_time = datetime.datetime.utcfromtimestamp(p['startdatetime'])
        if start_time.time().hour < 3:
            continue

        start_time -= datetime.timedelta(hours=2)
        duration_parts = p['duration'].split(":")
        duration = (int(duration_parts[0]) * 60) + int(duration_parts[1])

        progs.append(
            {
                "date": start_time.strftime("%Y-%m-%d"),
                "starts": start_time.strftime("%H%M"),
                # "starts_datetime": start_time,
                "program_name": p['programme_name'],
                "duration": duration
            }
        )

    return progs


# central is -1
# so PST is -3


class TrawlerFilmon(Trawler):
    @staticmethod
    def get_info_for_week(num):
        unorganised_data = get_filmon(num)

        programs_by_date = {}
        for p in unorganised_data:
            d = p['date']
            programs_by_date.setdefault(d, []).append(p)

        print(programs_by_date)
        return programs_by_date

# print TrawlerFilmon.get_info_for_week(2945)
        # schedule = {}
        # for day in days:
        # 	schedule.update( {day.strftime("%Y-%m-%d"): get_filmon_date(day, channel_num)})

        # print schedule
        # return schedule
