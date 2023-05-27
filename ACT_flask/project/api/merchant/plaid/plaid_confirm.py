from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db
import plaid
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from flask import request
from project.api.plaid import merchant_plaid_pull
from project.api.functions import pretty_print_response
from plaid.model.products import Products
from plaid.exceptions import ApiException
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
# from server import plaid_client, is_live_production_env
from project.api.plaid import plaid_client, format_plaid_error
from datetime import datetime, timedelta, date



Plaid_Confirm_Blueprint = Blueprint('MCA_Plaid_Confirm', __name__)
@Plaid_Confirm_Blueprint.route("/api/merchant/plaid/plaid_confirm/", methods=['GET', 'POST'])
def MCA_Plaid_Confirm():


    is_live_production_env = False
    if current_app.config['ENV'] == 'production':
        is_live_production_env = True


    dwolla_id = request.args.get('did', None)
    company_ID = request.args.get('mid', None)
    funder_id = request.args.get('fid', None)
    link_token = request.args.get('link_token', None)
    print('dwolla_id --------------------------------------------------------------------------->', dwolla_id, file=sys.stderr)
    print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)
    print('funder_id --------------------------------------------------------------------------->', funder_id, file=sys.stderr)
    

    # plaid_products = ['auth','transactions','identity'] #here b/c variable coming form ???
    # # for product in PLAID_PRODUCTS:
    # #         #plaid_products.append(Products(product))
    # #     print('product --->', product)
    # # print('plaid_products --->', plaid_products)


    # response = plaid_client.link_token_create({
    #     'user': {
    #         # This should correspond to a unique id for the current user.
    #         'client_user_id': 'user-id'
    #         # 'client_user_id': session.get('email')
    #     },
    #     'client_name': "Plaid Quickstart",
    #     'products': plaid_products,
    #     'country_codes': current_app.config['PLAID_COUNTRY_CODES'],
    #     'language': "en",
    #     #'redirect_uri': PLAID_REDIRECT_URI,
    # })


    # link_token = response['link_token']

    # print('11------------------------------------------------>', link_token, file=sys.stderr)


    # print('LINK TOKEN', link_token)


    #wrap all the following code in a 'try' because the included variables are not available until plaid returns them.
    #Need to skip this for initial page to load
    if request.method == 'POST':
    
        # trying both methods for redundancy
        # try: #try getting web info with post
        #     xx_plaid1 = request.form
        #     print ('xx_plaid1: ', xx_plaid1)
        #     public_token = request.form['public_token']
        #     print ('public_token: ', public_token)
        #     # dwolla_id = request.form['dwolla_id']
        #     # company_ID = request.form['company_ID']
        #     # print ('dwolla_id: ', dwolla_id, file=sys.stderr)
        #     # print ('company_ID: ', company_ID, file=sys.stderr)
        #     try: #if plaid select account feature
        #         selected_account_id = request.form['metadata']['account']['id']
        #         selected_account_name = request.form['metadata']['account']['id']
        #         print ('selected_account_id: ', selected_account_id, file=sys.stderr)
        #         print ('selected_account_name: ', selected_account_name, file=sys.stderr)
        #     except:
        #         print('no account selection')
        # except: #if post does not work the use Ajax
        ajax = request.get_json()
        print ('ajax: ', ajax)
        public_token = ajax['public_token']
        # dwolla_id = ajax['dwolla_id']
        # company_ID = ajax['company_ID']
        try: #if plaid select account feature
            selected_account_id = ajax['metadata']['account']['id']
            selected_account_name = ajax['metadata']['account']['id']
            print ('selected_account_id: ', selected_account_id, file=sys.stderr)
            print ('selected_account_name: ', selected_account_name, file=sys.stderr)
        except:
            print('no account selection')


        print('33------------------------------------------------>', file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)


        exchange_response = plaid_client.item_public_token_exchange(ItemPublicTokenExchangeRequest(public_token=public_token))
        print('exchange_response -->', exchange_response)

        #pretty_print_response(exchange_response.to_dict())
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']

        print('44------------------------------------------------>', file=sys.stderr)
        print('44------------------------------------------------>', file=sys.stderr)
        print ('access-token: ', access_token, file=sys.stderr)

        funder_db_name = db.Master.Funders.find_one({'company_ID': funder_id})['funder_db_name']

        for DB_name in session.get('user_databases'):
            mongoDB_merch = db[DB_name]
            if mongoDB_merch.Merchants.find({"company_ID": company_ID}).count() > 0:


                print('Company Company Company ---------------------------------------------------> ', company_ID)
                print('access_token ------>', access_token)

                mongoDB_merch.Merchants.update({"company_ID": company_ID},{"$set": {"plaid_access_token": access_token}});

                print('Plaid Added --------------------------------------------------------------------------->', file=sys.stderr)


        
        # merchant_plaid_pull(access_token, db, company_ID, funder_db_name)
        plaid_access_token = access_token
        print("Starting Plaid pull", file=sys.stderr)

        # Get identity
        identity_response = None
        try:
            print("Starting identity GET request", file=sys.stderr)
            identity_response = plaid_client.identity_get(IdentityGetRequest(access_token=plaid_access_token))
            #pretty_print_response(identity_response.to_dict())
            print('identity_response: ', identity_response , file=sys.stderr)
        except plaid.ApiException as e:
            error_response = format_plaid_error(e)
            print('Identity response error: ' + error_response, file=sys.stderr)


        # Get transactions
        transactions = None
        try:
            print('Starting first transactions pull', file=sys.stderr)
            today = date.today()
            days = timedelta(days = 730) # 2 years
            transactions_request = TransactionsGetRequest(
                access_token=plaid_access_token,
                start_date=today-days,
                end_date=today,
                options=TransactionsGetRequestOptions()
            )
            transactions_response = plaid_client.transactions_get(transactions_request)
            transactions = transactions_response['transactions']

            # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
            # retrieve all transactions
            transaction_pull_count = 1
            while len(transactions) < transactions_response['total_transactions']:
                transactions_request = TransactionsGetRequest(
                    access_token=plaid_access_token,
                    start_date=today-days,
                    end_date=today,
                    options=TransactionsGetRequestOptions(
                        offset=len(transactions)
                    )
                )
                transactions_response = plaid_client.transactions_get(transactions_request)
                transactions.extend(transactions_response['transactions'])
                transaction_pull_count += 1
                print('Transaction pull count: ' + str(transaction_pull_count), file=sys.stderr)
        except plaid.ApiException as e:
            error_response = format_plaid_error(e)
            print('Transaction error: ' + error_response, file=sys.stderr)

        # Get Auth
        auth_response = None
        try:
            print('Starting Auth pull', file=sys.stderr)
            auth_response = plaid_client.auth_get(AuthGetRequest(access_token=plaid_access_token))
        except plaid.ApiException as e:
            error_response = format_plaid_error(e)
            print('Auth error: ' + error_response, file=sys.stderr)

        identity_response = identity_response.to_dict()
        auth_response = auth_response.to_dict()
        transactions_clean = []
        # print("First transaction: " + str(transactions[0]))
        account_names = {}
        for account in transactions_response['accounts']:
            account_names[account.account_id] = account.name

        for transaction in transactions:
            t = {
                "account_id": transaction['account_id'],
                "account_name": account_names[transaction['account_id']],
                "account_owner": transaction['account_owner'],
                "amount": transaction['amount'],
                "authorized_date": transaction['authorized_date'].strftime('%Y-%m-%d'),
                "date": transaction['date'].strftime('%Y-%m-%d'),
                "merchant_name": transaction['merchant_name'],
                "payment_channel": transaction['payment_channel'],
                "pending": transaction['pending'],
                "iso_currency_code": transaction['iso_currency_code'],
                "transaction_id": transaction['transaction_id'],
                "transaction_type": transaction['transaction_type']
            }

            transactions_clean.append(t)


        #Now write to Mongo
        # mongoDB = mongo_client.Merchant_Users
        # user_table = mongoDB.merchant_users.find_one({ "email": session.get("email") })
        # all_DBs = set([item['DB_name'] for item in mongoDB_master_access.master_user_list.find()])

        # print('all_DBs ---------------------------------------------------> ', all_DBs , file=sys.stderr)

        db[funder_db_name].Merchants.update({'company_ID': company_ID}, {"$push": {
            "plaid_pull": {
                "pull_date":'{:%Y-%m-%d}'.format(datetime.now()), 
                "auth":auth_response, 
                "identity":identity_response, 
                "transactions":transactions_clean 
                }
            }})

        # for DB_name in all_DBs:
        #     mongoDB_merch = eval("mongo_client." + DB_name)
        #     print('mongoDB_merch ---------------------------------------------------> ', mongoDB_merch , file=sys.stderr)
        #     if mongoDB_merch.Company.find({"company_ID": company_ID}):

        #         print('Company Company Company ---------------------------------------------------> ', company_ID)
        #         print('access_token ------>', plaid_access_token)

        #         # mongoDB_merch.Company.update({"company_ID": company_ID},{"$set": {"plaid_access_token": access_token}});
        #         print('merch_1')
        #         mongoDB_merch.Company.update({"company_ID": company_ID},{"$push": {"Plaid_Pull": {"Pull_date":'{:%Y-%m-%d}'.format(datetime.now()), "Auth":auth_response, "Identity":identity_response, "Transactions":transactions_clean }}});


        print('Plaid Added --------------------------------------------------------------------------->', file=sys.stderr)
        # except:
        #     print('none yet')


        # secure_var_ids = str(dwolla_id) + "___" + str(company_ID)
        return redirect(url_for('MCA_Secure_Account_Select.MCA_Secure_Account_Select', did=dwolla_id, mid=company_ID, fid=funder_id))


    return render_template("/Merchant/Secure_Bank/Plaid_Confirm/plaid_confirm.html", did=dwolla_id, mid=company_ID, fid=funder_id, link_token=link_token, is_live_production_env=is_live_production_env)
