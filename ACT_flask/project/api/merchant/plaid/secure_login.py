from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db


Secure_Login_Blueprint = Blueprint('MCA_Secure_Login', __name__)
@Secure_Login_Blueprint.route('/api/merchant/plaid/secure_login/', methods=['GET', 'POST']) 
def MCA_Secure_Login():


    mongoDB = db.Master_Credentials

    secure_id_plaid = request.args.get('secure_id', None)

    if request.method == 'POST':


        form_data = request.form

        email = form_data["email"]
        password = form_data["password"]

        print(form_data, file=sys.stderr)
        print(email, file=sys.stderr)

        try:
            merchant = mongoDB.master_user_list.find_one({ "email": email })

            if merchant['password'] != password:
                flash(u'Password is Inncorrect', 'flash_error')
            elif merchant['email'] != email:
                flash(u'email Inncorrect', 'flash_error')
            else:
                session["email"] = email

                return redirect(url_for('MCA_Plaid_Confirm.MCA_Plaid_Confirm', secure_id_plaid=secure_id_plaid))

        except:
            print("no matching email", file=sys.stderr)



    return render_template("/Merchant/Secure_Bank/Secure_Login/secure_login.html", secure_id=secure_id_plaid)
