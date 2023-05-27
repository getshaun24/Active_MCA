from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db
import plaid
import plaid.api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from flask import request
from project.api.functions import pretty_print_response
from plaid.model.products import Products
from plaid.exceptions import ApiException
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from project.api.plaid import plaid_client, funder_plaid_pull, format_plaid_error
from flask_login import login_required
import datetime
from datetime import datetime, timedelta, date


Master_Plaid_Confirm_Blueprint = Blueprint('MCA_Master_Plaid_Confirm', __name__)
@Master_Plaid_Confirm_Blueprint.route("/api/master/master_plaid_confirm/", methods=['GET', 'POST']) # <- from '/'
def MCA_Master_Plaid_Confirm():

    is_live_production_env = False
    if current_app.config['ENV'] == 'production':
        is_live_production_env = True


    mongoDB = db.Master

    try:
        secure_id = request.args.get('secure_id', None) # Dwolla Customer ID
        # company_ID = secure_id[39:]
        company_ID = secure_id
        # Lets fetch the dwolla customer id from the db instead of exposing it in the url.
        # dwolla_id = secure_id[:36]
        # print(company_ID)
        dwolla_id = mongoDB.Funders.find_one({"company_ID": company_ID})["dwolla_customer_url_id"]
        
        print('secure_id --------------------------------------------------------------------------->', secure_id, file=sys.stderr)
        print('PLAID_IN_ID --------------------------------------------------------------------------->', dwolla_id, file=sys.stderr)
        print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)
    except:
        print('No Dwolla Id', file=sys.stderr)





    plaid_products = ['auth','transactions','identity'] #here b/c variable coming form ???
    # for product in PLAID_PRODUCTS:
    #         #plaid_products.append(Products(product))
    #     print('product --->', product)
    # print('plaid_products --->', plaid_products)


    response = plaid_client.link_token_create(
        {
        'user': {
            # This should correspond to a unique id for the current user.
            'client_user_id': 'user-id',
            },
        'client_name': "Plaid Quickstart",
        'products': plaid_products,
        'country_codes': current_app.config['PLAID_COUNTRY_CODES'],
        'language': "en"
        #'redirect_uri': PLAID_REDIRECT_URI,
        })

    # global link_token
    link_token = response['link_token']

    print('11------------------------------------------------>', link_token, file=sys.stderr)


    print('LINK TOKEN', link_token)



    #wrap all the following code in a 'try' because the included variables are not available until plaid returns them.
    #Need to skip this for initial page to load
    try:
        # trying both methods for redundancy
        try: #try getting web info with post
            xx_plaid1 = request.form
            print ('xx_plaid1: ', xx_plaid1)
            public_token = request.form['public_token']
            print ('public_token: ', public_token)
            dwolla_id = request.form['dwolla_id']
            company_ID = request.form['company_ID']
            print ('dwolla_id: ', dwolla_id, file=sys.stderr)
            print ('company_ID: ', company_ID, file=sys.stderr)
            try: #if plaid select account feature
                selected_account_id = request.form['metadata']['account']['id']
                selected_account_name = request.form['metadata']['account']['id']
                print ('selected_account_id: ', selected_account_id, file=sys.stderr)
                print ('selected_account_name: ', selected_account_name, file=sys.stderr)
            except:
                print('no account selection')
        except: #if post does not work the use Ajax
            ajax = request.get_json()
            print ('ajax: ', ajax)
            public_token = ajax['public_token']
            dwolla_id = ajax['dwolla_id']
            company_ID = ajax['company_ID']
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


        print('public_token: ', public_token)
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        print('exchange_request worked')
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        print('exchange_response worked')
        # access_token = response['access_token']
        # exchange_response = plaid_client.item_public_token_exchange(ItemPublicTokenExchangeRequest(public_token=public_token))
        print('exchange_response -->', exchange_response)

        #pretty_print_response(exchange_response.to_dict())
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']

        print('44------------------------------------------------>', file=sys.stderr)
        print('44------------------------------------------------>', file=sys.stderr)
        print ('access-token: ', access_token, file=sys.stderr)



        print('---------- company_id: ', company_ID)

        mongoDB.Funders.update({"company_ID": company_ID},{"$set": {"plaid_access_token": access_token}});

        print('Plaid token Added --------------------------------------------------------------------------->', file=sys.stderr)
        print('access_token --------------->', access_token, file=sys.stderr)
        print('company_id ----------------->', company_ID, file=sys.stderr)

        # funder_plaid_pull(plaid_access_token=access_token, mongo_client=db, company_ID=company_ID)





        plaid_access_token=access_token
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
        db.Master.Funders.update({"company_ID": company_ID},{"$push": {"plaid_pull": {"pull_date":'{:%Y-%m-%d}'.format(datetime.now()), "auth":auth_response, "identity":identity_response, "transactions":transactions_clean }}})

        print('Plaid Added --------------------------------------------------------------------------->', file=sys.stderr)



    except:
        print('No exchange', file=sys.stderr)





    return render_template("/Active_MCA_Master/Master_Plaid_Confirm/master_plaid_confirm.html", link_token=link_token, dwolla_id=dwolla_id, company_ID=company_ID, is_live_production_env=is_live_production_env)




































