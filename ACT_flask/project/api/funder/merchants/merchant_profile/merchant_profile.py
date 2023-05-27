from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
# from server import mongoDB_master_access, dwolla_app_token
from project import db
from project.api.dwolla import dwolla_app_token
from project.api.functions import transfer_failure_retrieve
from datetime import datetime, timedelta
from project.api.functions import ACH_pull_schedule_format
import re



Merchant_Profile_Blueprint = Blueprint('MCA_Merchant_Profile', __name__)
@Merchant_Profile_Blueprint.route('/api/funder/merchants/merchant_profile/merchant_profile/', methods=['GET', 'POST']) # <- from '/'
def MCA_Merchant_Profile():



    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongo_master = db.Master_Credentials.master_user_list.find_one({ "email": session.get("email") })
        dwolla_funding_source_destination_account = "https://api-sandbox.dwolla.com/funding-sources/" + mongo_master["dwolla_funding_source_destination_account"]

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]


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
        ACH_pull_sched_var = company_info['Cash_Advance_Contracts'][contract_count]['ACH_pull_schedule']
        #initiated_email = company_info['Cash_Advance_Contracts'][contract_count]['initiated_email']
        try:
            current_pause_until = (datetime.strptime(company_info['Cash_Advance_Contracts'][contract_count]['pause_until'], '%Y-%m-%d' ))
        except:
            current_pause_until = company_info['Cash_Advance_Contracts'][contract_count]['pause_until']

        transaction_table = company_info['Cash_Advance_Contracts'][contract_count]['Transaction_track']

        today_date = datetime.today()


        ACH_pull_sched, day_of_week = ACH_pull_schedule_format(ACH_pull_sched_var)


        if current_pause_until != "None":
            #get the day of week pause until falls on
            current_pause_weekday = current_pause_until.weekday()
            if current_pause_weekday == 5 or current_pause_weekday == 6:
                current_pause_weekday = 0

            days_ahead = day_of_week - current_pause_weekday
            if ACH_pull_sched == 'Weekdays':
                days_ahead = 0
            elif days_ahead < 0: # Target day already happened this week
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
        try:
            payback_table_results = []
            for transaction in transaction_table:
                payback_table_results.append([transaction['transaction_num'], transaction['transaction_date'], transaction['transaction_confirmed_date'], transaction['transaction_amount'], transaction['total_amount_repaid'], transaction['note'], transaction['transaction_ID'], transaction['status'], transaction['error']])
                if transaction['transaction_confirmed_date'] == "Pending":
                    pending_balance += transaction['transaction_amount']

        except:
            payback_table_results = []



        print(' 00000 --------------------------------------------------->', payback_table_results, file=sys.stderr)
        total_amount_repaid_list = [float(item[4]) for item in payback_table_results]

        print(' 00000 --------------------------------------------------->', file=sys.stderr)


        if request.method == 'POST':

            print(' 1010101 --------------------------------------------------->', file=sys.stderr)

            form_data = request.form

            contract_var_schedule = "Cash_Advance_Contracts." + str(contract_count) + ".ACH_pull_schedule"
            contract_var_pause = "Cash_Advance_Contracts." + str(contract_count) + ".pause_until"
            contract_var_status = "Cash_Advance_Contracts." + str(contract_count) + ".status"
            contract_var_default = "Cash_Advance_Contracts." + str(contract_count) + ".default_amount"

            print(' 00000 --------------------------------------------------->', form_data, file=sys.stderr)



            try:
                pause_until_format = form_data['pause_until']
                paust_until_dt = datetime.strptime(pause_until_format, '%Y-%m-%d')
                if paust_until_dt < today_date:
                    mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_pause:"None"}});
                    flash(u'Pause Until Ended', 'flash_success')
                else:
                    mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_pause:pause_until_format}});
                    flash(u'Now Pausing All Automatic Transactions Until ' + pause_until_format, 'flash_success')

                # set new pause_until variable so it updates on form submit
                #pause_until_format = pause_until #format the pause until date

                # set new pause_until variable so it updates on form submit and make sure it is a weekday
                if paust_until_dt.weekday() == 5:
                    cancel_next_day = paust_until_dt + timedelta(2)
                    pause_until_format = (cancel_next_day + timedelta(1)).strftime('%Y-%m-%d')
                    cancel_next_weekday = 0
                elif paust_until_dt.weekday() == 6:
                    cancel_next_day = pause_until_format + timedelta(1)
                    pause_until_format = (cancel_next_day + timedelta(1)).strftime('%Y-%m-%d')
                    cancel_next_weekday = 0
                else:
                    cancel_next_day = paust_until_dt
                    pause_until_format = (cancel_next_day + timedelta(1)).strftime('%Y-%m-%d')
                    cancel_next_weekday = paust_until_dt.weekday()
                # set new next_day variable so it updates on form submit
                #cancel_next_weekday = cancel_next.weekday()
                #if cancel_next_weekday == 5 or cancel_next_weekday == 6:
                #    cancel_next_weekday = 0

                days_ahead = day_of_week - cancel_next_weekday
                if ACH_pull_sched == 'Weekdays':
                    days_ahead = 1
                elif days_ahead < 0: # Target day already happened this week
                    days_ahead += 7

                next_day = (cancel_next_day + timedelta(days_ahead)).strftime('%Y-%m-%d')

            except:
                print ('no pause update')



            try:
                cancel_next = datetime.strptime(form_data['cancel_next'], '%Y-%m-%d' )
                print(' cancel_next --------------------------------------------------->', cancel_next, file=sys.stderr)
                #pause_until = (cancel_next + timedelta(1)).strftime('%Y-%m-%d')
                print(' cancel_next --------------------------------------------------->', cancel_next, file=sys.stderr)

                # set new pause_until variable so it updates on form submit and make sure it is a weekday
                if cancel_next.weekday() == 5:
                    cancel_next_day = cancel_next + timedelta(2)
                    pause_until_format = (cancel_next_day + timedelta(1)).strftime('%Y-%m-%d')
                    cancel_next_weekday = 0
                elif cancel_next.weekday() == 6:
                    cancel_next_day = cancel_next + timedelta(1)
                    pause_until_format = (cancel_next_day + timedelta(1)).strftime('%Y-%m-%d')
                    cancel_next_weekday = 0
                else:
                    cancel_next_day = cancel_next
                    pause_until_format = (cancel_next_day + timedelta(1)).strftime('%Y-%m-%d')
                    cancel_next_weekday = cancel_next.weekday()
                # set new next_day variable so it updates on form submit
                #cancel_next_weekday = cancel_next.weekday()
                #if cancel_next_weekday == 5 or cancel_next_weekday == 6:
                #    cancel_next_weekday = 0

                days_ahead = day_of_week - cancel_next_weekday
                if ACH_pull_sched == 'Weekdays':
                    days_ahead = 1
                elif days_ahead < 0: # Target day already happened this week
                    days_ahead += 7

                next_day = (cancel_next_day + timedelta(days_ahead)).strftime('%Y-%m-%d')

                mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_pause:pause_until_format}});
                flash(u'Next Transaction Canceled', 'flash_success')



            except:
                print ('no cancel update')


            try:
                schedule_update = form_data['schedule_update']
                mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_schedule:schedule_update}});

                # set new schedule variable so it updates on form submit
                ACH_pull_sched, day_of_week = ACH_pull_schedule_format(schedule_update)

                flash(u'Schedule Updated', 'flash_success')
            except:
                print ('no status update')


            try:
                status_update = form_data['status_update']
                mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_status:status_update}});
                if status_update == "Defaulted" or status_update == "Collections":
                    defaulted_amount = expected_repayment_amount - total_amount_repaid
                    mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_default:defaulted_amount}});
                if status_update == "Open":
                    mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_default:0}});

                # set new status variable so it updates on form submit
                status = status_update
                flash(u'Status Updated', 'flash_success')
            except:
                print ('no status update')


            try:

                non_decimal = re.compile(r'[^\d.]+')
                manual_pull_amount = round(float(non_decimal.sub('',form_data['manual_pull_amount'])),2)
                manual_pull_note = form_data['manual_pull_note']


                print(' 56565656 --------------------------------------------------->', file=sys.stderr)


                print(' 11111 --------------------------------------------------->', file=sys.stderr)

                full_customer_url = 'https://api-sandbox.dwolla.com/customers/' + dwolla_customer_url_id

                funding_sources = dwolla_app_token.get('%s/funding-sources' % full_customer_url)
                fs_id = funding_sources.body['_embedded']['funding-sources'][0]['id']

                print(' 22222 --------------------------------------------------->', file=sys.stderr)


                request_body = {
                        '_links': {
                            'source': {
                                'href': 'https://api-sandbox.dwolla.com/funding-sources/'  + fs_id
                                        },
                            'destination': {
                                'href': dwolla_funding_source_destination_account
                                        }
                            },
                        'amount': {
                            'currency': 'USD',
                            'value': manual_pull_amount
                            },
                        'clearing': {
                            'destination': 'next-available'
                            }
                        }


                print(' request_body --------------------------------------------------->', request_body, file=sys.stderr)


                if True:
                    transfer = dwolla_app_token.post('transfers', request_body)
                    transfer_url = transfer.headers['location']
                    transfer_id = transfer_url[41:]

                    print(' transfer_url --------------------------------------------------->', transfer_url, file=sys.stderr)


                    transfer_retrieve = dwolla_app_token.get(transfer_url)
                    try:
                        transfer_status = transfer_retrieve.body['status']
                    except:
                        transfer_status = 'no_status'


                    print(' 22 --------------------------------------------------->', file=sys.stderr)

                    transaction_date = datetime.today().strftime('%Y-%m-%d')
                    try:
                        payback_latest_row = payback_table_results[-1]
                        payment_num = int(payback_latest_row[0]) + 1
                    except:
                        payment_num = 1


                    try:
                        transfer_failure_code, failure_reason, transfer_status = transfer_failure_retrieve(transfer_url) #call function at bottom of page

                        print('Failure Reason --> ', failure_reason, file=sys.stderr)



                        transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track"
                        mongoDB.Company.update({"company_ID": company_ID}, {"$push": {transaction_var: { "transaction_num": payment_num, "transaction_date": transaction_date, "transaction_confirmed_date":"Failed", "transaction_amount":manual_pull_amount, "total_amount_repaid":total_amount_repaid, "default_amount":default_amount, "percent_paid":percent_paid, "note":manual_pull_note, "transaction_ID":transfer_id, "status":transfer_status, "error":failure_reason}}});

                        # add to payback table so visible on form submit
                        payback_table_results.append([payment_num, transaction_date, "Failed", manual_pull_amount, total_amount_repaid, manual_pull_note, transfer_id, transfer_status, failure_reason])

                        flash(u'Failed transaction -- ' + failure_reason, 'flash_error')

                    except:
                        failure_reason = "None"
                        print('No Failure', file=sys.stderr)



                        print(' 1 --------------------------------------------------->', file=sys.stderr)

                        print(' 1 --------------------------------------------------->', file=sys.stderr)


                        print(' Default 7 --------------------------------------------------->', file=sys.stderr)

                        transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track"

                        print(' Default 8 --------------------------------------------------->', file=sys.stderr)

                        mongoDB.Company.update({"company_ID": company_ID}, {"$push": {transaction_var: { "transaction_num": payment_num, "transaction_date": transaction_date, "transaction_confirmed_date":"Pending", "transaction_amount":manual_pull_amount, "total_amount_repaid":total_amount_repaid, "default_amount":default_amount, "percent_paid":percent_paid, "note":manual_pull_note, "transaction_ID":transfer_id, "status":transfer_status, "error":failure_reason}}});


                        # add to payback table so visible on form submit
                        payback_table_results.append([payment_num, transaction_date, "Pending", manual_pull_amount, total_amount_repaid, manual_pull_note, transfer_id, transfer_status, failure_reason])




                        print('transaction transacted', file=sys.stderr)
                        flash(u'Success Manual Transaction Initiated', 'flash_success')


                else:
                    print('Transaction Process failed', file=sys.stderr)

            except:
                print('Transaction Process failed', file=sys.stderr)





        return render_template("/Funder/Merchants/Merchant_Profile/Merchant_Profile/merchant_profile.html", merchant_view=merchant_view, synd_name=synd_name, admin_view=admin_view, contract_ID=contract_ID, payback_table_results=payback_table_results, access_status=access_status, notification_count=notification_count,
        funder=funder, under_writer=under_writer, iso=iso, sales_rep=sales_rep, mcc=mcc, sic=sic, business_description=business_description, total_amount_repaid_list=total_amount_repaid_list, cash_ad_var=cash_ad_var, contract_count_show=contract_count_show, pending_balance=pending_balance,
        company_ID=company_ID, status=status, start_date=start_date, expected_end_date=expected_end_date, split_percent=split_percent, factor_rate=factor_rate, funded_via=funded_via, fico_score=fico_score, position=position, tags=tags, advance_amount=advance_amount,
        legal_company_name=legal_company_name, company_DBA=company_DBA, poc_first_name=poc_first_name, poc_last_name=poc_last_name, poc_email=poc_email, poc_phone=poc_phone, total_amount_repaid=total_amount_repaid, percent_paid=percent_paid, ACH_pull_sched=ACH_pull_sched, pause_until_format=pause_until_format,
        expected_repayment_amount=expected_repayment_amount, company_id_var_full=company_id_var_full, company_id_var=company_id_var, advance_view=advance_view, syndicator_view=syndicator_view, next_day=next_day, pull_amount=pull_amount, default_amount=default_amount
        )
