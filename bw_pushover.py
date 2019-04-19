import requests
import secrets

pu_token = secrets.pushover_app_token
pu_user = secrets.pushover_user_key
url = "https://api.pushover.net/1/messages.json"

message = "test2"
title = "test title"

def send_message (message, title):
    querystring = {"token":pu_token,"user":pu_user,"message":message,"title":title}

    headers = {
                }

    response = requests.request("POST", url, headers=headers, params=querystring)

    print(response.text)


