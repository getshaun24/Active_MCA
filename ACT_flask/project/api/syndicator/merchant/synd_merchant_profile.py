from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
import datetime
from datetime import datetime, timedelta
from project import db


Synd_Merchant_Profile_Blueprint = Blueprint('MCA_Synd_Merchant_Profile', __name__)
@Synd_Merchant_Profile_Blueprint.route('/api/syndicator/merchant/synd_merchant_profile/', methods=['GET', 'POST'])
def MCA_Synd_Merchant_Profile():



    if not session.get("email"):
        return redirect("../../user_settings/login/")

    else:

        mongoDB = db[session.get("user_database")]


        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]


        if "_admin_view" in request.args.get('company_id_var', None):
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            synd_name = company_id_var_full[79:]
            cash_ad_var = company_id_var_full[44:76]
            admin_view = True
            merchant_view = False
            advance_view = False
        elif "_merchant_" in request.args.get('company_id_var', None):
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            cash_ad_var = company_id_var_full[42:]
            merchant_view = True
            admin_view = False
            advance_view = False
            synd_name = None
        elif "_advances_" in request.args.get('company_id_var', None):
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            cash_ad_var = company_id_var_full[42:]
            merchant_view = False
            admin_view = False
            advance_view = True
            synd_name = None
        else:
            company_id_var_full = request.args.get('company_id_var', None)
            company_id_var = company_id_var_full[:32]
            cash_ad_var = company_id_var_full[35:]
            admin_view = False
            merchant_view = False
            advance_view = False
            synd_name = None



        syndicator_view = False
        if access_status == 'syndicator' or synd_name:
            syndicator_view = True



        company_info = mongoDB.Company.find_one({ "company_ID": company_id_var })



        company_ID = company_info['company_ID']
        legal_company_name = company_info['legal_company_name']
        company_DBA = company_info['company_DBA']
        poc_first_name = company_info['poc_first_name']
        poc_last_name = company_info['poc_last_name']
        poc_email = company_info['poc_email']
        poc_phone = company_info['poc_phone']
        business_description = company_info['business_description']
        funder = company_info['funder']
        under_writer = company_info['under_writer']
        iso = company_info['ISO']
        sales_rep = company_info['sales_rep']
        mcc = company_info['MCC']
        sic = company_info['SIC']

        contract_count = 0 #the contract count to use on the backend
        for contract in company_info['Cash_Advance_Contracts']:
            if contract['contract_ID'] == cash_ad_var:
                break
            else:
                contract_count += 1

        contract_count_show = contract_count + 1 #the contract count to show on the page

        dwolla_customer_url_id = company_info['dwolla_customer_url_id']
        contract_ID = company_info['Cash_Advance_Contracts'][contract_count]['contract_ID']
        status = company_info['Cash_Advance_Contracts'][contract_count]['status']
        start_date = company_info['Cash_Advance_Contracts'][contract_count]['start_date']
        expected_end_date = company_info['Cash_Advance_Contracts'][contract_count]['expected_end_date']
        duration = company_info['Cash_Advance_Contracts'][contract_count]['duration']
        split_percent = company_info['Cash_Advance_Contracts'][contract_count]['split_percent']
        factor_rate = company_info['Cash_Advance_Contracts'][contract_count]['factor_rate']
        funded_via = company_info['Cash_Advance_Contracts'][contract_count]['funded_via']
        fico_score = company_info['Cash_Advance_Contracts'][contract_count]['fico_score']
        position = company_info['Cash_Advance_Contracts'][contract_count]['position']
        tags = company_info['Cash_Advance_Contracts'][contract_count]['tags']
        advance_amount = company_info['Cash_Advance_Contracts'][contract_count]['advance_amount']
        pull_amount = company_info['Cash_Advance_Contracts'][contract_count]['pull_amount']
        expected_repayment_amount = company_info['Cash_Advance_Contracts'][contract_count]['expected_repayment_amount']
        #commission = company_info['Cash_Advance_Contracts'][contract_count]['commission']
        default_amount = company_info['Cash_Advance_Contracts'][contract_count]['default_amount']
        total_amount_repaid = company_info['Cash_Advance_Contracts'][contract_count]['total_amount_repaid']
        percent_paid = company_info['Cash_Advance_Contracts'][contract_count]['percent_paid']
        syndicators = company_info['Cash_Advance_Contracts'][contract_count]['Syndicators']
        ACH_pull_sched = company_info['Cash_Advance_Contracts'][contract_count]['ACH_pull_schedule']
        #initiated_email = company_info['Cash_Advance_Contracts'][contract_count]['initiated_email']
        try:
            current_pause_until = (datetime.strptime(company_info['Cash_Advance_Contracts'][contract_count]['pause_until'], '%Y-%m-%d' ))
        except:
            current_pause_until = company_info['Cash_Advance_Contracts'][contract_count]['pause_until']

        transaction_table = company_info['Cash_Advance_Contracts'][contract_count]['Transaction_track']

        today_date = datetime.today()
        if ACH_pull_sched == 'weekly_mon':
            day_of_week = 0
            ACH_pull_sched = "Weekly on Mondays"
        if ACH_pull_sched == 'weekly_tues':
            day_of_week = 1
            ACH_pull_sched = "Weekly on Tuesdays"
        if ACH_pull_sched == 'weekly_wed':
            day_of_week = 2
            ACH_pull_sched = "Weekly on Wednesdays"
        if ACH_pull_sched == 'weekly_thurs':
            day_of_week = 3
            ACH_pull_sched = "Weekly on Thursdays"
        if ACH_pull_sched == 'weekly_fri':
            day_of_week = 4
            ACH_pull_sched = "Weekly on Fridays"
        if ACH_pull_sched == 'weekdays':
            ACH_pull_sched = "Weekdays"
            try:
                day_of_week = today_date.weekday() + 1
            except:
                day_of_week = current_pause_until.weekday() + 1
            print(' day_of_week --------------------------------------------------->', day_of_week, file=sys.stderr)
            if day_of_week == 5 or day_of_week == 6:
                day_of_week = 0
                print(' day_of_week --------------------------------------------------->', day_of_week, file=sys.stderr)


        print(' current_pause_until --------------------------------------------------->', current_pause_until, file=sys.stderr)
        if current_pause_until != "None":
            days_ahead = day_of_week - current_pause_until.weekday()
            if days_ahead < 0: # Target day already happened this week
                days_ahead += 7
            next_day = (current_pause_until + timedelta(days_ahead)).strftime('%Y-%m-%d')

            print(' next_day --------------------------------------------------->', next_day, file=sys.stderr)
            print(' next_day --------------------------------------------------->', next_day, file=sys.stderr)
            print(' next_day --------------------------------------------------->', next_day, file=sys.stderr)
        else:
            days_ahead = day_of_week - today_date.weekday()
            if days_ahead < 0: # Target day already happened this week
                days_ahead += 7
            next_day = (today_date + timedelta(days_ahead)).strftime('%Y-%m-%d')

            print(' next_day --------------------------------------------------->', next_day, file=sys.stderr)
            print(' next_day --------------------------------------------------->', next_day, file=sys.stderr)
            print(' next_day --------------------------------------------------->', next_day, file=sys.stderr)

        try:
            pause_until_format = current_pause_until.strftime('%m/%d/%y') #format the pause until date
        except:
            pause_until_format = "None" #when the pause date is none let the pause_until variable be None

        pending_balance = 0
        if True:
            payback_table_results = []
            for transaction in transaction_table:
                payback_table_results.append([transaction['transaction_num'], transaction['transaction_date'], transaction['transaction_confirmed_date'], transaction['transaction_amount'], transaction['total_amount_repaid'], transaction['note'], transaction['transaction_ID'], transaction['status'], transaction['error']])
                if transaction['transaction_confirmed_date'] == "Pending":
                    pending_balance += transaction['transaction_amount']

        else:
            payback_table_results = []




        total_amount_repaid_list = [float(item[4]) for item in payback_table_results]

        print(' 00000 --------------------------------------------------->', file=sys.stderr)


        if request.method == 'POST':
            session.clear()
            return redirect("MCA_Public_Homepage")






        return render_template("/Syndicator/Synd_Merchant_Profile/Synd_Merchant_Profile/synd_merchant_profile.html", merchant_view=merchant_view, synd_name=synd_name, admin_view=admin_view, contract_ID=contract_ID, payback_table_results=payback_table_results, access_status=access_status,
        funder=funder, under_writer=under_writer, iso=iso, sales_rep=sales_rep, mcc=mcc, sic=sic, business_description=business_description, total_amount_repaid_list=total_amount_repaid_list, cash_ad_var=cash_ad_var, contract_count_show=contract_count_show, pending_balance=pending_balance,
        company_ID=company_ID, status=status, start_date=start_date, expected_end_date=expected_end_date, split_percent=split_percent, factor_rate=factor_rate, funded_via=funded_via, fico_score=fico_score, position=position, tags=tags, advance_amount=advance_amount,
        legal_company_name=legal_company_name, company_DBA=company_DBA, poc_first_name=poc_first_name, poc_last_name=poc_last_name, poc_email=poc_email, poc_phone=poc_phone, total_amount_repaid=total_amount_repaid, percent_paid=percent_paid, ACH_pull_sched=ACH_pull_sched, pause_until_format=pause_until_format,
        expected_repayment_amount=expected_repayment_amount, company_id_var_full=company_id_var_full, company_id_var=company_id_var, advance_view=advance_view, syndicator_view=syndicator_view, next_day=next_day, pull_amount=pull_amount, default_amount=default_amount
        )
