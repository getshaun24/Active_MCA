from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import sys
# from server import mongo_client
from project import db


Notifications_Blueprint = Blueprint('MCA_Notifications', __name__)
@Notifications_Blueprint.route('/api/funder/notifications/', methods=['GET', 'POST']) 
def MCA_Notifications():


    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    notifications = db.Credentials.Users.find().sort("timestamp", -1).limit(1000)

    notifications_formatted = []
    for note in notifications:
        # We will figure out what fields we want to have in the notifications. 
        notifications_formatted.append([note['timestamp'], note['legal_company_name'], note['topic']])


    return render_template("/Funder/Notifications/notifications.html", notifications=notifications_formatted, access_status=session.get('access_status'))
