from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access, signnow_access_token
from project import db
import json
import datetime
from datetime import datetime, timedelta

signnow_webhook_Blueprint = Blueprint('signnow_webhook', __name__)
@signnow_webhook_Blueprint.route("/api/webhooks/signnow_webhook/", methods=['GET', 'POST']) 
def signnow_webhook():


    webhook = request.json

    #time.sleep(8)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    print(webhook, file=sys.stderr)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    #time.sleep(8)

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string, file=sys.stderr)

    document_id = webhook['content']['document_id']
    document_name = webhook['content']['document_name']
    event = webhook['meta']['event']
    print('event ----------------------------------------- >', event, file=sys.stderr)
    print('document_id ----------------------------------------- >', document_id, file=sys.stderr)
    print('document_name ----------------------------------------- >', document_name, file=sys.stderr)

    if event == 'user.document.complete':
        status = 'completed'
    if event == 'user.document.open':
        status = 'pending'


    # loop though all databases and put into an array
    all_DBs = set([item['DB_name'] for item in db.Master_Credentials.master_user_list.find()])


    # loop through all the databases and then through all the companies and contracts to find the document that the webhook references
    # breaks loop as soon as the document is found and database entry updated
    break_loops = False
    for DB_name in all_DBs:
        if break_loops == False:
            # global mongoDB
            mongoDB = db[DB_name]


            for comp in mongoDB.Company.find():
                company_id_var = comp['company_ID']
                if break_loops == False:
                    contract_count = 0
                    for contract in comp['Cash_Advance_Contracts']:
                        try: # this is because signnow is not in earlier databases. This should add on reset
                            for key, value in contract['SignNow'].items():
                                if value == document_id:
                                    signnow_var = "Cash_Advance_Contracts." + str(contract_count) + ".SignNow"
                                    mongoDB.Company.update({"company_ID": company_id_var},{"$set": {signnow_var: {"signnow_document_id": document_id, "signnow_status": status, "signnow_document_name": document_name}}});
                                    print('SignNow Updated', file=sys.stderr)
                                    break_loops = True
                                    break
                                contract_count += 1
                        except:
                            print('no signnow variable', file=sys.stderr)
                else:
                    break
        else:
            break





    return "Success", 200
