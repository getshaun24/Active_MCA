from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
import re
from flask import render_template
from flask import flash
import datetime
from datetime import datetime, timedelta
# from server import mongo_client, mongoDB_master_access
from project import db
import signnow_python_sdk
import requests
import json



SignNow_Manager_Blueprint = Blueprint('MCA_SignNow_Manager', __name__)
@SignNow_Manager_Blueprint.route('/api/funder/merchants/signnow_manager/signnow_manager/', methods=['GET', 'POST'])
def MCA_SignNow_Manager():

    if not session.get("email"):
        return redirect(url_for('MCA_Login'))


    mongo_master = db.Master_Credentials.master_user_list.find_one({ "email": session.get("email") })
    DB_name = mongo_master["DB_name"]
    #global mongoDB
    mongoDB = db[DB_name]

    user_table = mongoDB.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]
    notification_count = user_table["notification_count"]

    if access_status != "admin":
        return redirect(url_for('MCA_Login'))


    today_date = datetime.today().strftime('%m/%d/%Y')


    all_companies = mongoDB.Company.find()
    #all_pre_contracts = mongoDB.Pre_Contract.find()




    document_groups = []
    company_count = 0
    for comp in all_companies:
        for cash_ad in comp['Cash_Advance_Contracts']:
            try:
                # signnow_status = document_data['field_invites'][0]['status']
                signnow_group_id = cash_ad['SignNow']['document_group']['document_group_id']
                signnow_group_name = cash_ad['SignNow']['document_group']['document_group_name']
                signnow_group_doc_number = cash_ad['SignNow']['document_group']['document_group_doc_number']
                signnow_group_last_modified = cash_ad['SignNow']['document_group']['document_group_last_modified']
                signnow_group_total_group_recipients = cash_ad['SignNow']['document_group']['total_group_recipients']
                print('exists!')
                sent_docs = []
                doc_status_nums = []
                for sent_doc in cash_ad['SignNow']['document_group']['sent_documents']:
                    doc_id = sent_doc['signnow_document_id']
                    doc_name = sent_doc['signnow_document_name']
                    doc_status = sent_doc['signnow_status']
                    print(doc_status)
                    # to get priority status
                    if doc_status == 'completed':
                        doc_num = 1
                    elif doc_status == 'pending':
                        doc_num = 2
                    elif doc_status == 'inbox':
                        doc_num = 3
                    elif doc_status == 'expiring':
                        doc_num = 4
                    doc_status_nums.append(doc_num)
                    sent_docs.append([doc_id, doc_status, doc_name])
                group_status = max(doc_status_nums)
                document_groups.append([company_count, signnow_group_id, signnow_group_name, signnow_group_doc_number, signnow_group_last_modified, group_status, signnow_group_total_group_recipients, sent_docs])
            except:
                print('no sign now')




            company_count += 1




    return render_template("/Funder/Merchants/SignNow_Manager/SignNow_Manager/signnow_manager.html", notification_count=notification_count, document_groups=document_groups)
