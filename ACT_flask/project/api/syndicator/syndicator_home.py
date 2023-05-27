from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db


Syndicator_Home_Blueprint = Blueprint('MCA_Syndicator_Home', __name__)
@Syndicator_Home_Blueprint.route('/api/syndicator/syndicator_home/', methods=['GET', 'POST']) 
def MCA_Syndicator_Home():

    if session.get("access_status") != 'syndicator':
        return redirect(url_for('logout'))

    else:

        user_database = session.get("user_databases")[0]


        mongoDB = db[user_database]



        syndicator_array = []


        cash_ad_results = []
        # Update query to 
        contracts = mongoDB.Merchants.find({"cash_advance_contracts.syndicators.syndicator_ID": session.get('business_id')})
        print(contracts)
        # for xx in mongoDB.Merchants.find():
        #     for k1 in xx['cash_advance_contracts']:
        #         if syndicator_name in k1['Syndicators']:
        #             cash_ad_results.append([xx['company_ID'], xx['company_DBA'], k1['status'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['contract_ID']])

        actv_results = []
        # for xx in mongoDB.Merchants.find():
        #     for k1 in xx['cash_advance_contracts']:
        #         if k1['status'] == 'Open' or k1['status'] == 'Defaulted':
        #             if syndicator_name in k1['Syndicators']:
        #                 actv_results.append([xx['company_ID'], xx['company_DBA'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['contract_ID'], k1['status']])


    return render_template("/Syndicator/Syndicator_Home/syndicator_home.html", actv_results=actv_results, cash_ad_results=cash_ad_results, syndicator_array=syndicator_array, access_status=session.get('access_status'), syndicator_name_no_underscore=session.get('first_name'), syndicator_name=session.get('first_name'))
