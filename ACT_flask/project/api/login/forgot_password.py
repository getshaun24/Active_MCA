from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access, mail
from project import db
from project.api.mail import mail
from random import randint
from flask_mail import Mail
from flask_mail import Message
import bcrypt
from datetime import datetime
from project.api.models import User
import flask_login

Forgot_Password_Blueprint = Blueprint('MCA_Forgot_Password', __name__)

@Forgot_Password_Blueprint.route('/api/login/forgot_password/', methods=['GET', 'POST']) # <- from '/'
def MCA_Forgot_Password():

    reset_var = request.args.get('reset_var', None)
    print("reset_var ---> ", reset_var, file=sys.stderr)
    print("reset_var ---> ", len(reset_var), file=sys.stderr)
    reset_code = reset_var[:-10]
    timestamp = int(reset_var[-10:])
    print("reset_code ---> ", reset_code, file=sys.stderr)
    print("timestamp ---> ", timestamp, file=sys.stderr)

    #see if 30 min experation has transpired
    dt_timestamp = datetime.fromtimestamp(timestamp)
    dt_now = datetime.now()
    duration = dt_now - dt_timestamp                         # get difference in datetimes
    duration_in_s = duration.total_seconds()      # Total number of seconds between dates
    print("duration_in_s ---> ", duration_in_s, file=sys.stderr)
    minutes = int(divmod(duration_in_s, 60)[0])        # Seconds in a minute = 60
    print("minutes ---> ", minutes, file=sys.stderr)

    expired = False
    if minutes > 30:
        expired = True  #make true and hide html form
        flash(u'Link Expired, 30 Minute Limit', 'flash_error_expired')



    if request.method == 'POST':

        # The reset codes could be the same for multiple users so not sure this is a bullet proof method to get a user 
        # (based on the reset code). Why don't we add an email field and use it to search for the user? We can protect pages using the 
        # flask_login @login_required decorator to prevent access to account pages.
        # mongo_master = db.master_user_list.find_one({ "reset_code": reset_code })
        # DB_name = mongo_master["DB_name"]
        # access_status = mongo_master["access_status"]
        # email = mongo_master["email"]

        if request.form.get('email') and request.form.get('new_password') and request.form.get('re_password'):
            
            form_data = request.form
            email = form_data['email']
            new_password = form_data["new_password"]
            re_password = form_data["re_password"]

            user = User(email=email, db=db)

            if user.id is not None:

                # Verify email with reset code
                code_match = user.verify_reset_code(reset_code=reset_code, db=db)
                print(code_match)

                if code_match:
                    

                    if new_password == re_password:

                        hashed = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt(14))
                        
                        user.update_password(password=hashed, db=db)
                        user.clear_reset_code(db=db)
             
                        session['first_name'] = user.first_name
                        session['last_name'] = user.last_name
                        session['access_status'] = user.access_status
                        session['notification_count'] = user.notification_count
                        session['business_id'] = user.business_id

                        flask_login.login_user(user)

                        if user.access_status == "master":
                            print("active master ---> ", file=sys.stderr)
                            return redirect(url_for('MCA_Active_Master_Home.MCA_Active_Master_Home'))
                        elif user.access_status == "admin":
                            print("active admin ---> ", file=sys.stderr)
                            session["user_database"] = user.user_database
                            return redirect(url_for('MCA_Funder_Home.MCA_Funder_Home'))
                        elif user.access_status =="syndicator":
                            print("active syndicator ---> ", file=sys.stderr)
                            session["user_databases"] = user.user_databases
                            return redirect(url_for('MCA_Syndicator_Home.MCA_Syndicator_Home'))
                        elif user.access_status == "merchant":
                            print("active merchant ---> ", file=sys.stderr)
                            session["user_databases"] = user.user_databases
                            return redirect(url_for('MCA_Merchant_Home.MCA_Merchant_Home'))
                    
                    else:
                        flash(u'Passwords Do Not Match', 'flash_error')

                else:
                    flash(u'Error we did not get a password reset request for this account.', 'flash_error')

            else:
                flash(u'No account exists for this email.', 'flash_error')

        else:
            flash(u'Please enter all of the fields.')


        # form_data = request.form
        # new_password = form_data["new_password"]
        # re_password = form_data["re_password"]

        # if new_password == re_password:

        #     hashed = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt(14))

        #     db.master_user_list.update({"reset_code": reset_code}, {"$set": {"password":hashed}})
        #     db.master_user_list.update({"reset_code": reset_code}, {"$set": {"reset_code":''}})

        #     session["email"] = email

        #     if access_status == "admin":
        #         print("active admin ---> ", file=sys.stderr)
        #         return redirect(url_for('MCA_Funder_Home.MCA_Funder_Home'))
        #     elif access_status =="syndicator":
        #         return redirect(url_for('MCA_Syndicator_Home.MCA_Syndicator_Home'))
        #     else:
        #         return redirect(url_for('MCA_Merchant_Home.MCA_Merchant_Home'))

        # else:
        #     flash(u'Passwords Do Not Match', 'flash_error')








    return render_template("/Login/Forgot_Password/forgot_password.html", expired=expired, reset_var=reset_var)
