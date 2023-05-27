from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db


Synd_Contact_Blueprint = Blueprint('MCA_Synd_Contact', __name__)
@Synd_Contact_Blueprint.route('/api/syndicator/contact/', methods=['GET', 'POST'])
def MCA_Synd_Contact():


    if not session.get("email"):
        return redirect("../user_settings/login/")

    mongoDB = db[session.get("user_database")]

    user_table = mongoDB.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]

    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")


    return render_template("/Syndicator/Contact/contact.html", access_status=access_status)
