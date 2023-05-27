from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db


Merchant_Manager_Blueprint = Blueprint('MCA_Merchant_Manager', __name__)
@Merchant_Manager_Blueprint.route('/api/funder/merchants/merchant_manager/', methods=['GET', 'POST']) 
def MCA_Merchant_Manager():

    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    mongoDB = db[session.get("user_database")]

    get_company = mongoDB.Merchants.find()

    company_info = []
    for get in get_company:
        poc_first = get['poc_first_name']
        poc_last = get['poc_last_name']
        name = poc_first + ' ' + poc_last
        company_info.append([get['company_ID'], get['company_DBA'], get['legal_company_name'], name, get['poc_email']])


    return render_template("/Funder/Merchants/Merchant_Manager/merchant_manager.html", company_info=company_info, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
