from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
import uuid
import datetime
from datetime import datetime, timedelta
import dwollav2
# from server import mongo_client, mongoDB_master_access, app
from project import db
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
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
import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.processor_token_create_request import ProcessorTokenCreateRequest
# from server import dwolla_app_token, plaid_client
from project.api.dwolla import dwolla_app_token
from project.api.plaid import plaid_client, merchant_plaid_pull


Secure_Account_Select_Blueprint = Blueprint('MCA_Secure_Account_Select', __name__)
@Secure_Account_Select_Blueprint.route("/api/merchant/plaid/secure_account_select/", methods=['GET', 'POST']) 
def MCA_Secure_Account_Select():




    print('Mongo DB---------------------------------------------->', file=sys.stderr)

    # secure_var = request.args.get('secure_var', None) # Dwolla Customer ID
    # dwolla_id = secure_var[:36]
    # company_ID = secure_var[39:]
    dwolla_id = request.args.get('did', None)
    company_ID = request.args.get('mid', None)
    funder_id = request.args.get('fid', None)
    #secure_id_plaid = secure_var[:106]
    print('Dwolla_ID --------------------------------------------------------------------------->', dwolla_id, file=sys.stderr)
    print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)

    funder_db_name = db.Master.Funders.find_one({'company_ID': funder_id})['funder_db_name']

    # all_DBs = set([item['DB_name'] for item in db.Master_Credentials.master_user_list.find()])

    # print('all_DBs ---------------------------------------------------> ', all_DBs , file=sys.stderr)


    # mongoDB_funder = ''
    # for DB_name in all_DBs:
    #     mongoDB_merch = db[DB_name]
    #     if mongoDB_merch.Company.find_one({ "company_ID": company_ID }):
    #         print('mongoDB_merch 2 ---------------------------------------------------> ', mongoDB_merch , file=sys.stderr)
    #         mongoDB_funder = mongoDB_merch
    #         break


    get_company = db[funder_db_name].Merchants.find_one({ "company_ID": company_ID })
    plaid_access_token = get_company["plaid_access_token"]
    business_ein = get_company["business_ein"]
    # cash_ads = get_company["cash_advance_contracts"]
    # len_of_cash = len(cash_ads)
    # cash_ad_var = "cash_advance_contracts." + str(len_of_cash - 1)
    contract_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, (company_ID + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))))

    print('plaid_access_token --------------------------------------------------->', plaid_access_token, file=sys.stderr)


    # Now that we are adding a list of funders to each merchant db this loop is probably unnessisary

    # get all plaid selected accounts from all merchants with maching EIN. Why?? We should just reference accounts that the just selected no?
    # all_account_ids = []
    # for DB_name in all_DBs:
    #     mongoDB_eins = db[DB_name]
    #     if mongoDB_eins.Merchants.find_one({ "business_ein": business_ein }):
    #         ein_company = mongoDB_eins.Merchants.find_one({ "business_ein": business_ein })
    #         for contract in ein_company['cash_advance_contracts']:
    #             all_account_ids.append(contract["selected_account_ID"])




    print('plaid_access_token plaid_access_token plaid_access_token ---------------------------------------------->', plaid_access_token, file=sys.stderr)

    account_list = []
    for ii in get_company["plaid_pull"][-1]["auth"]["accounts"]:
        print('ii ii ii ii ii ii ii ii ---------------------------------------------->', ii, file=sys.stderr)
        account_list.append([ii["name"], ii["official_name"], ii["account_id"]])


    print('ii ii ii ii ii ii ii ii ---------------------------------------------->', account_list, file=sys.stderr)




    if request.method == 'POST':

        # Steps:
        # 1. We know that customer has already been set up with dwolla from the secure register step so we just need to try to add
        # the account selected/funding source.
        # 2. If step 1 throws an error

        date_added = str(datetime.today().strftime('%m/%d/%Y'))

        form_data = request.form
        print('form_data form_data form_data ---------------------------------------------->', form_data, file=sys.stderr)

        selected_account = str(form_data['selected_account'])

        print('selected_account ---------------------------------------------->', selected_account, file=sys.stderr)

        # find if any selected_accounts from all merchants with maching EIN, if so get the existing dwolla funding url and skip the dwolla submit
        # skip_dwolla_submit = False
        # existing_dwolla_funding_source_url = '-'
        # for DB_name in all_DBs:
        #     mongoDB_eins = db[DB_name]
        #     if mongoDB_eins.Merchants.find_one({ "business_ein": business_ein }):
        #         ein_company = mongoDB_eins.Company.find_one({ "business_ein": business_ein })
        #         for contract in ein_company['cash_advance_contracts']:
        #             if contract["selected_account_ID"] == selected_account:
        #                 existing_dwolla_funding_source_url = contract["dwolla_funding_source_url"]
        #                 skip_dwolla_submit = True

        # Instead of looping through all merchants in all dbs why don't we just see if that account has been added to dwolla instead.
        # Since the account numbers cannot be retrieved through the API we could compare names? Or, just try to add it and handle the error.


        

        print('UPLOADING ---------------------------------------------->', file=sys.stderr)

        print('company_ID ---------------------------------------------->', company_ID, file=sys.stderr)
        print('date_added ---------------------------------------------->', date_added, file=sys.stderr)
        print('contract_ID ---------------------------------------------->', contract_ID, file=sys.stderr)
        # print('existing_dwolla_funding_source_url ---------------------------------------------->', existing_dwolla_funding_source_url, file=sys.stderr)
        print(selected_account)


        print('company_ID ---------------------------------------------->', company_ID, file=sys.stderr)


        print('skip_dwolla_submit ---------------------------------------------->', file=sys.stderr)

        # Create a processor token for a specific account id.
        create_request = ProcessorTokenCreateRequest(
            access_token=plaid_access_token,
            account_id=selected_account,
            processor='dwolla'
        )
        create_response = plaid_client.processor_token_create(create_request)
        processor_token = create_response['processor_token']

        print('processor_token ---->  ', processor_token , file=sys.stderr)


        # select_account_var = dwolla_id + '___' +  '___' + processor_token

        # print('select_account_var', select_account_var , file=sys.stderr)




        customer_url = current_app.config['DWOLLA_APP_URL'] + '/customers/' + dwolla_id
        print('ooo------------------------------------------------>', customer_url, file=sys.stderr)

        on_demand_authorization = dwolla_app_token.post('on-demand-authorizations')
        on_demand_authorization_accepted = on_demand_authorization.body['_links']['self']['href'] # => 'Agree & Continue'
        print('ooo------------------------------------------------>', on_demand_authorization, file=sys.stderr)
        print('ooo------------------------------------------------>', on_demand_authorization_accepted, file=sys.stderr)

        request_body = {
               "_links": {
                    "on-demand-authorization": {
                        "href": on_demand_authorization_accepted
                    }
                },
                'plaidToken': processor_token,
                'name': selected_account
            }


        print('0000========================================================>>>>>>>>>>>>>>>>>>', file=sys.stderr)

        dwolla_funding_source_url = None

        try:

            # Using dwollav2 - https://github.com/Dwolla/dwolla-v2-python (Recommended)
            #dwolla_funding_source_create = app_token.post('%s/funding-sources' % customer_url, request_body)
            try:
                customer = dwolla_app_token.post('%s/funding-sources' % customer_url, request_body)
                print('0011001100110011 ========================================================>>>>>>>>>>>>>>>>>>', file=sys.stderr)
            except:
                raise Exception("Could not add funding source.")
            try:
                dwolla_funding_source_url = customer.headers['location']
                print('dwolla_funding_source_url  ========================================================>>>>>>>>>>>>>>>>>>', dwolla_funding_source_url, file=sys.stderr)
                dwolla_funding_source_url = dwolla_funding_source_url.split('/')[-1]
                print('dwolla_funding_source_url  ========================================================>>>>>>>>>>>>>>>>>>', dwolla_funding_source_url, file=sys.stderr)
            except:
                raise Exception("Could not retrieve funding source URL.")
                
        except:
            # We get an error from dwolla because a account has already been set up. Let's find the dwolla source url in the funder dbs.
            all_DBs = list(db.Master.Funders.find({},{"funder_db_name":1}))
            for f_db in all_DBs:
                mongoDB_eins = db[f_db['funder_db_name']]
                if mongoDB_eins.Merchants.find_one({ "business_ein": business_ein }):
                    ein_company = mongoDB_eins.Merchants.find_one({ "business_ein": business_ein })
                    for contract in ein_company['cash_advance_contracts']:
                        if contract["selected_account_ID"] == selected_account:
                            dwolla_funding_source_url = contract["dwolla_funding_source_url"]

        print("DWOLLA FUNDING URL: " + dwolla_funding_source_url)

        if dwolla_funding_source_url is not None:

            db[funder_db_name].Merchants.update({ "company_ID": company_ID }, {"$push": {"cash_advance_contracts":{ "contract_ID": contract_ID, "status": "Prefund", "date_added":date_added, "start_date": "-", "expected_end_date": "-", "duration": "-", "split_percent": "-", "factor_rate": "-", "funded_via": "-", "fico_score": "-", "position": "-", "tags": "-", "advance_amount":"-", "pull_amount":"-", "expected_repayment_amount": "-", "day":"-", "total_amount_repaid":"-", "default_amount":"-", "percent_paid":"-", "bank_fee":"-", "commission": "-", "management_fee":"-", "ACH_pull_schedule": "", "pause_until":"None", "dwolla_funding_source_url": dwolla_funding_source_url, "selected_account_ID": selected_account, "syndicators":[], "signnow": [{"signnow_document_id": "", "signnow_status": "", "signnow_document_name": ""}]}}})

            #Remove Pre-Contract because added to Pre-Funded
            db[funder_db_name].Pre_Contract.delete_one({"company_ID": company_ID})

            return redirect(url_for('MCA_Merchant_Home.MCA_Merchant_Home'))

        else:
            raise Exception("Dwolla funding source could not be generated.")


    return render_template("/Merchant/Secure_Bank/Secure_Account_Select/secure_account_select.html", did=str(dwolla_id), mid=str(company_ID), fid=str(funder_id), account_list=account_list)
