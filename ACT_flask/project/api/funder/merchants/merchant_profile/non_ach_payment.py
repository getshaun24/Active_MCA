from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
import datetime


Non_ACH_Payment_Blueprint = Blueprint('MCA_Non_ACH_Payment', __name__)
@Non_ACH_Payment_Blueprint.route('/api/funder/merchants/merchant_profile/non_ach_payment/', methods=['GET', 'POST']) 
def MCA_Non_ACH_Payment():


    if not session.get("email"):
        return redirect(url_for('MCA_Login.MCA_Login'))

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        if access_status != "admin":
            return redirect(url_for('MCA_Login.MCA_Login'))




        company_id_var_full = request.args.get('company_id_var', None)
        company_id_var = company_id_var_full[:32]
        cash_ad_var = company_id_var_full[35:]

        print(' company_id_var_full --------------------------------------------------->', company_id_var_full, file=sys.stderr)
        print(' company_id_var --------------------------------------------------->', company_id_var, file=sys.stderr)
        print(' cash_ad_var --------------------------------------------------->', cash_ad_var, file=sys.stderr)





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

        contract_count = 0
        for contract in company_info['Cash_Advance_Contracts']:
            if contract['contract_ID'] == cash_ad_var:
                print(' contract --------------------------------------------------->', contract['contract_ID'], file=sys.stderr)
                break
            else:
                contract_count += 1


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
        commission = company_info['Cash_Advance_Contracts'][contract_count]['commission']
        default_amount = company_info['Cash_Advance_Contracts'][contract_count]['default_amount']
        total_amount_repaid = company_info['Cash_Advance_Contracts'][contract_count]['total_amount_repaid']
        percent_paid = company_info['Cash_Advance_Contracts'][contract_count]['percent_paid']
        syndicators = company_info['Cash_Advance_Contracts'][contract_count]['Syndicators']
        ACH_pull_sched = company_info['Cash_Advance_Contracts'][contract_count]['ACH_pull_schedule']

        try:
            current_pause_until = datetime.strptime(company_info['Cash_Advance_Contracts'][contract_count]['pause_until'], '%Y-%m-%d' )
        except:
            current_pause_until = company_info['Cash_Advance_Contracts'][contract_count]['pause_until']

        transaction_table = company_info['Cash_Advance_Contracts'][contract_count]['Transaction_track']


        try:
            payback_table_results = []
            for transaction in transaction_table:
                payback_table_results.append([transaction['transaction_num'], transaction['transaction_date'], transaction['transaction_confirmed_date'], transaction['transaction_amount'], transaction['total_amount_repaid'], transaction['open_percent_paid'], transaction['note'], transaction['transaction_ID'], transaction['status'], transaction['error']])
        except:
            payback_table_results = []




        if request.method == 'POST':


            form_data = request.form
            print(form_data, file=sys.stderr)


            transaction_amount = float(form_data["transaction_amount"])
            transaction_date = form_data["transaction_date"]


            if form_data["transaction_confirmed_date"]:
                transaction_confirmed_date = form_data["transaction_confirmed_date"]
            else:
                transaction_confirmed_date = ' '
            if form_data["note"]:
                note = form_data["note"]
            else:
                note = ' '
            if form_data["transaction_ID"]:
                transaction_ID = form_data["transaction_ID"]
            else:
                transaction_ID = ' '
            if form_data["status"]:
                status = form_data["status"]
            else:
                status = ' '
            if form_data["error"]:
                error = form_data["error"]
            else:
                error = ' '



            #-------------------- Math --------------------


            #-----------------------------------------------

            try:
                print(' Default --------------------------------------------------->', file=sys.stderr)
                payback_latest_row = payback_table_results[-1]
                payment_num = int(payback_latest_row[0]) + 1
                print(' Default 1 --------------------------------------------------->', file=sys.stderr)
                if status == "Defaulted":
                    print(' Default 2 --------------------------------------------------->', file=sys.stderr)
                    default_amount_repaid = round(float(default_amount_repaid) + transaction_amount, 2)
                    total_amount_repaid = round(float(default_amount_repaid) + transaction_amount, 2)
                    default_percent_paid = round(total_percent_paid / float(expected_repayment_amount) * 100, 2)
                    total_percent_paid = round(total_percent_paid / float(expected_repayment_amount) * 100, 2)
                    print(' default_percent_paid --------------------------------------------------->', default_percent_paid, file=sys.stderr)
                    print(' default_amount_repaid --------------------------------------------------->', default_amount_repaid, file=sys.stderr)
                else:
                    open_amount_repaid = round(float(open_amount_repaid) + transaction_amount, 2)
                    total_amount_repaid = round(float(open_amount_repaid) + transaction_amount, 2)
                    open_percent_paid = round(open_amount_repaid / float(expected_repayment_amount) * 100, 2)
                    total_percent_paid = round(total_percent_paid / float(expected_repayment_amount) * 100, 2)
                    print(' Default 4 --------------------------------------------------->', file=sys.stderr)
            except:
                payment_num = 1
                if status == "Defaulted":
                    default_amount_repaid = round(transaction_amount, 2)
                    total_amount_repaid = round(transaction_amount, 2)
                    default_percent_paid = round(total_amount_repaid / float(expected_repayment_amount) * 100, 2)
                    total_percent_paid = round(total_amount_repaid / float(expected_repayment_amount) * 100, 2)
                else:
                    open_amount_repaid = round(transaction_amount, 2)
                    total_amount_repaid = round(transaction_amount, 2)
                    open_percent_paid = round(total_amount_repaid / float(expected_repayment_amount) * 100, 2)
                    total_percent_paid = round(total_amount_repaid / float(expected_repayment_amount) * 100, 2)


            print(' Default 5 --------------------------------------------------->', file=sys.stderr)
            transaction_date = datetime.today().strftime('%Y-%m-%d')

            print(' Default 6 --------------------------------------------------->', file=sys.stderr)
            for key, val in syndicators.items():
                print(' synd 1 --------------------------------------------------->', file=sys.stderr)
                synd_collection = mongoDB.Syndicators.find_one({ "syndicator_business_name": key })
                syndicated_percent = float(val) / float(advance_amount)
                print(' synd 2 --------------------------------------------------->', file=sys.stderr)
                rev_amount = round(float(synd_collection['revenue']) + (float(total_amount_repaid) * syndicated_percent),2)
                mongoDB.Syndicators.update({ "syndicator_business_name": key }, {"$set": {'revenue': rev_amount}});
                print(' synd 3 --------------------------------------------------->', file=sys.stderr)


            print(' Default 7 --------------------------------------------------->', file=sys.stderr)

            transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track"
            contract_var_repaid = "Cash_Advance_Contracts." + str(contract_count) + ".open_amount_repaid"
            contract_var_default_repaid = "Cash_Advance_Contracts." + str(contract_count) + ".default_amount_repaid"
            contract_var_total_repaid = "Cash_Advance_Contracts." + str(contract_count) + ".total_amount_repaid"
            contract_var_percent = "Cash_Advance_Contracts." + str(contract_count) + ".open_percent_paid"
            contract_var_default_percent = "Cash_Advance_Contracts." + str(contract_count) + ".default_percent_paid"
            contract_var_total_percent = "Cash_Advance_Contracts." + str(contract_count) + ".total_percent_paid"
            contract_var_status = "Cash_Advance_Contracts." + str(contract_count) + ".status"

            print(' Default 8 --------------------------------------------------->', file=sys.stderr)

            if total_amount_repaid >= expected_repayment_amount:
                print(' mongo 1 --------------------------------------------------->', file=sys.stderr)
                mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_repaid: open_amount_repaid, contract_var_percent: open_percent_paid, contract_var_default_repaid:default_amount_repaid, contract_var_default_percent:default_percent_paid, contract_var_total_percent:total_percent_paid, contract_var_total_repaid:total_amount_repaid, contract_var_status:"Closed"}});
                print(' mongo 2 --------------------------------------------------->', file=sys.stderr)
            else:
                print(' mongo 3 --------------------------------------------------->', file=sys.stderr)
                mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_repaid: open_amount_repaid, contract_var_percent: open_percent_paid, contract_var_default_repaid:default_amount_repaid, contract_var_default_percent:default_percent_paid, contract_var_total_percent:total_percent_paid, contract_var_total_repaid:total_amount_repaid}});
                print(' mongo 4 --------------------------------------------------->', file=sys.stderr)
            print(' Default 9 --------------------------------------------------->', file=sys.stderr)


            mongoDB.Company.update({"company_ID": company_ID}, {"$push": {transaction_var: { "transaction_num": payment_num, "transaction_date": transaction_date, "transaction_confirmed_date":transaction_confirmed_date, "transaction_amount":transaction_amount, "open_amount_repaid":open_amount_repaid,  "default_amount_repaid":default_amount_repaid, "total_amount_repaid":total_amount_repaid, "open_percent_paid":open_percent_paid, "default_percent_paid":default_percent_paid, "total_percent_paid":total_percent_paid, "note":note, "transaction_ID":transaction_ID, "status":status, "error":error}}});




            print('transaction transacted', file=sys.stderr)


    return render_template("/Funder/Merchants/Merchant_Profile/Non_ACH_Payment/non_ach_payment.html", company_DBA=company_DBA, company_id_var=company_id_var, access_status=access_status, notification_count=notification_count, company_id_var_full=company_id_var_full)
