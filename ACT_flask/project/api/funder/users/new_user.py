from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db


New_User_Blueprint = Blueprint('MCA_New_User', __name__)
@New_User_Blueprint.route('/api/funder/users/new_user/', methods=['GET', 'POST']) 
def MCA_New_User():


    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongo_master = db.Master_Credentials.master_user_list.find_one({ "email": session.get("email") })
        dwolla_funding_source_destination_account = mongo_master["dwolla_funding_source_destination_account"]

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        if access_status != "admin":
            return redirect(url_for('MCA_Login'))

        if request.method == 'POST':

            form_data = request.form


            access_status = form_data["access_status"]
            first_name = form_data["first_name"]
            last_name = form_data["last_name"]
            email = form_data["email"]
            password_1 = form_data["password_1"]
            password_2 = form_data["password_2"]



            all_users = [item['email'] for item in db.Master_Credentials.master_user_list.find()]


            if password_1 != password_2:
                flash(u'Password Do Not Match', 'flash_error')
            elif email in all_users:
                flash(u'email already exists', 'flash_error')
            else:

                mongoDB.Users.insert_one({"access_status": access_status, "first_name": first_name, "last_name": last_name, "email": email, "password": password_1, "notification_count": 0})

                if access_status == "admin":
                    db.Master_Credentials.master_user_list.insert_one({"email": email, "DB_name": DB_name, "password": password_1, "access_status":access_status, "dwolla_funding_source_destination_account":dwolla_funding_source_destination_account})
                else:
                    db.Master_Credentials.master_user_list.insert_one({"email": email, "DB_name": DB_name, "password": password_1, "access_status":access_status})



                flash(u'Success New User Registered', 'flash_success')


    return render_template("/Funder/Users/New_User/new_user.html", access_status=access_status, notification_count=notification_count)
