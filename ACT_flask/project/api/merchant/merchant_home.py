from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db
# from functions import _jinja2_currency_format
from flask_login import login_required
from project.api.models import User
from datetime import datetime, timedelta


Merchant_Home_Blueprint = Blueprint('MCA_Merchant_Home', __name__)
@Merchant_Home_Blueprint.route('/api/merchant/merchant_home/', methods=['GET', 'POST'])
def MCA_Merchant_Home():


    if not session.get("access_status") == 'merchant':
        return redirect(url_for('MCA_Login'))


    else:

        name = session.get("first_name")
        merchant_dba = ""

        # mongoDB = db.Merchant_Users


        # user_table = mongoDB.merchant_users.find_one({ "email": session.get("email") })
        # print('SESSION ---------------------------------------------------> ', session.get("email") , file=sys.stderr)

        # #set as session variable later
        # access_status = 'merchant'

        # business_ein = user_table["business_ein"]


        # notification_count = 0


# --------------------------------------------

        # We can replace this part with the newly added list of funder DBs in the merchant collection

        # all_DBs = set([item['DB_name'] for item in db.Master_Credentials.master_user_list.find()])
        funder_dbs = session.get("user_databases")

        print('funder_dbs ---------------------------------------------------> ', funder_dbs , file=sys.stderr)

        # all_company_list = []
        # for DB_name in all_DBs:
        #     mongoDB_comp = db[DB_name]
        #     for xx in mongoDB_comp.Company.find({"business_ein": business_ein}):
        #         all_company_list.append([xx, DB_name.replace("_", " ")])

        # print(all_company_list, file=sys.stderr)

#--------------------------------------------------

        admin_syndicator_view = False
        actv_results = []
        for ii in funder_dbs:
            print('ii iii ii  ---------------------------------------------------> ', ii , file=sys.stderr)
            funder_db = db[ii]
            merchant = funder_db.Merchants.find_one({"company_ID": session.get("business_id")})
            merchant_dba = merchant['company_DBA']
            
            # If it is just the funder name (DB name) throw exception
            try:
                for k1 in merchant['cash_advance_contracts']:
                    if k1['status'] == 'Open':
                        actv_results.append([merchant['company_ID'], merchant['company_DBA'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['contract_ID']])
            except:
                print('is funder name')


        num_of_active = len(actv_results)


        company_DBA = ''
        merchant_count = 0
        months_list = []
        years_list = []
        portfolio_snapshot = {}
        prefunded_results = []
        cash_ad_results = []
        payment_error_list = []
        for ii in funder_dbs:
            funder_db = db[ii]
            funder_DBA = db.Master.Funders.find_one({"funder_db_name": ii}, {"company_DBA":1})["company_DBA"]
            merchant = funder_db.Merchants.find_one({"company_ID": session.get("business_id")})

            print('ii iii ii 22222 ---------------------------------------------------> ', ii , file=sys.stderr)
            # If it is just the funder name (DB name) throw exception
            # try:
            merchant_count += 1
            for k1 in merchant['cash_advance_contracts']:
                if k1['status'] == 'Prefund':
                    prefunded_results.append([funder_DBA, k1['date_added']])

                elif k1['status'] != 'Prefund':

                    company_DBA = merchant['company_DBA']
                    ACH_pull_sched = k1['ACH_pull_schedule']

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



                    try:
                        current_pause_until = (datetime.strptime(k1['pause_until'], '%Y-%m-%d' ))
                    except:
                        current_pause_until = k1['pause_until']
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



                    amount_to_pay_remaining = float(k1['expected_repayment_amount']) - float(k1['total_amount_repaid'])
                    cash_ad_results.append([ii[1], k1['status'], k1['start_date'], k1['advance_amount'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], next_day, k1['pull_amount']])

                    for trans in k1['transaction_track']:
                        if trans['error'] == 'R01' or trans['error'] == 'R08':
                            payment_error_list.append([merchant['company_DBA'], trans['transaction_date'], trans['transaction_amount'], trans['transaction_ID'], trans['status'], trans['error'], merchant['company_ID'], k1['contract_ID']])
            # except:
            #     print('is funder name')





        print('cash_ad_results ---------------------------------------------------> ', cash_ad_results, file=sys.stderr)
        print('prefunded_results ---------------------------------------------------> ', prefunded_results, file=sys.stderr)
        #print('payment_error_list ---------------------------------------------------> ', payment_error_list, file=sys.stderr)



        num_of_open_advs = 0
        num_of_closed_advs = 0
        num_of_defaulted_advs = 0
        num_of_collections_advs = 0
        num_of_legal_advs = 0
        total_expected_repayment = 0
        total_payback_todate = 0
        total_in_collections = 0
        for row in cash_ad_results:
            if row[1] == "Open":
                num_of_open_advs += 1
                print('OPEN ---------------------------------------------------> ', file=sys.stderr)
            if row[1] == "Closed":
                num_of_closed_advs += 1
                print('CLOSED---------------------------------------------------> ', file=sys.stderr)
            if row[1] == "Defaulted":
                num_of_defaulted_advs += 1
            if row[1] == "Collections":
                num_of_collections_advs += 1
                total_in_collections += float(row[11])
            if row[1] == "Legal":
                num_of_legal_advs += 1

            advance_amount = round(float(row[3]),2)
            payback_todate = round(float(row[4]),2)
            total_expected_repayment += round(float(row[5]),2)
            total_payback_todate += payback_todate




        open_total_cash_out = 0
        open_total_expected_repayment = 0
        open_total_payback_todate = 0
        for row in actv_results:
            open_total_cash_out += round(float(row[5]),2)
            open_total_expected_repayment += round(float(row[7]),2)
            open_total_payback_todate += round(float(row[8]),2)



        return render_template("/Merchant/Merchant_Home/merchant_home.html", name=name, merchant_dba=merchant_dba, prefunded_results=prefunded_results, actv_results=actv_results, access_status=session.get("access_status"), admin_syndicator_view=admin_syndicator_view, cash_ad_results=cash_ad_results,
        num_of_active=num_of_active, num_of_defaulted_advs=num_of_defaulted_advs, num_of_closed_advs=num_of_closed_advs, merchant_count=merchant_count, notification_count=session.get("notification_count"), payment_error_list=payment_error_list,
        total_expected_repayment=total_expected_repayment, total_payback_todate=total_payback_todate, open_total_cash_out=open_total_cash_out, total_in_collections=total_in_collections, open_total_expected_repayment=open_total_expected_repayment,
        open_total_payback_todate=open_total_payback_todate, num_of_open_advs=num_of_open_advs, num_of_collections_advs=num_of_collections_advs, num_of_legal_advs=num_of_legal_advs, company_DBA=company_DBA)
