import plaid
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.auth_get_request import AuthGetRequest
# from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.products import Products
from plaid.exceptions import ApiException
# from plaid.model.link_token_create_request import LinkTokenCreateRequest
# from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
# from plaid.model.country_code import CountryCode
from plaid.api import plaid_api
# from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
# from plaid.model.processor_token_create_request import ProcessorTokenCreateRequest
from flask import current_app, g
from werkzeug.local import LocalProxy
import datetime
from datetime import datetime, timedelta, date


def get_plaid_client():

    plaid_client = getattr(g, "_plaid_client", None)

    if plaid_client is None:
        host = plaid.Environment.Sandbox
        # Will need to add production and test plaid env to config file eventually

        # if app.config['ENV'] == 'production':
        #     # host = something else
        plaid_configuration = plaid.Configuration(
            host=host,
            api_key={
                'clientId': current_app.config['PLAID_CLIENT_ID'],
                'secret': current_app.config['PLAID_SECRET']
            }
        )
        plaid_api_client = plaid.ApiClient(plaid_configuration)
        plaid_client = g._plaid_client = plaid_api.PlaidApi(plaid_api_client)

    return plaid_client

plaid_client = LocalProxy(get_plaid_client)


def merchant_plaid_pull(plaid_access_token, db, company_ID, funder_db_name):

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


# Funder Plaid pull
def funder_plaid_pull(plaid_access_token, db, company_ID):

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


def format_plaid_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message': response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}