from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db



Merchant_Notifications_Blueprint = Blueprint('MCA_Merchant_Notifications', __name__)
@Merchant_Notifications_Blueprint.route('/api/merchant/merchant_notifications/', methods=['GET', 'POST']) 
def MCA_Merchant_Notifications():


    if not session.get("access_status") == 'merchant':
        return redirect(url_for('MCA_Login'))

    user_table = db.Credentials.Users.find_one({ "email": session.get("email") })
    print('SESSION ---------------------------------------------------> ', session.get("email") , file=sys.stderr)
    notification_count = int(user_table["notification_count"])



    db.Credentials.Users.update({"email": session.get("email")}, {"$set": {"notification_count": 0}});


    try:
        all_notifications = user_table["notifications"]
        print('all_notifications ---------------------------------------------------> ', all_notifications , file=sys.stderr)
        #all_notifications = mongoDB.merchant_users.find("Notifications").sort("timestamp", -1).limit(2000)
    except:
        #mongoDB.Notifications.insert_one({"Notification": "Placeholder_Notification" })
        all_notifications = []

    notifications = []
    for note in all_notifications:
        notifications.append([note['timestamp'], note['topic'], note['transfer_id']])

    notifications = reversed(notifications)


    return render_template("/Merchant/Merchant_Notifications/merchant_notifications.html", notification_count=notification_count, notifications=notifications)
