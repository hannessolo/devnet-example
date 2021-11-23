import requests
import os

device = {
    "ip": "sandbox-iosxe-latest-1.cisco.com",
    "username": os.environ["USER"],
    "password": os.environ["PASSW"],
    "port": "443"
}

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

module = "ietf-interfaces:interfaces"

url = f"https://{device['ip']}:{device['port']}/restconf/data/{module}"

res = requests.get(url, headers=headers, auth=(device['username'],device['password']))

print(res.json())