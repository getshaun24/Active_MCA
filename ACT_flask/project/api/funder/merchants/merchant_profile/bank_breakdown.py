from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db
from project.api.plaid import merchant_plaid_pull
import jinja2
from datetime import datetime
import calendar


Bank_Breakdown_Blueprint = Blueprint('MCA_Bank_Breakdown', __name__)
@Bank_Breakdown_Blueprint.route('/api/funder/merchants/merchant_profile/bank_breakdown/', methods=['GET', 'POST']) # <- from '/'
def MCA_Bank_Breakdown():



    if session.get("access_status") != "admin":
        return redirect(url_for('MCA_Login'))

    mongoDB = db[session.get("user_database")]

    user_table = db.Credentials.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]
    notification_count = user_table["notification_count"]


    most_recent = True
    from_dash = request.args.get('dash', False) == 'True'
    print("FROM DASH", from_dash)
    company_id_var = request.args.get('mid', None)
    pull_date = request.args.get('ppd', '')
    if pull_date != '':
        most_recent = False
    # company_id_var_full = request.args.get('company_id_var', None)
    # if '_dash' in company_id_var_full:
    #     from_dash = True
    #     cash_ad_var = company_id_var_full[38:]
    #     company_id_var_full = company_id_var_full[:32]
    #     print('dash ------------ ---- ----- --> ', company_id_var_full, file=sys.stderr)
    #     print('cash_ad_var ------------ ---- ----- --> ', cash_ad_var, file=sys.stderr)

    # if '___date___' in company_id_var_full:
    #     company_id_var = company_id_var_full[:32]
    #     current_date = company_id_var_full[42:]
    #     most_recent = False
    #     print('company_id_var ------------ ---- ----- --> ', company_id_var, file=sys.stderr)
    #     print('current_date ------------ ---- ----- --> ', current_date, file=sys.stderr)
    # else:
    #     company_id_var = company_id_var_full[:32]
    #     print('company_id_var ------------ ---- ----- --> ', company_id_var, file=sys.stderr)


    company = mongoDB.Merchants.find_one({ "company_ID": company_id_var })

    # if from_dash == True:
    #     contract_count = 0
    #     for contract in company['cash_advance_contracts']:
    #         if contract['contract_ID'] == cash_ad_var:
    #             break
    #         else:
    #             contract_count += 1

    #     contract_ID = company['cash_advance_contracts'][contract_count]['contract_ID']
    # else:
    #     contract_ID = ''
    contract_ID = ''


    pull_dates = []
    for info in company['plaid_pull']:
        pull_dates.append(info['pull_date'])

    print('pull_dates ------------ ---- ----- --> ', pull_dates, file=sys.stderr)
    pull_len = len(pull_dates)


    if most_recent == True:
        current_pull_date = pull_dates[-1]
        try:
            previous_pull_date = pull_dates[-2]
        except:
            previous_pull_date = 'None'
    else:
        current_pull_date = pull_date
        pull_index = pull_dates.index(pull_date)
        if pull_index == 0:
            previous_pull_date = pull_dates[-1]
        else:
            previous_pull_date = pull_dates[(pull_index - 1)]

    auth_list = []
    account_list = []
    transactions_list = []
    address_list = []
    emails_list = []
    phones_list = []
    names_list = []
    months_list = []
    years_list = []
    deposit_dict = {}
    # pull_date = ''
    for info in company['plaid_pull']:
        if current_pull_date == info['pull_date']:
            pull_date = info['pull_date']
            print('pull_date ------------ ---- ----- --> ', pull_date, file=sys.stderr)
            account_names = {}
            for aa in info['auth']['accounts']:
                print('aa id: -------------------' + str(aa['account_id']))
                print('aa name: -------------------' + str(aa['name']))
                account_names[aa['account_id']] = aa['name']
            print('Account Names: ' + str(account_names))
            for ach in info['auth']['numbers']['ach']:
                account_name = account_names[ach['account_id']]
                account_number = ach['account']
                rounting_number = ach['routing']
                auth_list.append([account_name, account_number, rounting_number])
            print('Auth List: ' + str(auth_list))
            for a in info['identity']['accounts']:
                for owner in a['owners']:
                    for name in owner['names']:
                        if name not in names_list:
                            names_list.append(name)
                    for address in owner['addresses']:
                        address_string = address['data']['street'] + " " + address['data']['city'] + ", " + address['data']['region'] + " " + address['data']['postal_code'] + " " + address['data']['country']
                        address_final = ""
                        if address['primary'] == True:
                            address_final = '--------------- Primary --------------- ' + address_string
                        else:
                            address_final = address_string
                        if address_final not in address_list:
                            address_list.append(address_final)
                    print(address_list)
                    for email in owner['emails']:
                        email_string = email['data']
                        email_final = ""
                        if email['primary'] == True:
                            email_final = '--------------- Primary --------------- ' + email_string
                        else:
                            email_final = email_string
                        if email_final not in emails_list:
                            emails_list.append(email_string)
                    for phone in owner['phone_numbers']:
                        phone_string = phone['data'] + ' --- ' + phone['type']
                        phone_final = ""
                        if phone['primary'] == True:
                            phone_final = '--------------- Primary --------------- ' + phone_string
                        else:
                            phone_final = phone_string
                        if phone_final not in phones_list:
                            phones_list.append(phone_final)

                account_name = a['name']
                subtype = a['subtype']
                available_balance = a['balances']['available']
                current_balance = a['balances']['current']
                currency = a['balances']['iso_currency_code']
                limit = a['balances']['limit']
                account_list.append([account_name, subtype, available_balance, current_balance, currency, limit])


            for trans in info['transactions']:
                account_name = trans['account_name']
                amount = trans['amount']
                date = trans['date']
                merchant_name = trans['merchant_name']
                pending = trans['pending']
                currency = trans['iso_currency_code']
                transactions_list.append([account_name, amount, date, merchant_name, pending, currency])


                if amount < 0:
                    withdrawl_amount = amount
                    deposit_amount = 0
                else:
                    deposit_amount = amount
                    withdrawl_amount = 0
                dt = datetime.strptime(date, '%Y-%m-%d' )
                month = calendar.month_name[dt.month]
                year = dt.year
                if year not in deposit_dict:
                    deposit_dict.update({year:{month: { "deposit_amount":0, "withdrawl_amount":0 }}})
                elif month not in deposit_dict[year]:
                    deposit_dict[year].update({month: {"deposit_amount":0, "withdrawl_amount":0}})

                deposit_dict[year][month]["deposit_amount"] = deposit_dict[year][month]["deposit_amount"] + deposit_amount
                deposit_dict[year][month]["withdrawl_amount"] = deposit_dict[year][month]["withdrawl_amount"] + withdrawl_amount



            print('deposit_dict ---------------------------------------------------> ', deposit_dict, file=sys.stderr)


            deposit_list = []
            for year, val in deposit_dict.items():
                print('val ---------------------------------------------------> ', val, file=sys.stderr)
                for month, v in val.items():
                    print('v ---------------------------------------------------> ', v, file=sys.stderr)
                    deposit_amount = v["deposit_amount"]
                    withdrawl_amount = v["withdrawl_amount"]

                    print('total_avrg ---------------------------------------------------> ', deposit_amount, file=sys.stderr)
                    deposit_list.append([year, month, deposit_amount, withdrawl_amount])

            print('deposit_list ---------------------------------------------------> ', deposit_list, file=sys.stderr)


            break
    # except:
    #     print('no plaid yet')
    #     transactions_list=[],
    #     auth_list=[],
    #     account_list=[],
    #     names_list=[],
    #     address_list=[],
    #     emails_list=[],
    #     phones_list=[],
    #     deposit_list =[],
    #     pull_date='Plaid login has not yet been initiated',
    #     previous_pull_date='none'


    if request.method == 'POST':

        form_data = request.form


        access_token = company['plaid_access_token']

        print ('access-token: ', access_token, file=sys.stderr)

        print('Pulling Plaid data ----------------------------------------------->', file=sys.stderr)

        merchant_plaid_pull(access_token, db, company_id_var)

        flash(u'New Updated Bank Breakdown Added', 'flash_success')

        # identity_response = plaid_client.Identity.get(access_token)
        # print('identity_response: ', identity_response["accounts"] , file=sys.stderr)
        #
        # print('66 66 66 66 66 66 66 6 6 6 6 6 6 6 ------------------------------------------------>', file=sys.stderr)
        # print('66 66 66 66 66 66 66 6 6 6 6 6 6 6 ------------------------------------------------>', file=sys.stderr)
        #
        # identity_response_list = []
        # for acc in identity_response["accounts"]:
        #     address_list = []
        #     email_list = []
        #     phone_list = []
        #     names_list = acc["owners"][0]["names"]
        #     for address in acc["owners"][0]["addresses"]:
        #         address_full = address["data"]["street"] + ' ' + address["data"]["city"] + ' ' + address["data"]["region"] + ' ' + address["data"]["country"] + ' ' + address["data"]["postal_code"]
        #         is_primary = address["primary"]
        #         address_list.append({"address":address_full, "is_primary":is_primary})
        #         print('address 2------------------------------------------------>', address, file=sys.stderr)
        #     for emails in acc["owners"][0]["emails"]:
        #         email = emails["data"]
        #         is_primary = emails["primary"]
        #         email_list.append({"email":email, "is_primary":is_primary})
        #         print('emails ------------------------------------------------>', emails, file=sys.stderr)
        #     for phone in acc["owners"][0]["phone_numbers"]:
        #         phone_num = phone["data"]
        #         is_primary = emails["primary"]
        #         phone_type = phone["type"]
        #         phone_list.append({"phone":phone_num, "is_primary":is_primary, "type":phone_type})
        #         print('phone 2------------------------------------------------>', phone, file=sys.stderr)
        #
        #     new_dict = {"names":names_list, "address":address_list, "emails":email_list, "phones":phone_list }
        #     if new_dict not in identity_response_list:
        #         identity_response_list.append({"names":names_list, "address":address_list, "emails":email_list, "phones":phone_list })
        #
        #
        # #identity_response_list_unique = [dict(t) for t in {tuple(d.items()) for d in identity_response_list}]
        # #identity_response_list_unique = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in identity_response_list)]
        #
        #
        # print('identity_response_list ------------------------------------------------>', identity_response_list, file=sys.stderr)
        #
        #
        # print('99------------------------------------------------>', file=sys.stderr)
        # print('99------------------------------------------------>', file=sys.stderr)
        #
        # # Retrieve Transactions for an Item
        # # Pull transactions for the last 30 days
        # start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-731))
        # end_date = '{:%Y-%m-%d}'.format(datetime.now())
        # try:
        #
        #     transactions_response = plaid_client.Transactions.get(access_token, start_date=start_date, end_date=end_date)
        #
        # #    pretty_print_response(transactions_response)
        # #    print(transactions_response, file=sys.stderr)
        # except plaid.errors.PlaidError as e:
        #     print(jsonify(format_error(e)), file=sys.stderr)
        #
        #
        #
        # transaction_list = []
        # for acc in transactions_response["accounts"]:
        #     account_name = acc["name"]
        #     account_id = acc["account_id"]
        #     print('account_name ------------------------------------------------>', account_name, file=sys.stderr)
        #     for trans in transactions_response["transactions"]:
        #         if trans["account_id"] == account_id:
        #             amount = trans["amount"]
        #             date = trans["date"]
        #             merchant_name = trans["merchant_name"]
        #             pending = trans["pending"]
        #             currency = trans["iso_currency_code"]
        #             print('amount ------------------------------------------------>', amount, file=sys.stderr)
        #             transaction_list.append({"account_name": account_name, "amount": amount, "date": date, "merchant_name":merchant_name, "pending":pending, "curreny":currency})
        #
        #
        #
        #
        #
        # print('transaction_list ------------------------------------------------>', transaction_list, file=sys.stderr)
        #
        # print('1010------------------------------------------------>', file=sys.stderr)
        # print('1010------------------------------------------------>', file=sys.stderr)
        #
        #
        # try:
        #     auth_response = plaid_client.Auth.get(access_token)
        # #    pretty_print_response(auth_response)
        # #    print(auth_response, file=sys.stderr)
        #
        #     auth_response_list = []
        #     for ach in auth_response["numbers"]["ach"]:
        #         routing = ach["routing"]
        #         wire_routing = ach["wire_routing"]
        #         for acc in auth_response["accounts"]:
        #             account_name = acc["name"]
        #             if acc["account_id"] == ach["account_id"]:
        #                 auth_response_list.append({"account_name": account_name, "account_number": routing, "rounting_number": wire_routing})
        #
        #     accounts_list = []
        #     for acc in auth_response["accounts"]:
        #         account_name = acc["name"]
        #         available_balance = acc["balances"]["available"]
        #         current_balance = acc["balances"]["current"]
        #         currency = acc["balances"]["iso_currency_code"]
        #         limit = acc["balances"]["limit"]
        #         subtype= acc["subtype"]
        #         accounts_list.append({"account_name": account_name, "subtype":subtype, "available_balance": available_balance, "current_balance": current_balance, "currency":currency, "limit":limit})
        #
        #
        # except plaid.errors.PlaidError as e:
        #     print(jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } }), file=sys.stderr)
        #
        #
        # print('1111------------------------------------------------>', file=sys.stderr)
        # print('1111------------------------------------------------>', file=sys.stderr)
        #
        # # Retrieve investment holdings data for an Item
        # # https://plaid.com/docs/#investments
        # #try:
        # #    holdings_response = plaid_client.Holdings.get(access_token)
        # #    pretty_print_response(holdings_response)
        # #    print(holdings_response, file=sys.stderr)
        # #except plaid.errors.PlaidError as e:
        # #    print(jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } }), file=sys.stderr)
        #
        # print('1212------------------------------------------------>', file=sys.stderr)
        # print('1212------------------------------------------------>', file=sys.stderr)
        #
        #
        # # Retrieve Investment Transactions for an Item
        # # https://plaid.com/docs/#investments
        # # Pull transactions for the last 30 days
        # #start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-360))
        # #end_date = '{:%Y-%m-%d}'.format(datetime.now())
        # #try:
        # #    investment_transactions_response = plaid_client.InvestmentTransactions.get(access_token, start_date, end_date)
        # #    pretty_print_response(investment_transactions_response)
        # #    print(investment_transactions_response, file=sys.stderr)
        # #except plaid.errors.PlaidError as e:
        # #    print(jsonify({'error': None, 'investment_transactions': investment_transactions_response}), file=sys.stderr)
        #
        #
        # print('1313------------------------------------------------>', file=sys.stderr)
        # print('1313------------------------------------------------>', file=sys.stderr)
        #
        #
        # mongoDB.Company.update({"company_ID": company_id_var},{"$push": {"Plaid_Pull": {"Pull_date":'{:%Y-%m-%d}'.format(datetime.now()), "Auth":auth_response_list, "Identity":identity_response_list, "Accounts":accounts_list, "Transactions":transaction_list }}});
        #
        #
        # print('1515------------------------------------------------>', file=sys.stderr)
        # print('1515------------------------------------------------>', file=sys.stderr)




    return render_template("/Funder/Merchants/Merchant_Profile/Bank_Breakdown/bank_breakdown.html", transactions_list=transactions_list, auth_list=auth_list, account_list=account_list, names_list=names_list, address_list=address_list, emails_list=emails_list, phones_list=phones_list, pull_date=pull_date, previous_pull_date=previous_pull_date, mid=company_id_var, access_status=access_status, notification_count=notification_count, deposit_list=deposit_list, from_dash=from_dash, contract_ID=contract_ID)
