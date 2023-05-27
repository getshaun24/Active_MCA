from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
import re
from flask import render_template
from flask import flash
import datetime
from datetime import datetime, timedelta
# from server import mongo_client, mongoDB_master_access, signnow_access_token
from project import db
from project.api.signnow import signnow_access_token
import signnow_python_sdk
import requests
import json
import os
import uuid
import gridfs
import codecs
import base64
from base64 import b64encode


Contract_Templates_Blueprint = Blueprint('MCA_Contract_Templates', __name__)
@Contract_Templates_Blueprint.route('/api/funder/merchants/signnow_manager/contract_templates/', methods=['GET', 'POST']) 
def MCA_Contract_Templates():

    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    mongo_master = db.Master_Credentials.master_user_list.find_one({ "email": session.get("email") })
    DB_name = mongo_master["DB_name"]
    mongoDB = db[DB_name]

    user_table = mongoDB.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]
    notification_count = user_table["notification_count"]



    fs = gridfs.GridFS(mongoDB)


    temp_list = []
    for temp in mongoDB.SignNow_Templates.find():
        fsgrid_template_id = temp['fsgrid_template_id']
        template_id = temp['template_id']

        image = fs.get_last_version(filename=fsgrid_template_id)
        base64_data = codecs.encode(image.read(), 'base64')
        image = base64_data.decode('utf-8')


        signnow_embed_url = "https://api-eval.signnow.com/v2/documents/" + template_id + "/embedded-editor"

        signnow_embed_payload = {
            "redirect_uri": current_app.config['APP_URL'] + "/Funder/Merchants/SignNow_Manager/Contract_Templates/?template_var=" + template_id,
            "link_expiration": 30
        }

        signnow_embed_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(signnow_access_token)
        }
        signnow_embed_response = (requests.request("POST", signnow_embed_url, json=signnow_embed_payload, headers=signnow_embed_headers)).json()
        signnow_embed_url = signnow_embed_response['data']['url']

        print('------')
        print(len(image))
        print('------')

        temp_list.append([template_id, temp['template_name'], temp['date_added'], temp['number_of_roles'], image, signnow_embed_url])


    try:
        template_var = request.args.get('template_var', None)


        print('template_var --> ', template_var)


        get_template_url = "https://api-eval.signnow.com/document/" + template_var

        get_template_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(signnow_access_token)
        }

        get_template_response = (requests.request("GET", get_template_url, headers=get_template_headers)).json()

        number_of_roles = len(get_template_response["roles"])


        mongoDB.SignNow_Templates.update({"template_id": template_var}, {"$set": {"number_of_roles": number_of_roles}})


    except:
        print('no template upldate')










    if request.method == 'POST':


        form_data = request.form
        print(form_data, file=sys.stderr)

        today_date = datetime.today().strftime('%m/%d/%Y')

        print("REQUEST", file=sys.stderr)
        new_document = request.files["new_document"]
        document_name = form_data["document_name"]

        new_doc_ID = (document_name + '_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (document_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")).replace(" ", "_")

        #must add to fsgrid above stream for some reason
        fs = gridfs.GridFS(mongoDB)
        fs.put(new_document, filename=new_doc_ID)

        #saves file to then send signnow path for upload
        filepath = 'static/signnow/' + new_doc_ID + '.pdf'
        new_document.stream.seek(0)
        new_document.save('static/signnow/' + new_doc_ID + '.pdf')


        signnow_doc_response = signnow_python_sdk.Document.upload(signnow_access_token, filepath, False)
        signnow_doc_id = signnow_doc_response['id']
        signnow_template_response = signnow_python_sdk.Template.create(signnow_access_token, signnow_doc_id, document_name);
        signnow_template_id = signnow_template_response['id']

        mongoDB.SignNow_Templates.insert_one({"template_id":signnow_template_id, "template_name": document_name, "date_added":today_date, "fsgrid_template_id": new_doc_ID})

        new_image = fs.get_last_version(filename=new_doc_ID)
        base64_data = codecs.encode(new_image.read(), 'base64')
        new_image = base64_data.decode('utf-8')

        temp_list.append([signnow_template_id, document_name, today_date, new_image])

        os.remove(filepath)



        signnow_embed_url = "https://api-eval.signnow.com/v2/documents/" + signnow_template_id + "/embedded-editor"

        signnow_embed_payload = {
            "redirect_uri": current_app.config['APP_URL'] + "/Funder/Merchants/SignNow_Manager/Contract_Templates/?template_var=" + signnow_template_id,
            "link_expiration": 30
        }

        signnow_embed_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(signnow_access_token)
        }
        signnow_embed_response = (requests.request("POST", signnow_embed_url, json=signnow_embed_payload, headers=signnow_embed_headers)).json()
        signnow_embed_url = signnow_embed_response['data']['url']

        return redirect(signnow_embed_url)






    return render_template("/Funder/Merchants/SignNow_Manager/Contract_Templates/contract_templates.html", notification_count=notification_count, temp_list=temp_list)
