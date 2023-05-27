from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
import datetime
from datetime import datetime, timedelta
from project import db


Synd_Merchant_Transactions_Blueprint = Blueprint('MCA_Synd_Merchant_Transactions', __name__)
@Synd_Merchant_Transactions_Blueprint.route('/api/syndicator/merchant/synd_merchant_transactions/', methods=['GET', 'POST'])
def MCA_Synd_Merchant_Transactions():



    if not session.get("email"):
        return redirect("../../user_settings/login/")

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]



        print(request.args.get('company_id_var', None), file=sys.stderr)
        if "_admin_view" in request.args.get('company_id_var', None):
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            print('company_id_var --------------------------------------------------------------------> ', company_id_var, file=sys.stderr)
            print(company_id_var, file=sys.stderr)
            synd_name = company_id_var_full[79:]
            print('SYND NAME --------------------------------------------------------------------> ', synd_name, file=sys.stderr)
            cash_ad_var = company_id_var_full[44:76]
            print('cash_ad_var --------------------------------------------------------------------> ', cash_ad_var, file=sys.stderr)
            admin_view = True
            merchant_view = False
            advance_view = False
        elif "_merchant_" in request.args.get('company_id_var', None):
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            cash_ad_var = company_id_var_full[42:]
            print(company_id_var, file=sys.stderr)
            print(cash_ad_var, file=sys.stderr)
            merchant_view = True
            admin_view = False
            advance_view = False
            synd_name = None
        elif "_advances_" in request.args.get('company_id_var', None):
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            cash_ad_var = company_id_var_full[42:]
            print(company_id_var, file=sys.stderr)
            print(cash_ad_var, file=sys.stderr)
            merchant_view = False
            admin_view = False
            advance_view = True
            synd_name = None
        else:
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            cash_ad_var = company_id_var_full[35:]
            print('cash_ad_var --------------------------------------------------------------------> ', cash_ad_var, file=sys.stderr)
            admin_view = False
            merchant_view = False
            advance_view = False
            synd_name = None

        print('admin_view --------------------------------------------------------------------> ', admin_view, file=sys.stderr)
        print('merchant_view --------------------------------------------------------------------> ', merchant_view, file=sys.stderr)



        company_info = mongoDB.Company.find_one({ "company_ID": company_id_var })
        print (company_info, file=sys.stderr)

        contract_count = 0
        for contract in company_info['Cash_Advance_Contracts']:
            print('status --------------------------------------------------------------------> ', contract['contract_ID'], file=sys.stderr)
            print('cash_ad_var --------------------------------------------------------------------> ', cash_ad_var, file=sys.stderr)
            if contract['contract_ID'] == cash_ad_var:
                break
            else:
                contract_count += 1


        transaction_table = company_info['Cash_Advance_Contracts'][contract_count]['Transaction_track']
        print('transaction_table -------- ---------- --- - >', transaction_table, file=sys.stderr)


        try:
            transactions = []
            for transaction in transaction_table:
                print('transaction -------- ---------- --- - >', transaction, file=sys.stderr)
                transactions.append([transaction['transaction_num'], transaction['transaction_date'], transaction['transaction_confirmed_date'], transaction['transaction_amount'], transaction['total_amount_repaid'], transaction['note'], transaction['transaction_ID'], transaction['status'], transaction['error']])
        except:
            transactions = []


        print(transactions, file=sys.stderr)

        if request.method == 'POST':
            session.clear()
            return redirect("MCA_Public_Homepage")



        return render_template("/Syndicator/Synd_Merchant_Profile/Synd_Merchant_Transactions/synd_merchant_transactions.html", transactions=transactions, company_id_var_full=company_id_var_full, company_id_var=company_id_var, access_status=access_status)
