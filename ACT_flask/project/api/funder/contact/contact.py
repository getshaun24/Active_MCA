from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
from flask_login import login_required


Funder_Contact_Blueprint = Blueprint('MCA_Funder_Contact', __name__)
@Funder_Contact_Blueprint.route('/api/funder/contact/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Funder_Contact():



    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    mongoDB = db[session.get("user_database")]

    user_table = mongoDB.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]
    notification_count = user_table["notification_count"]

    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")


    return render_template("/Funder/Contact/contact.html", access_status=access_status, notification_count=notification_count)
