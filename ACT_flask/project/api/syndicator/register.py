from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db
import dwollav2
from project.api.dwolla import dwolla_app_token
from flask import flash
import flask_login
from project.api.models import User
import bcrypt
from project.api.plaid import plaid_client


Synd_Register_Blueprint = Blueprint('Synd_Register', __name__)
@Synd_Register_Blueprint.route('/api/syndicator/register/', methods=['GET', 'POST']) # <- from '/'
def Synd_Register():


    
    syndicator_id = request.args.get('sid', None)
    funder_id = request.args.get('fid', None)
    print('Syndicator ID: ', syndicator_id)
    print('Funder ID: ', funder_id)

    if funder_id is None or syndicator_id is None:
        raise Exception('The link appears to be broken.')

    if request.method == 'POST':


        form_data = request.form
        print('form_data form_data form_data ---------------------------------------------->', form_data, file=sys.stderr)


        access_status = "syndicator"
        email = form_data["email"]
        password_1 = form_data["password_1"]
        password_2 = form_data["password_2"]

        print('email email email---------------------------------------------->', email, file=sys.stderr)

        # Make sure form data is good
        funder_doc = db.Master.Funders.find_one({"company_ID": funder_id})
        print(funder_doc)
        if funder_doc is None:
            flash(u'Funder does not exist.', 'flash_error')

        funder_db_name = funder_doc["funder_db_name"]

        user = db.Credentials.Users.find_one({"email": email, "access_status": access_status, "metadata.funder_dbs": { "$in": [funder_db_name]}})
        if user is None:
            flash(u'Your email has not been registered by the funder.', 'flash_error')
            print('Email not in users collection. -------------------------------------->', file=sys.stderr)

        elif password_1 != password_2:
            flash(u'Passwords Do Not Match', 'flash_error')
            print('Passwords Do Not Match ---------------------------------------------->', file=sys.stderr)

        else:            

            # 1. Verify that the user business_id and the syndicator_id id in the link match 
            if user['business_id'] != syndicator_id:
                flash(u'The user business id and the syndicator id do not match.', 'flash_error')

            # 2. Verify that merchant company id exists in the merchant table in the funder db based on the mid in the link
            # and that it matches the user business id.
            mongoDB = db[funder_db_name]
            synd_info = mongoDB.Syndicators.find_one({"syndicator_ID": syndicator_id})
            if synd_info['syndicator_ID'] != user['business_id']:
                flash(u'This user business id does not match the merchant id in the funder records.', 'flash_error')

            # 3. If all of these things work then update password and proceed.
            user = User(email=email, db=db)
            hashed = bcrypt.hashpw(password_1.encode('utf8'), bcrypt.gensalt(14))
            user.update_password(password=hashed, db=db)
        
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['access_status'] = user.access_status
            session['notification_count'] = user.notification_count
            session['business_id'] = user.business_id
            session["user_databases"] = user.user_databases
            
            flask_login.login_user(user)

            return redirect(url_for('MCA_Syndicator_Home.MCA_Syndicator_Home'))
            

    return render_template("/Syndicator/Register/register.html", sid=syndicator_id, fid=funder_id)