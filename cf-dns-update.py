#! /usr/bin/env python3
import requests
import json
import sys
import secrets

# XXX Settings you need to update!!!
IP_API = 'https://api.ipify.org?format=json'
# Get CF API Key: https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-
CF_API_KEY = secrets.cloudflare_api_key
# Your cloudflare email address
CF_EMAIL = secrets.cloudflare_email
# Your zone id is located on the main cloudflare domain dashboard
ZONE_ID = secrets.cloudflare_zone_id
# Run script once without this set and it'll retrive a list of records for you to find the ID to update here
RECORD_ID_ARRAY = secrets.cloudflare_dns_record_ids

if not RECORD_ID_ARRAY:
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(ZONE_ID),
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    print(json.dumps(resp.json(), indent=4, sort_keys=True))
    print('Please find the DNS record ID you would like to update and entry the value into the script')
    sys.exit(0)

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
    json_return['content'] = updated_ip
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

IP_ADDRESS = get_updated_ip()

for id in RECORD_ID_ARRAY:
    update_dns(id, IP_ADDRESS)
