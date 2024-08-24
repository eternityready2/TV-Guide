#!python3.8
import bottle
from bottle import redirect, route, get, post, run, template, static_file, request, response, auth_basic
import os
import uuid
import json
import hashlib

# import datetime
from datetime import datetime

import re
import pickle
import urllib3

http = urllib3.PoolManager()


bottle.debug(True)

days = []
days_js = []


schedules = {
    # "46":{},
    # "50": {
    # 	# "2015-09-22": [
    # 	# 	{
    # 	# 		"program_name": "Test Hour-long Show",
    # 	# 		"episode_name": "Season 4 Episode 2",
    # 	# 		"date": "2015-09-23",
    # 	# 		"starts": "0000",
    # 	# 		"duration": 60,
    # 	# 		"info_link": "http://somewhere"
    # 	# 	},
    # 	# 	{
    # 	# 		"program_name": "Test 30min Show",
    # 	# 		"episode_name": "Season 1 Episode 1",
    # 	# 		"date": "2015-09-23",
    # 	# 		"starts": "0100",
    # 	# 		"duration": 30,
    # 	# 		"info_link": "http://somewhere"
    # 	# 	},
    # 	# =]
    # }
}


def add_ordinal(n):
    return str(n) + (
        "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(
            n % 10, "th"
        )
    )


def is_authenticated_user(user, password):
    if user == 'jeremiah' and hashlib.md5(password.encode('utf8')).hexdigest() == '21232f297a57a5a743894a0e4a801fc3':
        return True
    return False


with open("./data/channels_corrected.json") as channels_file:
    channels = json.load(channels_file)


@route('/live-tv/update')
def update_data():
    global channels
    global schedules
    global days
    global days_js

    with open(
            './cache/days.pickle', mode='rb'
    ) as days_handle:
        days_data = pickle.load(days_handle, encoding='latin1')
        days = days_data["days"]
        days_js = days_data["days_js"]

    with open("./data/channels_corrected.json") as channels_file:
        channels = json.load(channels_file)

    with open('./cache/schedule.pickle', 'rb') as sched_handle:
        schedules = pickle.load(sched_handle)


@route('/live-tv/days')
def get_days():
    response.content_type = 'application/json'
    return json.dumps(days_js)


@route('/live-tv/channels')
def get_channels():
    return channels


@route('/live-tv/proxy/<url>')
def get_schedule(url):
    # if channel != 50:
    # 	channel = 50
    response.content_type = 'application/json'
    try:
        if url == 'days':
            return get_days()
        elif url == 'channels':
            return get_channels()
        else:
            raise KeyError()
    except KeyError:
        return {"error": "yes"}


@route('/live-tv/schedule/<channel:int>/<date>')
def get_schedule(channel, date):

    options = None

    with open("./manual_schedule/options.json") as options_file:
        options = json.load(options_file)

    day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
    is_manual = options.get(str(channel), {}).get(
        day_of_week, {}).get("is_manual")

    response.content_type = 'application/json'
    try:
        res = []
        if (is_manual and bottle.request.params.get('scr') is None):
            with open("./manual_schedule/schedule.json") as manual_schedule_file:
                manual_schedule = json.load(manual_schedule_file)
                if (manual_schedule[str(channel)][day_of_week]):
                    res = manual_schedule[str(channel)][day_of_week]
        elif (bottle.request.params.get('man') is not None):
            with open("./manual_schedule/schedule.json") as manual_schedule_file:
                manual_schedule = json.load(manual_schedule_file)
                res = manual_schedule.get(str(channel), {}).get(day_of_week, [])
        else:
            res = schedules.get(str(channel), {}).get(date, [])

        return json.dumps(res)
    except KeyError:
        with json.load(open('data/obs/data.json')) as j:
            return json.dumps(j.get('schedules', {}).get('50', {}).get(date, []))


@route('/live-tv/schedule/<channel:int>/<date>/manual')
def get_schedule_option(channel, date):

    options = None
    with open("./manual_schedule/options.json") as options_file:
        options = json.load(options_file)

    day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
    is_manual = options.get(str(channel), {}).get(
        day_of_week, {}).get("is_manual")

    response.content_type = 'application/json'
    return json.dumps({"isManual": True if is_manual else False})


@route('/live-tv/')
def index():
    return template('index')



@route('/on-demand/')
def on_demand():
    with open("./data/on_demand.json") as on_demand_file:
        on_demand_data = json.load(on_demand_file)


    categories = {}
    channel_titles = []
    for channel in on_demand_data['channels']:
        channel_category = channel['category']
        channel_title = channel['title']

        channel_titles.append(channel_title)

        if (channel_category not in categories):
            new_category_obj = {}
            categories[channel_category] = new_category_obj

        if (channel_title not in categories[channel_category]):
            categories[channel_category][channel_title] = channel

    return template('on_demand', on_demand_data=on_demand_data, categories=categories, channel_titles=channel_titles)


