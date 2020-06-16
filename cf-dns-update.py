#! /usr/bin/env python3
import requests
import json
import sys
import secrets
import socket

IP_API = 'https://api.ipify.org?format=json'
CF_API_KEY = secrets.cloudflare_api_key
CF_EMAIL = secrets.cloudflare_email
ZONE_ID = secrets.cloudflare_zone_id
RECORD_ID_ARRAY = []
OLD_IP = socket.gethostbyname(secrets.hostname)

# if not RECORD_ID_ARRAY:
#     resp = requests.get(
#         'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(ZONE_ID),
#         headers={
#             'X-Auth-Key': CF_API_KEY,
#             'X-Auth-Email': CF_EMAIL
#         })
#     print(json.dumps(resp.json(), indent=4, sort_keys=True))
#     print('Please find the DNS record ID you would like to update and entry the value into the script')
#     sys.exit(0)

def get_record_id_json(record_id, updated_ip):
    json_return = {}

    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(ZONE_ID, record_id),
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })

    jsondata = json.loads(resp.text)

    json_return['type'] = jsondata['result']['type']
    json_return['name'] = jsondata['result']['name']
    if json_return['content'] == OLD_IP:
        json_return['content'] = updated_ip
    else:
        json_return['content'] = jsondata['result']['content']
    json_return['proxied'] = jsondata['result']['proxied']
    json_return['ttl'] = jsondata['result']['ttl']

    return json_return

def update_dns(record_id, updated_ip):

    json_payload = get_record_id_json(record_id, updated_ip)
    print (json_payload)

    resp = requests.put(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
            ZONE_ID, record_id),
        json=json_payload,
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    print (resp.text)
    assert resp.status_code == 200

    print('updated dns record for {}'.format(updated_ip))

def get_updated_ip():
    resp = requests.get(IP_API)
    json_data = json.loads(resp.text)
    IP_ADDRESS = json_data['ip']
    print(IP_ADDRESS)
    return IP_ADDRESS

def get_record_id_array(RECORD_ID_ARRAY,ZONE_ID, type):
   json_return = {}

   resp = requests.get(
       'https://api.cloudflare.com/client/v4/zones/{}/dns_records?type={}'.format(ZONE_ID,type),
       headers={
         'X-Auth-Key': CF_API_KEY,
         'X-Auth-Email': CF_EMAIL
       })

   jsondata = json.loads(resp.text)

   for item in jsondata['result']:
      record_id = item['id']
      RECORD_ID_ARRAY.append(record_id)

IP_ADDRESS = get_updated_ip()
get_record_id_array(RECORD_ID_ARRAY,ZONE_ID,'A')

for id in RECORD_ID_ARRAY:
    update_dns(id, IP_ADDRESS)

