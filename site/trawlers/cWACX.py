from .common import Trawler 
import json
import datetime

def get_data(the_date):
    
    day_of_week = the_date.strftime("%A")
    
    with open('./data/wacx.json', 'r') as file:
        data = json.load(file)
    
    programs = []
    
    
    for day_data in data["data"]:
        if day_data.get(day_of_week):
            Day = day_data[day_of_week]
            break
    else:
       
        return programs

    for program in Day:
        time_str = program["time"]
        program_name = program["program"]
        
        central_time_str = datetime.datetime.strptime(time_str, "%I:%M %p").strftime("%H%M")
        
        programs.append({
            "starts": central_time_str,
            "program_name": program_name,
            "duration": 30  
        })

    for i in range(len(programs) - 1):
        start_time_next = datetime.datetime.strptime(programs[i + 1]['starts'], "%H%M")
        start_time_current = datetime.datetime.strptime(programs[i]['starts'], "%H%M")
        duration_minutes = (start_time_next - start_time_current).seconds // 60
        programs[i]['duration'] = duration_minutes
    programs.sort(key=lambda x: datetime.datetime.strptime(x['starts'], "%H%M"))
    return programs
        

class Trawlerwacx(Trawler):
    @staticmethod
    def get_info_for_days(days):
        schedule = {}
        for day in days:
            schedule.update({day.strftime("%Y-%m-%d"): get_data(day)})

        return schedule
