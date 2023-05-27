from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db
import datetime
from datetime import datetime, timedelta


Active_Master_Home_Blueprint = Blueprint('MCA_Active_Master_Home', __name__)
@Active_Master_Home_Blueprint.route('/api/master/active_mca_home/', methods=['GET', 'POST']) 
def MCA_Active_Master_Home():



    if session.get("access_status") != "master":
        return redirect(url_for('logout'))

    print('Active_MCA_Home --------------------> 0', file=sys.stderr)

    mongoDB = db.Master

    all_funders = mongoDB.Funders.find()

    print('Active_MCA_Home --------------------> 1', file=sys.stderr)

    funder_list = []
    for xx in all_funders:
        funder_list.append([xx["company_DBA"], xx["business_email"], xx["poc_phone"]])


    print('Active_MCA_Home --------------------> 2', file=sys.stderr)

    # We might want to add code to navigate to a funder breakdown when the row item is clicked.



    return render_template("/Active_MCA_Master/Active_MCA_Home/active_mca_home.html", funder_list=funder_list)
