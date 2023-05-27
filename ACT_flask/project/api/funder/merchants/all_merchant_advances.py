from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db


All_Merchant_Advances_Blueprint = Blueprint('MCA_All_Merchant_Advances', __name__)
@All_Merchant_Advances_Blueprint.route('/api/funder/merchants/all_merchant_advances/', methods=['GET', 'POST'])
def MCA_All_Merchant_Advances():



    if session.get("access_status") != "admin":
        return redirect(url_for('MCA_Login'))

    else:

        mongoDB = db[session.get("user_database")]

        user_table = db.Credentials.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        merchant_id = request.args.get('mid', None)
        print('merchant_id --- -- --- - -->', merchant_id , file=sys.stderr)

        company = mongoDB.Merchants.find_one({ "company_ID": merchant_id})

        company_info = []
        company_DBA = company["company_DBA"]
        company_ID = company["company_ID"]
        for cash_ad in company['cash_advance_contracts']:
            company_info.append([company_ID, company_DBA, str(cash_ad['contract_ID']), cash_ad['status'], cash_ad['start_date'], cash_ad['expected_end_date'], cash_ad['duration'], cash_ad['advance_amount'], cash_ad['factor_rate'], cash_ad['expected_repayment_amount'], cash_ad['total_amount_repaid'], cash_ad['percent_paid']])
            print('get --- -- --- - -->', cash_ad, file=sys.stderr)



    return render_template("/Funder/Merchants/All_Merchant_Advances/all_merchant_advances.html", company_DBA=company_DBA, company_info=company_info, access_status=access_status, notification_count=notification_count, mid=merchant_id)
