from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import requests
import json
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access, ocrolus_access_token
from project.api.ocrolus import ocrolus_access_token


ocrolus_webhook_Blueprint = Blueprint('ocrolus_webhook', __name__)
@ocrolus_webhook_Blueprint.route("/api/webhooks/ocrolus_webhook/", methods=['GET', 'POST']) 
def ocrolus_webhook():



    webhooks = request.json

    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    print(webhooks, file=sys.stderr)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)

    book_pk = str(webhooks['book_pk'])
    book_uuid = str(webhooks['book_uuid'])
    status =  webhooks['status']


    if status == 'BOOK_COMPLETE':


        print("Ocrulous Status Start ", file=sys.stderr)

        status_url = "https://api.ocrolus.com/v1/book/status?pk=" + book_pk
        status_headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + str(ocrolus_access_token)
        }
        status_response = (requests.request("GET", status_url, headers=status_headers)).json()
        print(status_response, file=sys.stderr)

        print("Ocrulous Status End ", file=sys.stderr)


        doc_uuid = ''
        for doc in status_response['response']['docs']:
            if 'ISO_Doc' in doc['name']:
                doc_uuid = str(doc['uuid'])

        print("doc_uuid =  ", doc_uuid, file=sys.stderr)


        form_data_url = "https://api.ocrolus.com/v1/document/forms/fields"
        payload = {"doc_uuid": doc_uuid}
        form_data_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(ocrolus_access_token)
            }
        form_data_response = (requests.request("GET", form_data_url, json=payload, headers=form_data_headers)).json()

        print("ISO FORM RESPONSE --> ", form_data_response, file=sys.stderr)




        transaction_url = "https://api.ocrolus.com/v1/transaction"
        transaction_payload = {"book_pk": book_pk}
        transaction_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(ocrolus_access_token)
        }
        transaction_response = (requests.request("GET", transaction_url, json=transaction_payload, headers=transaction_headers)).json()
        print(transaction_response, file=sys.stderr)

        with open('static/ocrolus/test_transactions.txt', 'w') as outfile:
            json.dump(transaction_response, outfile)



        analytic_url = "https://api.ocrolus.com/v1/book/analytics/async/request"
        analytic_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(ocrolus_access_token)
            }
        analytic_payload = {"pk": book_pk}
        analytic_response = (requests.request("POST", analytic_url, json=analytic_payload, headers=analytic_headers)).json()

        print(analytic_response, file=sys.stderr)


    elif status == 'COMPLETED':
        if webhooks['event'] == 'ANALYTICS_COMPLETED':

            completed_analytic_url = "https://api.ocrolus.com/v1/book/summary"
            completed_analytic_payload = { "book_uuid": book_uuid}
            completed_analytic_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + str(ocrolus_access_token)
                }
            completed_analytic_response = (requests.request("GET", completed_analytic_url, json=completed_analytic_payload, headers=completed_analytic_headers)).json()


            print(completed_analytic_response, file=sys.stderr)

            with open('static/ocrolus/test_analystics.txt', 'w') as outfile:
                json.dump(completed_analytic_response, outfile)

        else:
            print('NEW EVENT', webhooks['event'], file=sys.stderr)


    else:
        print('NEW STATUS', status, file=sys.stderr)





    return "Success", 200
