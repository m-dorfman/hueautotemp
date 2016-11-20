#!/usr/bin/env python3
import requests
import json

val = 0
obj = {u"sat":val}
payload =json.dumps(obj)

print(payload)

r = requests.put(
    'http://192.168.1.12/api/YqRUanSsJWqimwEXaox6OaxaRS8UxIoMjuv5IvNg/lights/3/state/',
    data=payload
    )
print(r.text)

