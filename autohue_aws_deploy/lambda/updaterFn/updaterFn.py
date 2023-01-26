import os
import boto3
import requests
import json
import urllib.parse

API_KEY_SSM_PARAM = os.environ.get('API_KEY_SSM_PARAM')
ADDRESS = os.environ.get('ADDRESS')
CRON_EVENT_NAME = os.environ.get('CRON_EVENT_NAME')
WRITE_QUEUE_NAME = os.environ.get('WRITE_QUEUE_NAME')

event_bridge = boto3.client('event_bridge')
ssm = boto3.client('ssm')

def turn_lights_off_on(state: bool, light, header):
    resource_identifier = '/clip/v2/resource/light/'
    payload = json.dumps({"on":{"on":state}})
    url = f"https://{ADDRESS}/{resource_identifier}"
    url = urllib.parse.urljoin(url, light)
    request = requests.put(url=url, headers=header, data=payload)

    return request

def event_controller(state: bool):
    if state is False:
        event_bridge.disable_rule(Name=CRON_EVENT_NAME)
    elif state is True:
        event_bridge.enable_rule(Name=CRON_EVENT_NAME)


def lambda_handler(event, context):
    api_key = ssm.get_parameter(Name=API_KEY_SSM_PARAM)
    api_key = api_key['Parameter']['Name']
    header = {'hue-application-key': api_key}
    operation = event['operation']
    light = event['payload']['light']
    if event['operation'] is 'turn-off':
        turn_lights_off_on(False, light, header)
        event_controller(False)
        # TODO add return
    elif event['operation'] is 'turn-on':
        turn_lights_off_on(True, light, header)
        event_controller(True)
        # TODO add return
    else:
        raise ValueError(f'Unrecognized operation "{operation}"')

    #if WRITE_QUEUE_NAME:
        #send_to_write_queue()

# the following function only runs if db flag is enabled for the build
#def send_to_write_queue():