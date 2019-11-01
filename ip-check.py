#!/usr/bin/env python3

import requests
import json
import os.path
import subprocess
import socket
import bw_pushover

IP_API = 'https://api.ipify.org?format=json'
#OLD_IP_FILE_PATH = '/etc/external_ip'
CLOUDFLARE_UPDATE_SCRIPT_PATH = '/home/pi/.scripts/cf-dns-update/cf-dns-update.py'

def get_updated_ip():
    resp = requests.get(IP_API)
    json_data = json.loads(resp.text)
    IP_ADDRESS = json_data['ip']
    # print(IP_ADDRESS)
    return IP_ADDRESS

#def update_ip(ip_address):
#    f = open(OLD_IP_FILE_PATH, 'w')
#    f.write(ip_address)
#    f.close

#f = open(OLD_IP_FILE_PATH, 'r')
#oldip = f.read()
#f.close()

oldip = socket.gethostbyname('ssh.benwal.io')
newip = get_updated_ip()

if oldip != newip:
#    update_ip(newip)
    subprocess.call(['python3',CLOUDFLARE_UPDATE_SCRIPT_PATH])
    title = "{} - update IP".format(socket.gethostname())
    message = "SUCCESS - IP changed from {} to {}".format(oldip,newip)
    bw_pushover.send_message(message, title)
