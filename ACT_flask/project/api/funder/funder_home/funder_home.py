from flask import Blueprint, jsonify
from flask_session import Session
import pymongo
import sys
import datetime
from datetime import datetime, timedelta
import calendar
import statistics
# from server import mongo_client, mongoDB_master_access
# from mongo import db as mongo_client
from project.api.functions import takeSecond
from project import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


Funder_Home_Blueprint = Blueprint('MCA_Funder_Home', __name__)
@Funder_Home_Blueprint.route('/api/funder/funder_home/', methods=['GET', 'POST']) # <- from '/'
@jwt_required()
def MCA_Funder_Home():

    if current_user.access_status != 'admin':
        return jsonify({'msg': 'Access denied'}), 403

    mongoDB = db[current_user.user_database]

    print('SESSION ---------------------------------------------------> ', current_user.email , file=sys.stderr)
    access_status = current_user.access_status
    first_name = current_user.first_name
    notification_count = current_user.notification_count

    print('NOTIFICATION_COUNT -------- ', notification_count)


            
    actv_results = []
    for xx in mongoDB.Merchants.find({"cash_advance_contracts.status": "Open"}):
        for k1 in xx['cash_advance_contracts']:
            if k1['status'] == 'Open':
                actv_results.append([xx['company_ID'], xx['company_DBA'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['contract_ID']])

    num_of_active = len(actv_results)

    merchant_count = 0
    months_list = []
    years_list = []
    portfolio_snapshot = {}
    cash_ad_results = []
    payment_error_list = []
    for xx in mongoDB.Merchants.find():
        merchant_count += 1
        for k1 in xx['cash_advance_contracts']:
            if k1['status'] != 'Prefund':
                cash_ad_results.append([xx['company_ID'], xx['company_DBA'], k1['status'], k1['start_date'], k1['expected_end_date'], k1['duration'], k1['advance_amount'], k1['factor_rate'], k1['expected_repayment_amount'], k1['total_amount_repaid'], k1['percent_paid'], k1['default_amount']])

                dt = datetime.strptime(k1['start_date'], '%Y-%m-%d' )
                dt_first = dt.replace(day=1).date()
                month = calendar.month_name[dt.month]
                year = dt.year
                if year not in years_list:
                    portfolio_snapshot.update({year:{month: { "dt_first": dt_first, "advance_amount":[k1['advance_amount']], "expected_repayment_amount":[k1['expected_repayment_amount']], "total_amount_repaid":[k1['total_amount_repaid']], "default_amount":[k1['default_amount']], "status":[k1['status']], "duration":[k1['duration']] }}})
                elif month not in months_list:
                    portfolio_snapshot[year][month] = { "dt_first": dt_first, "advance_amount":[k1['advance_amount']], "expected_repayment_amount":[k1['expected_repayment_amount']], "total_amount_repaid":[k1['total_amount_repaid']], "default_amount":[k1['default_amount']], "status":[k1['status']], "duration":[k1['duration']]}
                else:
                    portfolio_snapshot[year][month]["advance_amount"].append(k1['advance_amount'])
                    portfolio_snapshot[year][month]["expected_repayment_amount"].append(k1['expected_repayment_amount'])
                    portfolio_snapshot[year][month]["total_amount_repaid"].append(k1['total_amount_repaid'])
                    portfolio_snapshot[year][month]["default_amount"].append(k1['default_amount'])
                    portfolio_snapshot[year][month]["status"].append(k1['status'])
                    portfolio_snapshot[year][month]["duration"].append(k1['duration'])

                months_list.append(month)
                years_list.append(year)


                for trans in k1['transaction_track']:
                    if trans['error'] == 'R01' or trans['error'] == 'R08':
                        payment_error_list.append([xx['company_DBA'], trans['transaction_date'], trans['transaction_amount'], trans['transaction_ID'], trans['status'], trans['error'], xx['company_ID'], k1['contract_ID']])





    print('portfolio_snapshot ---------------------------------------------------> ', portfolio_snapshot, file=sys.stderr)
    print('cash_ad_results ---------------------------------------------------> ', cash_ad_results, file=sys.stderr)
    #print('payment_error_list ---------------------------------------------------> ', payment_error_list, file=sys.stderr)


    portfolio_list = []
    for year, val in portfolio_snapshot.items():
        print('val ---------------------------------------------------> ', val, file=sys.stderr)
        for month, v in val.items():
            print('v ---------------------------------------------------> ', v, file=sys.stderr)
            total_advance = sum(map(float,v["advance_amount"]))
            total_expected = sum(map(float,v["expected_repayment_amount"]))
            default_amount = sum(map(float,v["default_amount"]))
            total_amount_repaid = sum(map(float,v["total_amount_repaid"]))
            over_principal = total_amount_repaid - total_advance
            percent_paid = round((total_amount_repaid / total_advance) * 100, 2)
            default_percent_paid = round((default_amount / total_advance) * 100, 2)
            contract_count = len(v["status"])
            default_contract_count = v["status"].count("defaulted")
            average_deal_size = round(statistics.mean(map(float,v["advance_amount"])), 2)
            average_duration = round(statistics.mean(map(float,v["duration"])), 2)
            print('total_avrg ---------------------------------------------------> ', total_advance, file=sys.stderr)
            portfolio_list.append([v["dt_first"], month, total_advance, total_expected, total_amount_repaid, default_amount, percent_paid, default_percent_paid, contract_count, default_contract_count, average_deal_size, over_principal, average_duration])

    print('portfolio_list ---------------------------------------------------> ', portfolio_list, file=sys.stderr)


    num_of_ISOs = 0
    for xx in mongoDB.ISOs.find():
        num_of_ISOs += 1



    num_of_open_advs = 0
    num_of_closed_advs = 0
    num_of_defaulted_advs = 0
    num_of_collections_advs = 0
    num_of_legal_advs = 0
    total_cash_out = 0
    total_expected_repayment = 0
    total_expected_profit = 0
    total_payback_todate = 0
    profits_to_date = 0
    total_in_collections = 0
    factor_list = []
    top_cash_ad_list = []
    bottom_cash_ad_list = []
    top_payback_todate_list = []
    bottom_payback_todate_list = []
    for row in cash_ad_results:
        if row[2] == "open":
            num_of_open_advs += 1
            print('OPEN ---------------------------------------------------> ', file=sys.stderr)
        if row[2] == "closed":
            num_of_closed_advs += 1
            print('CLOSED---------------------------------------------------> ', file=sys.stderr)
        if row[2] == "defaulted":
            num_of_defaulted_advs += 1
        if row[2] == "collections":
            num_of_collections_advs += 1
            total_in_collections += float(row[11])
        if row[2] == "legal":
            num_of_legal_advs += 1
        print('NEXT ---------------------------------------------------> ', float(row[11]), file=sys.stderr)
        advance_amount = round(float(row[6]),2)
        total_cash_out += advance_amount
        payback_todate = round(float(row[9]),2)
        total_expected_repayment += round(float(row[8]),2)
        total_expected_profit += (total_expected_repayment - total_cash_out)
        total_payback_todate += payback_todate
        profits_to_date += (round(float(row[9]),2) - advance_amount)
        factor_list.append(float(row[7]))
        top_cash_ad_list.append([row[1], advance_amount])
        bottom_cash_ad_list.append([row[1], advance_amount])
        top_payback_todate_list.append([row[1], payback_todate])
        bottom_payback_todate_list.append([row[1], payback_todate])

    try:
        average_factor = round(statistics.mean(factor_list),2)
    except:
        average_factor = 0
    top_cash_ad_list.sort(key=takeSecond, reverse=True)
    bottom_cash_ad_list.sort(key=takeSecond)
    top_payback_todate_list.sort(key=takeSecond, reverse=True)
    bottom_payback_todate_list.sort(key=takeSecond)
    top_cash_ad_list = top_cash_ad_list[:5]
    bottom_cash_ad_list = bottom_cash_ad_list[:5]
    top_payback_todate_list = top_payback_todate_list[:5]
    bottom_payback_todate_list = bottom_payback_todate_list[:5]





    open_total_cash_out = 0
    open_total_expected_repayment = 0
    open_total_expected_profit = 0
    open_total_payback_todate = 0
    open_profits_to_date = 0
    open_factor_list = []
    open_percentage_list_top = []
    open_percentage_list_bottom = []
    for row in actv_results:
        open_total_cash_out += round(float(row[5]),2)
        open_total_expected_repayment += round(float(row[7]),2)
        open_total_expected_profit += (total_expected_repayment - total_cash_out)
        open_total_payback_todate += round(float(row[8]),2)
        open_profits_to_date += (round(float(row[8]),2) - round(float(row[4]),2))
        open_factor_list.append(float(row[6]))
        open_percentage_list_top.append([row[1], round(float(row[9]),2)])
        open_percentage_list_bottom.append([row[1], round(float(row[9]),2)])

    try:
        open_average_factor = round(statistics.mean(open_factor_list),2)
    except:
        open_average_factor = 0
    open_percentage_list_top.sort(key=takeSecond, reverse=True)
    open_percentage_list_bottom.sort(key=takeSecond)
    open_percentage_list_top = open_percentage_list_top[:5]
    open_percentage_list_bottom = open_percentage_list_bottom[:5]



    master_synd_list = mongoDB.Syndicators.find()

    synd_label = [];
    synd_amount = [];
    for synd in master_synd_list:
        synd_label.append((synd['syndicator_business_name']).replace("_", " "))
        synd_amount.append(float(synd['total_active_syndicated']))
    print('synd_amount ---------------------------------------------------> ', synd_amount, file=sys.stderr)
    print('synd_label ---------------------------------------------------> ', synd_label, file=sys.stderr)

    num_of_synd = len(synd_label)

    return jsonify(actv_results=actv_results, first_name=first_name, access_status=access_status, num_of_ISOs=num_of_ISOs,
    num_of_active=num_of_active, num_of_defaulted_advs=num_of_defaulted_advs, num_of_closed_advs=num_of_closed_advs, total_cash_out=total_cash_out, total_expected_profit=total_expected_profit, merchant_count=merchant_count,
    average_factor=average_factor, total_expected_repayment=total_expected_repayment, total_payback_todate=total_payback_todate, profits_to_date=profits_to_date, open_total_cash_out=open_total_cash_out, total_in_collections=total_in_collections,
    open_total_expected_repayment=open_total_expected_repayment, open_total_expected_profit=open_total_expected_profit, open_total_payback_todate=open_total_payback_todate, open_average_factor=open_average_factor, open_profits_to_date=open_profits_to_date,
    bottom_cash_ad_list=bottom_cash_ad_list, top_cash_ad_list=top_cash_ad_list, top_payback_todate_list=top_payback_todate_list, bottom_payback_todate_list=bottom_payback_todate_list, open_percentage_list_top=open_percentage_list_top, open_percentage_list_bottom=open_percentage_list_bottom,
    synd_amount=synd_amount, synd_label=synd_label, num_of_synd=num_of_synd, num_of_open_advs=num_of_open_advs, notification_count=notification_count, portfolio_list=portfolio_list, payment_error_list=payment_error_list, num_of_collections_advs=num_of_collections_advs, num_of_legal_advs=num_of_legal_advs), 200

    # return render_template("/Funder/Funder_Home/funder_home.html", actv_results=actv_results, first_name=first_name, access_status=access_status, num_of_ISOs=num_of_ISOs,
    # num_of_active=num_of_active, num_of_defaulted_advs=num_of_defaulted_advs, num_of_closed_advs=num_of_closed_advs, total_cash_out=total_cash_out, total_expected_profit=total_expected_profit, merchant_count=merchant_count,
    # average_factor=average_factor, total_expected_repayment=total_expected_repayment, total_payback_todate=total_payback_todate, profits_to_date=profits_to_date, open_total_cash_out=open_total_cash_out, total_in_collections=total_in_collections,
    # open_total_expected_repayment=open_total_expected_repayment, open_total_expected_profit=open_total_expected_profit, open_total_payback_todate=open_total_payback_todate, open_average_factor=open_average_factor, open_profits_to_date=open_profits_to_date,
    # bottom_cash_ad_list=bottom_cash_ad_list, top_cash_ad_list=top_cash_ad_list, top_payback_todate_list=top_payback_todate_list, bottom_payback_todate_list=bottom_payback_todate_list, open_percentage_list_top=open_percentage_list_top, open_percentage_list_bottom=open_percentage_list_bottom,
    # synd_amount=synd_amount, synd_label=synd_label, num_of_synd=num_of_synd, num_of_open_advs=num_of_open_advs, notification_count=notification_count, portfolio_list=portfolio_list, payment_error_list=payment_error_list, num_of_collections_advs=num_of_collections_advs, num_of_legal_advs=num_of_legal_advs)
