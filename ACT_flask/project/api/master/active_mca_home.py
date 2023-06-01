from flask import Blueprint, session, url_for, request, redirect, render_template, jsonify
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db
import datetime
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, current_user


Active_Master_Home_Blueprint = Blueprint('MCA_Active_Master_Home', __name__)
@Active_Master_Home_Blueprint.route('/api/master/active_mca_home/', methods=['GET', 'POST']) 
@jwt_required()
def MCA_Active_Master_Home():

    if current_user.access_status != 'master':
        return jsonify({'msg': 'Access denied'}), 403

    print('Active_MCA_Home --------------------> 0', file=sys.stderr)

    mongoDB = db.Master

    all_funders = mongoDB.Funders.find()

    print('Active_MCA_Home --------------------> 1', file=sys.stderr)

    funder_list = []
    for xx in all_funders:
        funder_list.append({"funder_dba":xx["company_DBA"], "biz_email":xx["business_email"], "phone":xx["poc_phone"]})


    response = jsonify(funder_list=funder_list, first_name=current_user.first_name)
    
    return response, 200