@route('/on-demand/channels')
def get_on_demand_channels():
    with open("./data/on_demand.json") as on_demand_file:
        on_demand_data = json.load(on_demand_file)
    return on_demand_data


@auth_basic(is_authenticated_user)
@post('/on-demand/upload')
def upload_on_demand_channel_file():
    upload = request.files.get('file')
    
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.jpg', '.jpeg', '.png'):
        return 'File extension not allowed.'
    new_filename = str(uuid.uuid4()) + ext
    upload.save('./static/img/on_demand/{}'.format(new_filename), overwrite=True)
    return json.dumps({"filename": new_filename})



@route('/live-tv/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@get('/live-tv/admin/channels')
@auth_basic(is_authenticated_user)
def get_admin_channels():
    success = False
    if request.query.loaded:
        success = True
    return template('admin/channels', channels=json.dumps(channels, indent=3), success=success)


@auth_basic(is_authenticated_user)
@post('/live-tv/admin/channels')
def post_admin_channels():
    try:
        with open("./data/channels_corrected.json", "w") as file:
            file.write(request.forms.get('channels'))
    except:
        return "Failed."

    update_data()
    redirect('/live-tv/admin/channels?loaded=1')


@auth_basic(is_authenticated_user)
@post('/live-tv/schedule/<channel:int>/<date>')
def post_admin_schedule(channel, date):
    is_manual = request.json['isManual']
    schedule = request.json['schedule']

    day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

    try:
        with open("./manual_schedule/schedule.json", "+r") as manual_schedule_file:
            manual_schedule = json.load(manual_schedule_file)
            channel_data = manual_schedule.get(str(channel))
            if (not channel_data):
                manual_schedule[str(channel)] = {}
            manual_schedule[str(channel)][day_of_week] = schedule
            new_text = json.dumps(manual_schedule)
            manual_schedule_file.seek(0)
            manual_schedule_file.write(new_text)
            manual_schedule_file.truncate()

        with open("./manual_schedule/options.json", 'r+') as options_file:
            options = json.load(options_file)
            channel_data = options.get(str(channel))
            if (not channel_data):
                options[str(channel)] = {}
            options[str(channel)][day_of_week] = {}
            options[str(channel)][day_of_week]["is_manual"] = is_manual
            new_text = json.dumps(options)
            options_file.seek(0)
            options_file.write(new_text)
            options_file.truncate()

        return json.dumps({"message": "Success"})
    except Exception as e:
        return json.dumps({"error": "Unexpected Server Error"})


@get('/live-tv/admin/on-demand')
@auth_basic(is_authenticated_user)
def get_admin_on_demand():
    with open("./data/on_demand.json") as on_demand_file:
        on_demand_data = json.load(on_demand_file)
    success = False
    if request.query.loaded:
        success = True
    return template('admin/on-demand', on_demand_data=on_demand_data, success=success)

@auth_basic(is_authenticated_user)
@post('/live-tv/admin/on-demand')
def post_admin_on_demand():
    try:
        # with open("./data/on_demand.json", "w") as file:
        #     file.write(request.json)

        with open("./data/on_demand.json", "w") as data_file:
            new_text = json.dumps(request.json['data'])
            data_file.seek(0)
            data_file.write(new_text)
            data_file.truncate()
    except:
        return "Failed."
    return "Success."


@get('/live-tv/admin/images')
@auth_basic(is_authenticated_user)
def get_admin_images():
    success = False
    if request.query.loaded:
        success = True
    return template('admin/images', channels=channels, success=success)


@auth_basic(is_authenticated_user)
@post('/live-tv/admin/images')
def post_admin_images():
    channel = request.forms.get('channel')
    upload = request.files.get('image')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.jpg', '.jpeg'):
        return 'File extension not allowed.'

    upload.save('./static/img/logos_2/{}.jpg'.format(channel), overwrite=True)

    redirect('/live-tv/admin/images?loaded='+channel)


@get('/live-tv/admin/schedules')
@auth_basic(is_authenticated_user)
def get_admin_schedules():
    selected_channel = request.query.get('channel')
    selected_day = request.query.get('day')
    return template('admin/schedules', channels=channels, days=days, selected_channel=selected_channel, selected_day=selected_day)


@auth_basic(is_authenticated_user)
@post('/live-tv/admin/schedules')
def post_admin_schedules():
    channel = request.forms.get('channel')
    date = request.forms.get('day')
    if channel not in schedules:
        schedules[channel] = {}
    schedules[channel][date] = json.loads(request.forms.get('schedule'))
    with open('./cache/schedule.pickle', 'wb+') as sched_dump_handle:
        pickle.dump(schedules, sched_dump_handle,
                    protocol=pickle.HIGHEST_PROTOCOL)
    update_data()
    redirect('/live-tv/admin/schedules?channel='+channel+'&day='+date)


update_data()

run(host='0.0.0.0', port=8000, reloader=False, server='bjoern')
print("exit")
