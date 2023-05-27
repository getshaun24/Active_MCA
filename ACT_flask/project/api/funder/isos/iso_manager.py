from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
from flask_login import login_required


ISO_Manager_Blueprint = Blueprint('MCA_ISO_Manager', __name__)
@ISO_Manager_Blueprint.route('/api/funder/isos/iso_manager/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_ISO_Manager():


    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    mongoDB = db[session.get("user_database")]

    ISO_list = []
    for iso in mongoDB.ISOs.find():
        ISO_address = iso['ISO_address'] + ' ' + iso['ISO_city'] + ' ' + iso['ISO_state'] + ' ' + iso['ISO_postal']
        ISO_list.append([ iso['ISO_ID'], iso['ISO_business_name'], iso['ISO_relationship_manager'], iso['ISO_email'], iso['ISO_phone'], ISO_address ])


    return render_template("/Funder/ISOs/ISO_Manager/ISO_Manager.html", ISO_list=ISO_list, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
