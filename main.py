import requests
import os


def find_interface(name, interfaces):
    print(interfaces)
    ifaces = list(filter(lambda x: x['name'] == name, interfaces))
    print(ifaces)
    return ifaces[0] if len(ifaces) > 0 else None


def check_status():
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

    return find_interface("GigabitEthernet3", res.json()["ietf-interfaces:interfaces"]["interface"])


def send_webex_msg(message):
    print(message)


def main():
    result = check_status()

    if result == None:
        send_webex_msg("Target interface does not exist!")
    elif not result["enabled"]:
        send_webex_msg("Target interface is shutdown")

if __name__ == "__main__":
    main()