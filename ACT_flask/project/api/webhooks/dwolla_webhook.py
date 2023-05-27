from flask import Blueprint, url_for, request, redirect, render_template
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access, dwolla_app_token
from project.api.dwolla import dwolla_app_token
from project.api.mongo import db
from project.api.functions import transfer_failure_retrieve
import datetime
from datetime import datetime, timedelta


dwolla_webhook_Blueprint = Blueprint('dwolla_webhook', __name__)
@dwolla_webhook_Blueprint.route("/api/webhooks/dwolla_webhook/", methods=['GET', 'POST']) 
def dwolla_webhook():


    customers_list = ['customer_created', 'customer_kba_verification_needed', 'customer_kba_verification_failed', 'customer_kba_verification_passed', 'customer_verification_document_needed', 'customer_verification_document_uploaded', 'customer_verification_document_failed', 'customer_verification_document_approved', 'customer_reverification_needed', 'customer_verified', 'customer_suspended', 'customer_activated', 'customer_deactivated']
    beneficial_owner_list = ['customer_beneficial_owner_created', 'customer_beneficial_owner_removed', 'customer_beneficial_owner_verification_document_needed', 'customer_beneficial_owner_verification_document_uploaded', 'customer_beneficial_owner_verification_document_failed', 'customer_beneficial_owner_verification_document_approved', 'customer_beneficial_owner_reverification_needed', 'customer_beneficial_owner_verified']
    funding_source_list = ['customer_funding_source_added', 'customer_funding_source_removed', 'customer_funding_source_verified', 'customer_funding_source_unverified', 'customer_funding_source_negative', 'customer_funding_source_updated']
    transfer_list = ['customer_transfer_created', 'customer_transfer_cancelled', 'customer_transfer_failed', 'customer_transfer_completed']
    transfer_bank_list = ['customer_bank_transfer_created', 'customer_bank_transfer_creation_failed', 'customer_bank_transfer_cancelled', 'customer_bank_transfer_failed', 'customer_bank_transfer_completed']
    all_list = ['customer_created', 'customer_kba_verification_needed', 'customer_kba_verification_failed', 'customer_kba_verification_passed', 'customer_verification_document_needed', 'customer_verification_document_uploaded', 'customer_verification_document_failed', 'customer_verification_document_approved', 'customer_reverification_needed', 'customer_verified', 'customer_suspended', 'customer_activated', 'customer_deactivated', 'customer_beneficial_owner_created', 'customer_beneficial_owner_removed', 'customer_beneficial_owner_verification_document_needed', 'customer_beneficial_owner_verification_document_uploaded', 'customer_beneficial_owner_verification_document_failed', 'customer_beneficial_owner_verification_document_approved', 'customer_beneficial_owner_reverification_needed', 'customer_beneficial_owner_verified', 'customer_funding_source_added', 'customer_funding_source_removed', 'customer_funding_source_verified', 'customer_funding_source_unverified', 'customer_funding_source_negative', 'customer_funding_source_updated', 'customer_transfer_created', 'customer_transfer_cancelled', 'customer_transfer_failed', 'customer_transfer_completed', 'customer_bank_transfer_created', 'customer_bank_transfer_creation_failed', 'customer_bank_transfer_cancelled', 'customer_bank_transfer_failed', 'customer_bank_transfer_completed']


    webhooks = request.json

    #time.sleep(8)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    print(webhooks, file=sys.stderr)
    print('HOOKS ----------------------------------------- >', file=sys.stderr)
    #time.sleep(8)


    timestamp = datetime.strptime(webhooks['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%m/%d/%y %H:%M:%S')
    topic = webhooks['topic']
    transfer_id = webhooks['resourceId']
    eventurl = webhooks['_links']['self']['href']
    customer_url = webhooks['_links']['customer']['href']
    account_url = webhooks['_links']['account']['href']
    #customer_url_id = customer_url[41:]
    #account_url_id = customer_url[41:]
    customer_url_id = customer_url.replace('https://api-sandbox.dwolla.com/customers/', '')
    account_url_id = account_url.replace('https://api-sandbox.dwolla.com/accounts/', '')
    customer = dwolla_app_token.get(webhooks['_links']['customer']['href'])
    legal_company_name = customer.body['businessName']



    #list of all Dwolla events related to transactrions
    if topic in transfer_list or topic in transfer_bank_list:
        transfer_url = webhooks['_links']['resource']['href']
        transfer_info_get = dwolla_app_token.get(transfer_url)
        transfer_info = transfer_info_get.body['_links']
        print('transfer_info ----------------------------------------- >', transfer_info, file=sys.stderr)
        try:
            destination_funding_source_url = transfer_info_get.body['_links']['destination-funding-source']['href']
            destination_funding_source = destination_funding_source_url[-36:]
        except:
            destination_funding_source = 'None'
        try:
            source_funding_source_url = transfer_info_get.body['_links']['source-funding-source']['href']
            source_funding_source = source_funding_source_url[-36:]
        except:
            source_funding_source = 'None'
        #print('transfer_info ----------------------------------------- >', transfer_info, file=sys.stderr)
        print('destination_funding_source ----------------------------------------- >', destination_funding_source, file=sys.stderr)
        print('source_funding_source ----------------------------------------- >', source_funding_source, file=sys.stderr)
    else:
        destination_funding_source = 'None'
        source_funding_source = 'None'
    print('customer ----------------------------------------- >', customer_url, file=sys.stderr)
    print('customer_url_id ----------------------------------------- >', customer_url_id, file=sys.stderr)
    print('account_url_id ----------------------------------------- >', account_url_id, file=sys.stderr)
    print('legal_company_name ----------------------------------------- >', legal_company_name, file=sys.stderr)
    print('TOPIC ----------------------------------------- >', topic, file=sys.stderr)
    print('eventurl ----------------------------------------- >', eventurl, file=sys.stderr)




    # Get merchnt DB and match customer url to merchant
    merchant_mongoDB = db.Merchant_Users
    merchant = merchant_mongoDB.merchant_users.find_one({"dwolla_id": customer_url_id})
    #if customer_url_id is a merchant:
    if merchant:

        print('Is Merchant ----------------------------------------- >', file=sys.stderr)

        # get more info regarding a transfer and add to DB
        if topic in transfer_list or topic in transfer_bank_list:
            transfer_failure_code, failure_reason, transfer_status = transfer_failure_retrieve(transfer_url)

            if failure_reason != "None":
                merchant_mongoDB.merchant_users.update({"dwolla_id": customer_url_id}, {"$push": {"Notifications": {"timestamp": timestamp, "topic": failure_reason, "transfer_id":transfer_id, "eventurl":eventurl }}});
            else:
                merchant_mongoDB.merchant_users.update({"dwolla_id": customer_url_id}, {"$push": {"Notifications": {"timestamp": timestamp, "topic": topic, "transfer_id":transfer_id, "eventurl":eventurl }}});

        # add any other notifications to DB
        if topic in customers_list or topic in beneficial_owner_list or topic in funding_source_list:
            merchant_mongoDB.merchant_users.update({"dwolla_id": customer_url_id}, {"$push": {"Notifications": {"timestamp": timestamp, "topic": topic, "transfer_id":"N/A", "eventurl":eventurl }}});


        notification_count = merchant["notification_count"]
        new_count = notification_count + 1
        merchant_mongoDB.merchant_users.update({"dwolla_id": customer_url_id}, {"$set": {"notification_count": new_count}});





    mongoDB_admin = db.Active_MCA_Admin
    funders = set([item['dwolla_customer_url_id'] for item in mongoDB_admin.Client_Funder.find()])

    all_DBs = set([item['DB_name'] for item in db.Master_Credentials.master_user_list.find()])

    all_dwolla_destination_accounts = []
    for item in db.Master_Credentials.master_user_list.find():
        try:
            all_dwolla_destination_accounts.append(item['dwolla_funding_source_destination_account'])
        except:
            continue

    all_dwolla_destination_accounts = set(all_dwolla_destination_accounts)

    #all_dwolla_destination_accounts = set([item['dwolla_funding_source_destination_account'] for item in db.Master_Credentials.master_user_list.find()])


    print('all_DBs ----------------------------------------- >', all_DBs, file=sys.stderr)
    print('all_dwolla_destination_accounts ----------------------------------------- >', all_dwolla_destination_accounts, file=sys.stderr)
    print('funders ----------------------------------------- >', funders, file=sys.stderr)



    for DB_name in all_DBs:
        print('DB ----------------------------------------- >', DB_name, file=sys.stderr)
        mongoDB = db[DB_name]


        company = mongoDB.Company.find_one({ "dwolla_customer_url_id": customer_url_id })
        if not company:
            print('no company ----------------------------------------- >', DB_name, file=sys.stderr)
            continue
            print('no company ----------------------------------------- >', DB_name, file=sys.stderr)

        print(' dest_account 1 ------------------------------------------------------------------------------->', file=sys.stderr)

        # find the right client account using the destination id to send the notifications to
        if destination_funding_source != 'None':
            for dest_account in all_dwolla_destination_accounts:
                print(' dest_account 1 ------------------------------------------------------------------------------->', dest_account, file=sys.stderr)
                print(' destination_funding_source 1 ------------------------------------------------------------------------------->', destination_funding_source, file=sys.stderr)
                print(' source_funding_source 1 ------------------------------------------------------------------------------->', source_funding_source, file=sys.stderr)
                if dest_account == destination_funding_source or dest_account == source_funding_source:
                    print(' dest_account EQUALS ------------------------------------------------------------------------------->', dest_account, file=sys.stderr)
                    if customer_url_id in funders:
                        print(' BREAKING ------------------------------------------------------------------------------->', customer_url_id, file=sys.stderr)
                        break
                    else:

                        webhook_date = datetime.today().strftime('%Y-%m-%d')

                        contract_count = 0
                        for contract in company['Cash_Advance_Contracts']:
                            print(' contract status ----------------------------------------------------------------->', contract['status'], file=sys.stderr)
                            if contract['status'] == 'Open' or contract['status'] == 'Collections' or contract['status'] == 'Legal' or contract['status'] == 'Prefund':
                                transaction_count = 0
                                for trans in contract['Transaction_track']:
                                    if trans['transaction_ID'] == transfer_id:

                                        company_ID = company['company_ID']
                                        status = contract['status']
                                        advance_amount = contract['advance_amount']
                                        pull_amount = contract['pull_amount']
                                        expected_repayment_amount = contract['expected_repayment_amount']
                                        percent_paid = contract['percent_paid']
                                        syndicators = contract['Syndicators'][0]
                                        transaction_amount = trans['transaction_amount']
                                        default_amount = contract['default_amount']
                                        total_amount_repaid = contract['total_amount_repaid']


                                        '''
                                        # Get the amounts in the previous transaction rather than the global amount so as to account for dwolla processing transactions at differents speeds
                                        if transaction_count > 1:
                                            ii = 1
                                            while ii < transaction_count:
                                                print('WHILE', contract['Transaction_track'][transaction_count - ii]['status'], file=sys.stderr)
                                                if contract['Transaction_track'][transaction_count - ii]['status'] == "processed":
                                                    print('WHILE 2', file=sys.stderr)
                                                    total_amount_repaid = contract['Transaction_track'][transaction_count - ii]['total_amount_repaid']
                                                    default_amount = contract['Transaction_track'][transaction_count - ii]['default_amount']
                                                    print('total_amount_repaid', total_amount_repaid, file=sys.stderr)
                                                    print('default_amount', default_amount, file=sys.stderr)
                                                    break
                                                else:
                                                    print('WHILE 1', file=sys.stderr)
                                                    ii += 1
                                        else:
                                            default_amount = contract['default_amount']
                                            total_amount_repaid = contract['total_amount_repaid']
                                        '''

                                        total_amount_repaid = round(float(total_amount_repaid) + transaction_amount, 2)
                                        percent_paid = round(total_amount_repaid / float(expected_repayment_amount) * 100, 2)

                                        if status == "Defaulted":
                                            default_amount = round(float(default_amount) - transaction_amount, 2)


                                        transfer_failure_code, failure_reason, transfer_status = transfer_failure_retrieve(transfer_url)

                                        #if topic == "customer_bank_transfer_created" or topic == "customer_transfer_created" or topic == "customer_bank_transfer_completed" or topic == "customer_transfer_completed":
                                        if False:
                                            print('Transfer Created', file=sys.stderr)
                                        else:
                                            for user in mongoDB.Users.find():
                                                if user["access_status"] == 'admin':
                                                    email = user["email"]
                                                    notification_count = user["notification_count"]
                                                    new_count = notification_count + 1
                                                    mongoDB.Users.update({"email": email}, {"$set": {"notification_count": new_count}});
                                                    print('Transfer 000000000000 ======= 000000000000 ========== 000000000000', file=sys.stderr)

                                                    if failure_reason != "None":
                                                        mongoDB.Notifications.insert_one({"timestamp": timestamp, "legal_company_name": legal_company_name, "topic": failure_reason, "transfer_id":transfer_id, "eventurl":eventurl })
                                                    else:
                                                        mongoDB.Notifications.insert_one({"timestamp": timestamp, "legal_company_name": legal_company_name, "topic": topic, "transfer_id":transfer_id, "eventurl":eventurl })
                                                    print('Transfer Created, Notifications Updated', file=sys.stderr)


                                        for key, val in syndicators.items():
                                            synd_collection = mongoDB.Syndicators.find_one({ "syndicator_business_name": key })
                                            syndicated_percent = float(val) / float(advance_amount)
                                            rev_amount = round(float(synd_collection['revenue']) + (float(total_amount_repaid) * syndicated_percent),2)
                                            mongoDB.Syndicators.update({ "syndicator_business_name": key }, {"$set": {'revenue': rev_amount}});

                                        transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track." + str(transaction_count)
                                        contract_var_repaid = "Cash_Advance_Contracts." + str(contract_count) + ".total_amount_repaid"
                                        contract_var_default_repaid = "Cash_Advance_Contracts." + str(contract_count) + ".default_amount"
                                        contract_var_percent = "Cash_Advance_Contracts." + str(contract_count) + ".percent_paid"
                                        contract_var_status = "Cash_Advance_Contracts." + str(contract_count) + ".status"

                                        if topic == "customer_bank_transfer_completed" or topic == "customer_transfer_completed":
                                            if trans['note'] == "First Payment Deposit":
                                                mongoDB.Company.update({"company_ID": company['company_ID']}, {"$set": {transaction_var: {"transaction_num":trans['transaction_num'], "transaction_date":trans['transaction_date'], "transaction_confirmed_date":webhook_date, "transaction_amount":transaction_amount, "default_amount":default_amount, "total_amount_repaid":0, "percent_paid":0, "note":trans['note'], "transaction_ID":trans['transaction_ID'], "status":transfer_status, "error":transfer_failure_code}}});
                                                print('transaction updated', file=sys.stderr)
                                            else:
                                                if total_amount_repaid >= expected_repayment_amount:
                                                    mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_repaid: total_amount_repaid, contract_var_percent: percent_paid, contract_var_default_repaid:default_amount, contract_var_status:"Closed" }});
                                                else:
                                                    mongoDB.Company.update({"company_ID": company_ID},{"$set": {contract_var_repaid: total_amount_repaid, contract_var_percent: percent_paid, contract_var_default_repaid:default_amount }});

                                                mongoDB.Company.update({"company_ID": company['company_ID']}, {"$set": {transaction_var: {"transaction_num":trans['transaction_num'], "transaction_date":trans['transaction_date'], "transaction_confirmed_date":webhook_date, "transaction_amount":transaction_amount, "default_amount":default_amount, "total_amount_repaid":total_amount_repaid, "percent_paid":percent_paid, "note":trans['note'], "transaction_ID":trans['transaction_ID'], "status":transfer_status, "error":transfer_failure_code}}});
                                                print('transaction updated 1', file=sys.stderr)

                                        elif topic == "customer_bank_transfer_created" or topic == "customer_transfer_created":
                                            print('do nothing', file=sys.stderr)

                                        else:
                                            mongoDB.Company.update({"company_ID": company['company_ID']}, {"$set": {transaction_var: {"transaction_num":trans['transaction_num'], "transaction_date":trans['transaction_date'], "transaction_confirmed_date":"Failure", "transaction_amount":transaction_amount, "default_amount":default_amount, "total_amount_repaid":total_amount_repaid, "percent_paid":percent_paid, "note":trans['note'], "transaction_ID":trans['transaction_ID'], "status":transfer_status, "error":transfer_failure_code}}});
                                            print('transaction updated 2', file=sys.stderr)
                                            break
                                    else:
                                        transaction_count += 1
                                contract_count += 1
                            break

                            print('destination loop succcess ----------------------------------------- >', file=sys.stderr)

        else:
            # If the webhook was not a transaction (has no destination account) then find all the Funders with the merchant and continue if the contract is active
            print('0000000000000000000000000001111111111111111122222222222222222333333333333333 ----------------------------------------- >', file=sys.stderr)
            for comp in mongoDB.Company.find():
                for contract in comp['Cash_Advance_Contracts']:
                    print(' contract status ----------------------------------------------------------------->', contract['status'], file=sys.stderr)
                    if contract['status'] == 'Open' or contract['status'] == 'Collections' or contract['status'] == 'Legal' or contract['status'] == 'Prefund':
                        if topic in transfer_list or topic in transfer_bank_list:
                            print('Transfer', file=sys.stderr)
                        else:
                            for user in mongoDB.Users.find():
                                if user["access_status"] == 'admin':
                                    email = user["email"]
                                    notification_count = user["notification_count"]
                                    new_count = notification_count + 1
                                    mongoDB.Users.update({"email": email}, {"$set": {"notification_count": new_count}});

                                    print('444444444444444555555555555555566666666666666666666 ----------------------------------------- >', file=sys.stderr)


                                    mongoDB.Notifications.insert_one({"timestamp": timestamp, "legal_company_name": legal_company_name, "topic": topic, "transfer_id":transfer_id, "eventurl":eventurl })

    print('SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_SUCCESS_ ----------------------------------------- >', file=sys.stderr)


    return "Success", 200
