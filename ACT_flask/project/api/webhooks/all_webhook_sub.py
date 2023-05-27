from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import sys
# from server import mongo_client, mongoDB_master_access, dwolla_app_token, signnow_access_token
from project.api.dwolla import dwolla_app_token
from project.api.signnow import signnow_access_token
import json
import requests


#subscribe to dwolla webhooks at an address


all_webhook_sub_Blueprint = Blueprint('all_webhook_sub', __name__)
@all_webhook_sub_Blueprint.route("/api/webhooks/all_webhook_sub/", methods=['GET', 'POST']) 
def all_webhook_sub():


    #get dwolla webhook info
    webhook_subscriptions = dwolla_app_token.get('webhook-subscriptions')
    num_of_hooks = webhook_subscriptions.body['total'] # => 1
    ids = webhook_subscriptions.body['_embedded']['webhook-subscriptions']


    for ii in ids:
        id_link = ii['_links']['self']['href']
        print(' id_link ------------------------------------------------------------------------------->  --', id_link, file=sys.stderr)

    print(' num of hooks ------------------------------------------------------------------------------->  --', num_of_hooks, file=sys.stderr)


    # Uncomment to delete a webhook
    #webhook_subscription_url_to_DELETE = 'https://api-sandbox.dwolla.com/webhook-subscriptions/ea6ffc82-5950-43c8-bc0b-aa3ceafeea8b'
    #dwolla_app_token.delete(webhook_subscription_url_to_DELETE)


    if request.method == 'POST':

        form_data = request.form
        print(form_data, file=sys.stderr)

        try:
            if form_data['dwolla'] == 'dwolla':

                # Create Dwolla webhook

                dwolla_request_body = {
                  'url': 'https://www.activemca.com/Webhooks/Dwolla_Webhook/',
                  'secret': 'super_secret_key_Gr33nworldwide1!'
                     }

                dwolla_subscription = dwolla_app_token.post('webhook-subscriptions', dwolla_request_body)
                dwolla_webhook_subscription_url = dwolla_subscription.headers['location']

                print('-------------------------------------------------------------------------------> dwolla_webhook_subscription_url --', dwolla_webhook_subscription_url, file=sys.stderr)
                dwolla_webhook_subscription = dwolla_app_token.get(dwolla_webhook_subscription_url)
                dwolla_sub_info = dwolla_webhook_subscription.body['created']

                print('-------------------------------------------------------------------------------> dwolla_sub_info --', dwolla_sub_info, file=sys.stderr)


                print('-------------------------------------------------------------------------------> Dwolla Subscribed --', file=sys.stderr)
        except:
            print('no dwolla')


        # --------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------

        try:
            if form_data['signnow'] == 'signnow':

                # Create SignNow webhook

                user_id = 'fb7b7066a4ca45cc9770ec9069476fc5be6d8993'

                signnow_webhook_url = "https://api-eval.signnow.com/api/v2/events"


                signnow_webhook_payload = json.dumps({
                  "event": "user.document.open",
                  "entity_id": user_id,
                  "action": "callback",
                  "attributes": {
                    "callback": "https://www.activemca.com/Webhooks/SignNow_Webhook/",
                    "use_tls_12": True,
                    "docid_queryparam": True,
                    }
                  })


                signnow_webhook_headers = {"Authorization": "Bearer " + str(signnow_access_token), "Content-Type": "application/json"}

                signnow_webhook_response = requests.request("POST", signnow_webhook_url, data=signnow_webhook_payload, headers=signnow_webhook_headers)

                print('signnow_webhook_response -------------- ---------------- ---------------- >')
                print(signnow_webhook_response.text)
        except:
            print('no signnow')



    return render_template("/Webhooks/All_Webhook_Sub/all_webhook_sub.html")
