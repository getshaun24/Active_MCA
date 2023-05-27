from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db



Merchant_Contact_Blueprint = Blueprint('MCA_Merchant_Contact', __name__)
@Merchant_Contact_Blueprint.route('/api/merchant/contact/', methods=['GET', 'POST'])
def MCA_Merchant_Contact():



    if not session.get("email"):
        return redirect("/user_settings/login/")


    else:

        # global mongoDB
        mongoDB = db.Merchant_Users

        user_table = mongoDB.merchant_users.find_one({ "email": session.get("email")})
        print('SESSION ---------------------------------------------------> ', session.get("email") , file=sys.stderr)

        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")
        
    return render_template("/Merchant/Contact/contact.html", access_status=access_status, notification_count=notification_count)
