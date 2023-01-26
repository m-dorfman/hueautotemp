import os
import threading
import boto3
from datetime import datetime
import requests
import json
import urllib.parse
from pickle import load as p_load

API_KEY_SSM_PARAM = os.environ.get('API_KEY_SSM_PARAM')
ADDRESS = os.environ.get('ADDRESS')
MODEL_BUCKET_NAME = os.environ.get('MODEL_BUCKET_NAME')
MODEL_OBJECT_KEY = os.environ.get('CALLER_OBJECT_KEY')
LIGHT_GROUP = os.environ.get('LIGHT_GROUP')

ssm = boto3.client('ssm')
s3 = boto3.resource('s3')

def set_light_temperature(temperature_mirek, light_group, header):
    # philips hue api only accepts values [140, 500]
    if temperature_mirek > 500:
        temperature_mirek = 500
    if temperature_mirek < 140:
        temperature_mirek = 140
    resource_identifier = '/clip/v2/resource/grouped_light/'
    payload = json.dumps({"color_temperature":{"mirek":temperature_mirek}})
    url = f"https://{ADDRESS}/{resource_identifier}"
    url = urllib.parse.urljoin(url, light_group)

    # we don't need the response from this, so we make it non-blocking
    def sender():
        request = requests.put(url=url, headers=header, data=payload)
    threading.Thread(target=sender).start()

    return

def lambda_handler(event, context):
    model = p_load(s3.Bucket(MODEL_BUCKET_NAME).Object(MODEL_OBJECT_KEY).get())

    now = datetime.now()
    minutes_since_midnight = ((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) // 60

    temperature = model(minutes_since_midnight)
    # temperature above is output in Kelvin, below we get Mired
    temperature_mirek = 1000000 // temperature

    api_key = ssm.get_parameter(Name=API_KEY_SSM_PARAM)
    api_key = api_key['Parameter']['Name']
    header = {'hue-application-key': api_key}

    set_light_temperature(temperature_mirek, LIGHT_GROUP, header)

    return