from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import sys
import pymongo
import os
# from server import signnow_access_token
from project.api.signnow import signnow_access_token
from project import db
import signnow_python_sdk
import uuid
from random import random
import datetime
from datetime import datetime, timedelta
import gridfs
from flask_login import login_required


All_Prefunded_Blueprint = Blueprint('MCA_All_Prefunded', __name__)
@All_Prefunded_Blueprint.route('/api/funder/advances/pre_funded/all_prefunded/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_All_Prefunded():


    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]


    all_companies = mongoDB.Merchants.find()

    companies = []
    for comp in all_companies:
        print(comp)
        for cash_ad in comp['cash_advance_contracts']:
            if cash_ad['status'] == "Prefund":
                signnow_document_id = cash_ad['signnow_document_id']
                document_data = signnow_python_sdk.Document.get(signnow_access_token['access_token'], signnow_document_id)
                try:
                    signnow_status = document_data['field_invites'][0]['status']
                except:
                    signnow_status = 'None'

                companies.append([comp['company_DBA'], comp['company_ID'], signnow_status] )


    return render_template("/Funder/Advances/Pre_Funded/All_Prefunded/all_prefunded.html", companies=companies, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
