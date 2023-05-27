from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
import uuid
import datetime
from datetime import datetime, timedelta
from project import db
from flask_login import login_required



New_ISO_Blueprint = Blueprint('MCA_New_ISO', __name__)
@New_ISO_Blueprint.route('/api/funder/isos/new_iso/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_New_ISO():

    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]

    if request.method == 'POST':


        form_data = request.form

        ISO_business_name = form_data["business_name"]
        ISO_relationship_manager = form_data["relationship_manager"]
        ISO_email = form_data["email"]
        ISO_phone = form_data["phone"]
        ISO_address = form_data["address"]
        ISO_city = form_data["city"]
        ISO_state = form_data["state"]
        ISO_postal = form_data["postal"]
        ISO_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, (ISO_business_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

        mongoDB.ISOs.insert_one({"ISO_ID": ISO_ID, "ISO_business_name": ISO_business_name, "ISO_relationship_manager": ISO_relationship_manager, "ISO_email": ISO_email, "ISO_phone": ISO_phone, "ISO_address": ISO_address, "ISO_city": ISO_city, "ISO_state": ISO_state, "ISO_postal": ISO_postal})

        flash(u'Success New User Registered', 'flash_success')


    return render_template("/Funder/ISOs/New_ISO/new_ISO.html", access_status=session.get('access_status'), notification_count=session.get('notification_count'))
