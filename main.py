import requests
import os


def find_interface(name, interfaces):
    ifaces = list(filter(lambda x: x['name'] == name, interfaces))
    return ifaces[0] if len(ifaces) > 0 else None


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
    result = check_status("GigabitEthernet0")

    if result == None:
        send_webex_msg("Target interface does not exist!")
    elif not result["enabled"]:
        send_webex_msg("Target interface is shutdown")

if __name__ == "__main__":
    main()