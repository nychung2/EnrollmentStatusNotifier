import requests
import json
import time
import xml.etree.ElementTree as ElementTree
import config


# Sends a GET Request to UIUC's CISAPI and returns the status of the class.
def retrieve_status(course):
    try:
        response = requests.get(course)
        print("IllinoisAPI Response Code: " + response.status_code.__str__())
    except response.status_code != 200:
        return 'Failed'

    root = ElementTree.fromstring(response.content)
    status = root.findtext('enrollmentStatus')
    notes = root.findtext('sectionNotes')
    if status == 'Open (Restricted)' or status == 'CrossListOpen (Restricted)':
        if 'Engineering tuition program (1ENR)' in notes:
            return 'Open'
        elif notes == 'Restricted to Undergrad - Urbana-Champaign.':
            return 'Open'
    else:
        return status


# Sends a notification to the user if the course is Open.
def notify_user():
    bot_dict = {"bot_id": config.pibot, "text": "The selected course is now open!"}
    bot_json = json.dumps(bot_dict)
    send = requests.post('https://api.groupme.com/v3/bots/post', data=bot_json)
    print("GroupMe Response Code: " + send.status_code.__str__())


# Tells the user that the API GET Request Failed.
def notify_failure():
    bot_dict = {"bot_id": config.pibot, "text": "Illinois API failed three times. Halting Script."}
    bot_json = json.dumps(bot_dict)
    send = requests.post('https://api.groupme.com/v3/bots/post', data=bot_json)
    print("GroupMe Response Code: " + send.status_code.__str__())


counter = 0
program = True
while program:
    string = retrieve_status(config.course_path)
    if string == 'Failed':
        counter += 1
        if counter == 3:
            notify_failure()
            print('Script Terminated')
            program = False
    else:
        if string == 'Open':
            notify_user()
            print('Script Terminated')
            program = False
    time.sleep(60)
