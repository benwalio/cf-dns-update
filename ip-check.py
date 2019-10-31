#!/usr/bin/env python3

import requests
import json
import os.path
import subprocess
import bw_pushover

IP_API = 'https://api.ipify.org?format=json'
OLD_IP_FILE_PATH = '/etc/external_ip'
<<<<<<< HEAD
CLOUDFLARE_UPDATE_SCRIPT_PATH = '/home/pi/.scripts/cf-dns-update/cf-dns-update.py'
=======
CLOUDFLARE_UPDATE_SCRIPT_PATH = '/usr/local/bin/cf-dns-update/cf-dns-update.py'
>>>>>>> 9e44a80570d4be3113a9cf0aa4645797d2f1f543

def get_updated_ip():
    resp = requests.get(IP_API)
    json_data = json.loads(resp.text)
    IP_ADDRESS = json_data['ip']
    # print(IP_ADDRESS)
    return IP_ADDRESS

def update_ip(ip_address):
    f = open(OLD_IP_FILE_PATH, 'w')
    f.write(ip_address)
    f.close

f = open(OLD_IP_FILE_PATH, 'r')
oldip = f.read()
f.close()

newip = get_updated_ip()

if not os.path.exists(OLD_IP_FILE_PATH):
    update_ip(newip)
elif oldip != newip:
    update_ip(newip)
    subprocess.call(['python3',CLOUDFLARE_UPDATE_SCRIPT_PATH])
<<<<<<< HEAD
    title = "purpi - update IP"
=======
    title = "redpi - update IP"
>>>>>>> 9e44a80570d4be3113a9cf0aa4645797d2f1f543
    message = "SUCCESS - IP changed from {} to {}".format(oldip,newip)
    bw_pushover.send_message(message, title)