# Old Plaid

'''



    try:
      response = plaid_client.LinkToken.create(
        {
          'user': {
            # This should correspond to a unique id for the current user.
            'client_user_id': 'user-id',
          },
          'client_name': "Plaid Quickstart",
          'products': PLAID_PRODUCTS,
          'country_codes': PLAID_COUNTRY_CODES,
          'language': "en",
          'redirect_uri': PLAID_REDIRECT_URI,
        }
      )

      global link_token
      link_token = response['link_token']

      print('11------------------------------------------------>', link_token, file=sys.stderr)


      print('LINK TOKEN', link_token)
    except:
      print ('EXCEPTION')



    try:
        xx = request.get_json()
        print('22------------------------------------------------>', xx, file=sys.stderr)
        public_token = xx['public_token']
        dwolla_id = xx['dwolla_id']['dwolla_id']
        company_ID = xx['company_ID']['company_ID']
        print ('secured_id: ', dwolla_id, file=sys.stderr)
        print ('company_ID: ', company_ID, file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)
        print('33------------------------------------------------>', file=sys.stderr)



        try:
          exchange_response = plaid_client.Item.public_token.exchange(public_token)
        except plaid.errors.PlaidError as e:
          print('No exchange', file=sys.stderr)

        pretty_print_response(exchange_response)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']


        print('44------------------------------------------------>', file=sys.stderr)
        print('44------------------------------------------------>', file=sys.stderr)
        access_token = exchange_response['access_token']
        print ('access-token: ', access_token, file=sys.stderr)


        identity_response = plaid_client.Identity.get(access_token)
        pretty_print_response(identity_response)
        print('identity_response: ', identity_response["accounts"] , file=sys.stderr)

        print('66 66 66 66 66 66 66 6 6 6 6 6 6 6 ------------------------------------------------>', file=sys.stderr)
        print('66 66 66 66 66 66 66 6 6 6 6 6 6 6 ------------------------------------------------>', file=sys.stderr)

        identity_response_list = []
        for acc in identity_response["accounts"]:
            address_list = []
            email_list = []
            phone_list = []
            names_list = acc["owners"][0]["names"]
            for address in acc["owners"][0]["addresses"]:
                address_full = address["data"]["street"] + ' ' + address["data"]["city"] + ' ' + address["data"]["region"] + ' ' + address["data"]["country"] + ' ' + address["data"]["postal_code"]
                is_primary = address["primary"]
                address_list.append({"address":address_full, "is_primary":is_primary})
                print('address 2------------------------------------------------>', address, file=sys.stderr)
            for emails in acc["owners"][0]["emails"]:
                email = emails["data"]
                is_primary = emails["primary"]
                email_list.append({"email":email, "is_primary":is_primary})
                print('emails ------------------------------------------------>', emails, file=sys.stderr)
            for phone in acc["owners"][0]["phone_numbers"]:
                phone_num = phone["data"]
                is_primary = emails["primary"]
                phone_type = phone["type"]
                phone_list.append({"phone":phone_num, "is_primary":is_primary, "type":phone_type})
                print('phone 2------------------------------------------------>', phone, file=sys.stderr)

            new_dict = {"names":names_list, "address":address_list, "emails":email_list, "phones":phone_list }
            if new_dict not in identity_response_list:
                identity_response_list.append({"names":names_list, "address":address_list, "emails":email_list, "phones":phone_list })


        #identity_response_list_unique = [dict(t) for t in {tuple(d.items()) for d in identity_response_list}]
        #identity_response_list_unique = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in identity_response_list)]


        print('identity_response_list ------------------------------------------------>', identity_response_list, file=sys.stderr)



        print('77------------------------------------------------>', file=sys.stderr)
        print('77------------------------------------------------>', file=sys.stderr)



         # Retrieve real-time balance data for each of an Item's accounts
        #try:
        #    balance_response = plaid_client.Accounts.balance.get(access_token)
        #    pretty_print_response(balance_response)
        #    print(balance_response, file=sys.stderr)
        #except plaid.errors.PlaidError as e:
        #    print(jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } }), file=sys.stderr)

        print('88------------------------------------------------>', file=sys.stderr)
        print('88------------------------------------------------>', file=sys.stderr)

        # Retrieve an Item's accounts
        #try:
        #    accounts_response = plaid_client.Accounts.get(access_token)
        #    pretty_print_response(accounts_response)
        #    print(accounts_response, file=sys.stderr)
        #except plaid.errors.PlaidError as e:
        #    print(jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } }), file=sys.stderr)


        print('99------------------------------------------------>', file=sys.stderr)
        print('99------------------------------------------------>', file=sys.stderr)

        # Retrieve Transactions for an Item
        # Pull transactions for the last 30 days
        start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-731))
        end_date = '{:%Y-%m-%d}'.format(datetime.now())
        try:
            transactions_response = plaid_client.Transactions.get(access_token, start_date=start_date, end_date=end_date)
        #    pretty_print_response(transactions_response)
        #    print(transactions_response, file=sys.stderr)
        except plaid.errors.PlaidError as e:
            print(jsonify(format_error(e)), file=sys.stderr)

        transaction_list = []
        for acc in transactions_response["accounts"]:
            account_name = acc["name"]
            account_id = acc["account_id"]
            print('account_name ------------------------------------------------>', account_name, file=sys.stderr)
            for trans in transactions_response["transactions"]:
                if trans["account_id"] == account_id:
                    amount = trans["amount"]
                    date = trans["date"]
                    merchant_name = trans["merchant_name"]
                    pending = trans["pending"]
                    currency = trans["iso_currency_code"]
                    print('amount ------------------------------------------------>', amount, file=sys.stderr)
                    transaction_list.append({"account_name": account_name, "amount": amount, "date": date, "merchant_name":merchant_name, "pending":pending, "curreny":currency})


        print('transaction_list ------------------------------------------------>', transaction_list, file=sys.stderr)

        print('1010------------------------------------------------>', file=sys.stderr)
        print('1010------------------------------------------------>', file=sys.stderr)


        try:
            print('AUTH!')
            auth_response = plaid_client.Auth.get(AuthGetRequest(access_token=access_token))
            print(auth_response)
        #    print(auth_response, file=sys.stderr)

            auth_response_list = []
            for ach in auth_response["numbers"]["ach"]:
                routing = ach["routing"]
                wire_routing = ach["wire_routing"]
                for acc in auth_response["accounts"]:
                    account_name = acc["name"]
                    account_id = acc["account_id"]
                    official_name = acc["official_name"]
                    if account_id == ach["account_id"]:
                        auth_response_list.append({"account_name": account_name, "official_name":official_name, "account_id": account_id, "account_number": routing, "rounting_number": wire_routing})

            accounts_list = []
            if auth_response_list != 0:
                for acc in auth_response["accounts"]:
                    account_name = acc["name"]
                    available_balance = acc["balances"]["available"]
                    current_balance = acc["balances"]["current"]
                    currency = acc["balances"]["iso_currency_code"]
                    limit = acc["balances"]["limit"]
                    subtype= acc["subtype"]
                    account_id = acc["account_id"]
                    official_name = acc["official_name"]
                    accounts_list.append({"account_name":account_name, "account_id":account_id, "official_name":official_name, "subtype":subtype, "available_balance": available_balance, "current_balance": current_balance, "currency":currency, "limit":limit})

            print('accounts_list ----->', accounts_list)

        except:
            print('AUTH ERROR')


        print('1111------------------------------------------------>', file=sys.stderr)
        print('1111------------------------------------------------>', file=sys.stderr)

        # Retrieve investment holdings data for an Item
        # https://plaid.com/docs/#investments
        #try:
        #    holdings_response = plaid_client.Holdings.get(access_token)
        #    pretty_print_response(holdings_response)
        #    print(holdings_response, file=sys.stderr)
        #except plaid.errors.PlaidError as e:
        #    print(jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } }), file=sys.stderr)

        print('1212------------------------------------------------>', file=sys.stderr)
        print('1212------------------------------------------------>', file=sys.stderr)


        # Retrieve Investment Transactions for an Item
        # https://plaid.com/docs/#investments
        # Pull transactions for the last 30 days
        #start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-360))
        #end_date = '{:%Y-%m-%d}'.format(datetime.now())
        #try:
        #    investment_transactions_response = plaid_client.InvestmentTransactions.get(access_token, start_date, end_date)
        #    pretty_print_response(investment_transactions_response)
        #    print(investment_transactions_response, file=sys.stderr)
        #except plaid.errors.PlaidError as e:
        #    print(jsonify({'error': None, 'investment_transactions': investment_transactions_response}), file=sys.stderr)


        print('1313------------------------------------------------>', file=sys.stderr)
        print('1313------------------------------------------------>', file=sys.stderr)




        print('1414------------------------------------------------>', file=sys.stderr)
        print('1414------------------------------------------------>', file=sys.stderr)
        print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)
        print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)
        print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)

        mongoDB.Client_Funder.update({"company_ID": company_ID},{"$set": {"plaid_access_token": access_token}});

        mongoDB.Client_Funder.update({"company_ID": company_ID},{"$push": {"Plaid_Pull": {"Pull_date":'{:%Y-%m-%d}'.format(datetime.now()), "Auth":auth_response_list, "Identity":identity_response_list, "Accounts":accounts_list, "Transactions":transaction_list }}});


        print('Plaid Added --------------------------------------------------------------------------->', file=sys.stderr)


        print('11111========================================================>>>>>>>>>>>>>>>>>>', file=sys.stderr)




        print('1515------------------------------------------------>', file=sys.stderr)
        print('1515------------------------------------------------>', file=sys.stderr)

       #return redirect(url_for('MCA_Funder_Register', select_account_var=select_account_var))

    except:

        print('no accounts yet', file=sys.stderr)

'''
