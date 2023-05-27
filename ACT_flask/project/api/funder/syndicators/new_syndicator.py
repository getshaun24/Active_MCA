from flask import Blueprint, session, url_for, request, redirect, render_template, flash, current_app
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db
import uuid
from project.api.mail import mail
from project.api.models import create_new_user
from flask_mail import Message


New_Syndicator_Blueprint = Blueprint('MCA_New_Syndicator', __name__)
@New_Syndicator_Blueprint.route('/api/funder/syndicators/new_syndicator/', methods=['GET', 'POST']) 
def MCA_New_Syndicator():

    access_status = session.get('access_status')

    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]

    notification_count = session.get('notification_count')

    if request.method == 'POST':

        form_data = request.form
        print("form request --->", form_data, file=sys.stderr)


        syndicator_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, form_data["business_name"])).replace("-", "")
        # syndicator_new_current = form_data["new_current"]
        syndicator_business_name = (form_data["business_name"])
        print("syndicator_business_name - - - - - - - -- - - - - - - - - - ->", syndicator_business_name, file=sys.stderr)
        syndicator_email = form_data["email"]
        syndicator_first_name = form_data["first_name"]
        syndicator_last_name = form_data["last_name"]
        syndicator_phone = form_data["phone"]
        syndicator_address = form_data["address"]
        syndicator_city = form_data["city"]
        syndicator_state = form_data["state"]
        syndicator_zip = form_data["zip"]
        # syndicator_is_ISO = form_data["is_ISO"]
        email = form_data["email"]
        # password_1 = form_data["password_1"]
        # password_2 = form_data["password_2"]

        user_count = db.Credentials.Users.find({"email": syndicator_email}).count()
        user_exists = False
        if user_count > 0:
            user_exists = True

        # email_list = []
        # for row in mongoDB.Users.find():
        #     for key, val in row.items():
        #         if key == 'email':
        #             email_list.append(val)
        #             print('key ---------------------------------------------------> ', key, file=sys.stderr)
        #             print('val ---------------------------------------------------> ', val, file=sys.stderr)

        # for row in mongoDB.Syndicators.find():
        #     for key, val in row.items():
        #         if key == 'email':
        #             email_list.append(val)
        #             print('key ---------------------------------------------------> ', key, file=sys.stderr)
        #             print('val ---------------------------------------------------> ', val, file=sys.stderr)

        # print("email_list --->", email_list, file=sys.stderr)


        # print("IS SIO ->", syndicator_is_ISO, file=sys.stderr)

        syndicator_count = mongoDB.Syndicators.find({"syndicator_ID": syndicator_ID}).count()
        syndicator_exists = False
        if syndicator_count > 0:
            syndicator_exists = True

        # try:
        #     all_synd_names = [item['email'] for item in mongoDB.Syndicators.find()]
        #     print(all_synd_names, file=sys.stderr)
        # except:
        #     all_synd_names = []

        if user_exists:
            flash(u'There is already an account associated with the email entered.', 'flash_error')
        # elif password_1 != password_2:
        #     flash(u' Passwords do not match!', 'flash_error')
        elif syndicator_exists:
            flash(u'Syndicator already exists.', 'flash_error')
        else:
            print("--- --- --- --- --- --- --- --- --- -- - ->", file=sys.stderr)

            mongoDB.Syndicators.insert_one({
                "syndicator_ID": syndicator_ID, 
                "syndicator_business_name": syndicator_business_name, 
                "syndicator_email": syndicator_email, 
                "syndicator_phone": syndicator_phone, 
                "syndicator_address": syndicator_address, 
                "syndicator_city": syndicator_city, 
                "syndicator_state": syndicator_state, 
                "syndicator_zip": syndicator_zip, 
                # "syndicator_is_ISO": syndicator_is_ISO, 
                "total_syndicated": 0, 
                "total_active_syndicated": 0, 
                "number_of_advances": 0, 
                "number_of_active_advances":0, 
                "revenue":0, 
                # "email": email, 
                # "password": password_1, 
                "access_status": "syndicator"
            })

            create_new_user(
                db=db, 
                email=syndicator_email, 
                access_status='syndicator', 
                first_name=syndicator_first_name, 
                last_name=syndicator_last_name, 
                business_id=syndicator_ID, 
                metadata={
                    "funder_dbs": [session.get('user_database')]
                })

            # db.Credentials.Users.insert_one({
            #     "access_status": "syndicator", 
            #     "first_name": syndicator_business_name, 
            #     "email": email, 
            #     "password": password_1
            # })
            # db.Master_Credentials.master_user_list.insert_one({"email": email, "DB_name": DB_name, "password": password_1, "access_status":"syndicator"})

            # Send email to sydicator
            email_recipients = current_app.config['EMAIL_LIST'].split(';')

            if current_app.config['ENV'] == 'production':
                email_recipients = [syndicator_email]

            funder_name_list = session.get('user_database').split('_')[1:-2]
            word_count = len(funder_name_list)
            funder_pretty_name = ""
            for word in funder_name_list:
                funder_pretty_name+=word+" "
            body = funder_pretty_name + "has registered you as a syndicator using ActiveMCA. Click the link below to complete the signup process.\n\n"
            body += current_app.config['APP_URL'] + "/Syndicator/Register/?sid=" + syndicator_ID + "&fid=" + session.get('business_id')

            msg = Message(
                sender="getresources@fastmail.com",
                recipients=email_recipients,
                subject="ActiveMCA Sydicator Sign Up",
                body=body
            )
            mail.send(msg)

            flash(u'Success New Syndicator Registered', 'flash_success')



    return render_template("/Funder/Syndicators/New_Syndicator/new_syndicator.html", access_status=access_status, notification_count=notification_count)
