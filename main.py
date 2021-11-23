import requests
import os
import time


# This finds the first interface by name out of a list of interfaces from the YANG model
def find_interface(name, interfaces):
    ifaces = list(filter(lambda x: x['name'] == name, interfaces))
    return ifaces[0] if len(ifaces) > 0 else None


# Finds the status of the specified interface on the device. Returns None if the int doesn't exist
def check_status(interface):
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

    if res.status_code != 200:
        return None

    return find_interface(interface, res.json()["ietf-interfaces:interfaces"]["interface"])


# Notifies the user of the outcome by sending a webex message
def send_webex_msg(message):
    print(message)

    url = f"https://webexapis.com/v1/messages"

    body = {
        "markdown": message,
        "toPersonEmail": "hhertach@cisco.com"
    }

    headers = {
        "Authorization": f"Bearer {os.environ['BOT']}"
    }

    res = requests.post(url, headers=headers, json=body)

    if res.status_code != 200:
        print(res.status_code)


def main():
    print("Started request...")
    result = check_status("Loopback1234")

    if result == None:
        send_webex_msg("Target interface does not exist!")
    elif not result["enabled"]:
        send_webex_msg("Target interface is shutdown")
    print("Request executed.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)