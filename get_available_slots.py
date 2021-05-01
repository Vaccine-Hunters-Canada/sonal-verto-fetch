import atexit
from datetime import datetime
import json
import os
import requests
import schedule
import time

#api-endpoint
VACCINETO_API_SLOTS="https://vaccineto.ca/api/slots"

def get_open_slots():
    global DATA_DIR
    global LAST_RUN_JSON

    print("")
    print("----------------------------------------")
    print("")
    print(datetime.now().strftime("%Y-%d-%mT%H:%M:%S") + " : Checking for new open slots")

    with open(os.path.join(DATA_DIR, LAST_RUN_JSON)) as last_run_json_file:
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
        clinic_open_slots_group = {}

        for group in data[clinic]['availabilities']:
            open_slots = 0
            clinic_open_slots_group_open_slots = {}
            for slot in data[clinic]['availabilities'][group]:
                open_slots = data[clinic]['availabilities'][group][slot]
                trimmed_datetime = slot.split("T")[0]
                clinic_open_slots_group_open_slots[trimmed_datetime] = open_slots
                total_open_slots += open_slots
            clinic_open_slots_group[group] = clinic_open_slots_group_open_slots

        clinic_data["open_slots"] = clinic_open_slots_group
        clinic_data["total_open_slots"] = total_open_slots
        parsed_data[clinic] = clinic_data

    date_time_obj = datetime.now()
    output_json_file = date_time_obj.strftime("%Y-%d-%m_%H-%M-%S") + '.json'

    with open(os.path.join(DATA_DIR, output_json_file), 'w') as output_json:
        json.dump(parsed_data, output_json, indent=4)

    for data in parsed_data:
        if (data != 'date'):
            total_open_slots = parsed_data[data]['total_open_slots']
            last_run_total_open_slots = last_run_json[data]['total_open_slots']
            total_diff_since_last_run = total_open_slots - last_run_json[data]['total_open_slots'] 
            parsed_data[data]['change_since_last_fetch'] = total_open_slots - last_run_total_open_slots

            print("")
            print("Clinic: {}".format(parsed_data[data]['name']))
            print("---------------------------------")

            for group in parsed_data[data]['open_slots']:
                group_summary_msg = "Group: {}\n".format(group)
                are_slots_available = False
                for date in parsed_data[data]['open_slots'][group]:
                    available_slots = parsed_data[data]['open_slots'][group][date]
                    if (available_slots > 0):
                        are_slots_available = True
                        diff_since_last_run_slot = available_slots - last_run_json[data]['open_slots'][group][date]
                        group_summary_msg += "{} : {} ({:+})\n".format(date, available_slots, diff_since_last_run_slot)
                if are_slots_available:
                    print(group_summary_msg)

            print("Total open slots for {} : {}".format(parsed_data[data]['name'], total_open_slots))
            print("Change since last fetch for {} : {:+}".format(parsed_data[data]['name'], total_diff_since_last_run))
            print("")

    LAST_RUN_JSON = output_json_file

def on_exit_handler():
    os.rename(os.path.join(DATA_DIR, LAST_RUN_JSON), os.path.join(DATA_DIR, 'last-run.json'))
    
if __name__ == '__main__':
    global DATA_DIR
    global LAST_RUN_JSON
    LAST_RUN_JSON = 'last-run.json'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = ROOT_DIR + '/data/'

    atexit.register(on_exit_handler)
    get_open_slots()
    schedule.every(3).minutes.do(get_open_slots)

    while 1:
        schedule.run_pending()
        time.sleep(1)

