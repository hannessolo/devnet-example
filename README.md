# devnet-example

Example of how a simple Python script can interact with IOS XE over Restconf and Webex over the REST API. 
The script monitors an interface on the device and sends a webex message if the interface is down or doesn't exist.

# How to use

1. Clone the repository
2. Create a Webex Bot: https://developer.webex.com/my-apps/new/bot
3. Get the username, password and hostname to a DevNet IOS XE device here: https://devnetsandbox.cisco.com/ (search for "IOS XE on CSR Latest Code Always On")
4. Create a file called `.env` in the cloned repo and add the following environment variables:
```
USER=<user for IOS XE device>
PASSW=<password for IOS XE device>
DEVICE_IP=<hostname or IP of IOS XE device>
BOT=<webex bot token>
INTERF=<the interface you would like to monitor>
NOTIFY_EMAIL=<email of the webex user to ping>
```
5. Start the docker container: `docker build -t hannessolo/devnet-demo . && docker run --env-file=.env  hannessolo/devnet-demo`
