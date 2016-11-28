#!/usr/bin/env python3
from requests import put
import json
import time
import subprocess
import os

print(os.getcwd())
vlc = './VLC.app/Contents/MacOS/VLC'
audio_file = './ALARM.mp3'

subprocess.call([vlc, audio_file])

sat_val = 240
hue_val = 0
obj = {u"sat": sat_val, u"hue": hue_val}
payload = json.dumps(obj)

r = put('http://192.168.1.12/api/YqRUanSsJWqimwEXaox6OaxaRS8UxIoMjuv5IvNg/lights/3/state/',
        data=payload
        )
print(r.text)

vag = {u"on":True}
penis = {u"on":False}

vag = json.dumps(vag)
penis = json.dumps(penis)

# print(payload)

b = True

while b == True:

    penis_send = put(
        'http://192.168.1.12/api/YqRUanSsJWqimwEXaox6OaxaRS8UxIoMjuv5IvNg/lights/3/state/',
        data=penis
        )
    # print(penis_send.text)

    time.sleep(1)

    vag_send = put(
        'http://192.168.1.12/api/YqRUanSsJWqimwEXaox6OaxaRS8UxIoMjuv5IvNg/lights/3/state/',
        data=vag
    )
    # print(vag_send.text)

    time.sleep(1)