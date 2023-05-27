from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
import uuid
import datetime
from datetime import datetime, timedelta
import dwollav2
import bcrypt
# from server import mongo_client, mongoDB_master_access
from project import db
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
import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.processor_token_create_request import ProcessorTokenCreateRequest
# from server import dwolla_app_token, plaid_client
from project.api.dwolla import dwolla_app_token
from project.api.plaid import plaid_client
from project.api.models import User
import flask_login


Account_Select_Blueprint = Blueprint('MCA_Account_Select', __name__)
@Account_Select_Blueprint.route('/api/master/account_select/', methods=['GET', 'POST']) # <- from '/'
def MCA_Account_Select():


    mongoDB_admin = db.Master
    

    print('Mongo DB---------------------------------------------->', file=sys.stderr)

    secure_var = request.args.get('secure_var', None) # Dwolla Customer ID
    # company_ID = secure_var[39:]
    company_ID = secure_var
    # print(company_ID)
    funder = mongoDB_admin.Funders.find_one({ "company_ID": company_ID })
    dwolla_id = funder["dwolla_customer_url_id"]
    # dwolla_id = secure_var[:36]
    
    #secure_id_plaid = secure_var[:106]
    print('Dwolla_ID --------------------------------------------------------------------------->', dwolla_id, file=sys.stderr)
    print('company_id --------------------------------------------------------------------------->', company_ID, file=sys.stderr)


    # db_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, (funder["poc_email"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")


    # legal_company_name_formatted = (funder["legal_company_name"]).replace(" ", "_").replace("'", "").replace("-", "_").replace("&", "_")
    # db_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, (legal_company_name_formatted + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
    DB_company_name = funder["funder_db_name"]
    poc_email = funder["poc_email"]
    first_name = funder["poc_first_name"]
    last_name = funder["poc_last_name"]
    plaid_access_token = funder["plaid_access_token"]

    print('plaid_access_token plaid_access_token plaid_access_token ---------------------------------------------->', plaid_access_token, file=sys.stderr)

    

    count = 0
    account_list = []
    for ii in funder["plaid_pull"][-1]["auth"]["accounts"]:
        print('ii ii ii ii ii ii ii ii ---------------------------------------------->', ii["name"], file=sys.stderr)
        account_list.append([ii["name"], ii["official_name"], ii["account_id"]])
        count += 1


    print('ii ii ii ii ii ii ii ii ---------------------------------------------->', account_list, file=sys.stderr)




    if request.method == 'POST':


        form_data = request.form
        print('form_data form_data form_data ---------------------------------------------->', form_data, file=sys.stderr)
        form_accounts = set([form_data['active_pull'], form_data['merchant_pull']]) #get accounts and remove duplicates - if account is already in dwolla, dont add again
        print(form_accounts)

        for elm in form_accounts:
            print('elm elm elm elm ---------------------------------------------->', elm, file=sys.stderr)


            print('55------------------------------------------------>', file=sys.stderr)

            # Create a processor token for a specific account id.
            create_request = ProcessorTokenCreateRequest(
                access_token=plaid_access_token,
                account_id=elm,
                processor='dwolla'
            )
            create_response = plaid_client.processor_token_create(create_request)
            processor_token = create_response['processor_token']

            print('processor_token ---->  ', processor_token , file=sys.stderr)



            select_account_var = dwolla_id + '___' +  '___' + processor_token

            print('select_account_var', select_account_var , file=sys.stderr)



            customer_url = current_app.config['DWOLLA_APP_URL'] + '/customers/' + dwolla_id
            # customer_url = 'https://api-sandbox.dwolla.com/customers/' + dwolla_id
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
                'name': elm
            }       


            print('0000========================================================>>>>>>>>>>>>>>>>>>', file=sys.stderr)

            # Using dwollav2 - https://github.com/Dwolla/dwolla-v2-python (Recommended)

            customer = dwolla_app_token.post('%s/funding-sources' % customer_url, request_body)
            print('0011001100110011 ========================================================>>>>>>>>>>>>>>>>>>', file=sys.stderr)
            dwolla_funding_source_url = customer.headers['location']
            dwolla_funding_source_url = dwolla_funding_source_url.split('/')[-1]

            # dwolla_funding_source_url = dwolla_funding_source_url[47:]


            print('11111========================================================>>>>>>>>>>>>>>>>>>', file=sys.stderr)

            hashed_password = bcrypt.hashpw(poc_email.encode('utf8'), bcrypt.gensalt(14))
            db.Credentials.Users.insert_one({"email": poc_email, "first_name": first_name, "last_name": last_name, "password": hashed_password, "access_status": 'admin', "two_factor_code": "", "reset_code": "", "notification_count": 0, "notifications": [], "business_id": company_ID, "metadata": {"funder_db": DB_company_name}})
                

            if form_data['active_pull'] == form_data['merchant_pull']:
                mongoDB_admin.Funders.update({ "company_ID": company_ID }, {"$set": {
                    "dwolla_funding_source_destination_account": dwolla_funding_source_url, 
                    "dwolla_funding_source_active_pay_account": dwolla_funding_source_url, 
                    "selected_active_pay_account_ID": elm,
                    "selected_account_ID": elm
                }});
                break
            else:
                if elm == form_data['merchant_pull']:
                    mongoDB_admin.Funders.update({ "company_ID": company_ID }, {"$set": {"dwolla_funding_source_destination_account": dwolla_funding_source_url, "selected_account_ID": elm}});
                else:
                    mongoDB_admin.Funders.update({ "company_ID": company_ID }, {"$set": {"dwolla_funding_source_active_pay_account": dwolla_funding_source_url, "selected_active_pay_account_ID": elm}});




        # new_mongodb = db[DB_company_name]  # you can also use dot notation client.mydatabase
        # All users are now in Credentials.Users
        # new_mongodb.Users.insert_one({"access_status": "admin", "first_name": first_name, "last_name": last_name, "email": poc_email, "password": hashed_password, "notification_count": 0})
        # print('inserted---------------------------------------------->', file=sys.stderr)

        user = User(email=poc_email, db=db)
        session["email"] = user.email
        session["user_database"] = user.funder_db
        session["access_status"] = user.access_status
        session["first_name"] = user.first_name
        session["last_name"] = user.last_name
        session["notification_count"] = user.notification_count
        session["business_id"] = company_ID
        flask_login.login_user(user)

        return redirect(url_for('MCA_Funder_Home.MCA_Funder_Home'))





    return render_template("/Active_MCA_Master/Account_Select/account_select.html", secure_var=secure_var, account_list=account_list)
