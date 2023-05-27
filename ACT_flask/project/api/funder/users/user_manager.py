from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db


User_Manager_Blueprint = Blueprint('MCA_User_Manager', __name__)
@User_Manager_Blueprint.route('/api/funder/users/user_manager/', methods=['GET', 'POST'])
def MCA_User_Manager():



    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]
        print(access_status, file=sys.stderr)


        if access_status != "admin":
            return redirect(url_for('MCA_Login'))


        user_list = []
        for user in mongoDB.Users.find():
            try:
                user_list.append([user['access_status'], user['first_name'], user['last_name'], user['email'], user['password']])
            except:
                user_list.append([user['access_status'], user['first_name'], '-', user['email'], user['password']])





    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")





    return render_template("/Funder/Users/User_Manager/user_manager.html", user_list=user_list, access_status=access_status, notification_count=notification_count)
