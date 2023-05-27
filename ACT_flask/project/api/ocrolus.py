import requests
from flask import current_app, g
from werkzeug.local import LocalProxy

def get_ocrolus_token():

    if '_ocrolus_access_token' not in g:
        ocrolus_url = "https://auth.ocrolus.com/oauth/token"
        ocrolus_payload = {
            "grant_type": "client_credentials",
            "audience": "https://api.ocrolus.com/",
            "client_id": current_app.config['OCROLUS_ID'],
            "client_secret": current_app.config['OCROLUS_SECRET']
        }
        ocrolus_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        ocrolus_oauth_response = (requests.post(ocrolus_url, json=ocrolus_payload, headers=ocrolus_headers)).json()
        ocrolus_access_token = g._ocrolus_access_token = ocrolus_oauth_response['access_token']

    return ocrolus_access_token

ocrolus_access_token = LocalProxy(get_ocrolus_token)