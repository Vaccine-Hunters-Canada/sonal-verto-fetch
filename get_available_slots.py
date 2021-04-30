import copy
from datetime import datetime
import json
import requests
import schedule
import time

#api-endpoint
VACCINETO_API_SLOTS="https://vaccineto.ca/api/slots"
LAST_RUN_JSON = 'last-run.json'

def get_open_slots():
    global LAST_RUN_JSON
    print("")
    print("----------------------------------------")
    print("")
    print(datetime.now().strftime("%Y-%d-%mT%H:%M:%S") + " : Checking for new open slots")
    with open(LAST_RUN_JSON) as last_run_json_file:
        last_run_json = json.load(last_run_json_file)

    response = requests.get(url = VACCINETO_API_SLOTS)
    full_data = response.json()
    data = full_data['data']
    parsed_data = {}
    parsed_data['date'] = datetime.now().strftime("%Y-%d-%mT%H:%M:%S")

    for clinic in data:
        clinic_name = data[clinic]['name']
        
        total_open_slots = 0
        clinic_data = {}
        clinic_data["name"] = clinic_name
        clinic_data["open_slots"] = {}
        clinic_open_slots = {}
        for group in data[clinic]['availabilities']:
            open_slots = 0
            for slot in data[clinic]['availabilities'][group]:
                open_slots = data[clinic]['availabilities'][group][slot]
                if slot in clinic_open_slots:
                    clinic_open_slots[slot] = clinic_open_slots[slot] + open_slots
                else:
                    clinic_open_slots[slot] = open_slots
                total_open_slots += open_slots
        clinic_data["open_slots"] = clinic_open_slots
        clinic_data["total_open_slots"] = total_open_slots
        parsed_data[clinic] = clinic_data
        
    date_time_obj = datetime.now()
    output_json_file = date_time_obj.strftime("%Y-%d-%m_%H-%M-%S") + '.json'
    for data in parsed_data:
        if (data != 'date'):
            total_open_slots = parsed_data[data]['total_open_slots']
            last_run_total_open_slots = last_run_json[data]['total_open_slots']
            parsed_data[data]['difference_since_lastrun'] = total_open_slots - last_run_total_open_slots
            print("Total open slots for " + parsed_data[data]['name'] + " : " + str(total_open_slots))
            print("Difference since last query for " + parsed_data[data]['name'] + " : " + str(total_open_slots - total_open_slots))

    with open(output_json_file, 'w') as output_json:
        json.dump(parsed_data, output_json)
    LAST_RUN_JSON = output_json_file
    

get_open_slots()
schedule.every(3).minutes.do(get_open_slots)

while 1:
    schedule.run_pending()
    time.sleep(1)