from flask import Blueprint, jsonify
import sys
from project import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user



Advance_Manager_Blueprint = Blueprint('MCA_Advance_Manager', __name__)
@Advance_Manager_Blueprint.route('/api/funder/advances/advance_manager/', methods=['GET']) # <- from '/'
@jwt_required
def MCA_Advance_Manager():

    if current_user.access_status != 'admin':
        return jsonify({'msg': 'Access denied'}), 403

    mongoDB = db[current_user.user_database]

    cash_ad_results = []
    for xx in mongoDB.Company.find():
        for k1 in xx['cash_advance_contracts']:
            if k1['status'] != 'prefund':
                cash_ad_results.append([xx['company_ID'], xx['company_DBA'], k1['status'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['contract_ID']])


    actv_results = []
    for xx in mongoDB.Company.find():
        for k1 in xx['cash_advance_contracts']:
            if k1['status'] == 'open' or k1['status'] == 'defaulted':
                actv_results.append([xx['company_ID'], xx['company_DBA'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['contract_ID'], k1['status']])

    return jsonify({
        'data': {
            'actv_results': actv_results,
            'cash_ad_results': cash_ad_results,
            'access_status': current_user.access_status,
            'notification_count': current_user.notification_count
        },
        'msg': 'Success'
    }), 200
    # return render_template("/Funder/Advances/Advance_Manager/advance_manager.html", actv_results=actv_results, cash_ad_results=cash_ad_results, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
