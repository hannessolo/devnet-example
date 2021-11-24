import requests
import os
import time

# Variable tracks the previous status, so we only send the message once if it hasn't changed
previousStatus = None

# This finds the first interface by name out of a list of interfaces from the YANG model
def find_interface(name, interfaces):
    ifaces = list(filter(lambda x: x['name'] == name, interfaces))
    return ifaces[0] if len(ifaces) > 0 else None


# Finds the status of the specified interface on the device. Returns None if the int doesn't exist
def check_status(interface):
    device = {
        "ip": os.environ["DEVICE_IP"],
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
        "toPersonEmail": os.environ["NOTIFY_EMAIL"]
    }

    headers = {
        "Authorization": f"Bearer {os.environ['BOT']}"
    }

    res = requests.post(url, headers=headers, json=body)

    if res.status_code != 200:
        print(res.status_code)


def main():
    global previousStatus
    result = check_status(os.environ["INTERF"])

    if result == None:
        if previousStatus != "deleted":
            send_webex_msg("Target interface does not exist!")
        previousStatus = "deleted"
    elif not result["enabled"]:
        if previousStatus != "shutdown":
            send_webex_msg("Target interface is shutdown")
        previousStatus = "shutdown"
    else:
        previousStatus = "running"

if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)