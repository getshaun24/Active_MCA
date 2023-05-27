# -*- coding: utf-8 -*-


from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from datetime import datetime, timedelta
import dwollav2
import pymongo
import plaid
import random


app = Flask(__name__, template_folder="")





DWOLLA_APP_KEY = os.getenv('DWOLLA_APP_KEY')
DWOLLA_APP_SECRET = os.getenv('DWOLLA_APP_SECRET')



# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
# PLAID_PRODUCTS is a comma-separated list of products to use when initializing
# Link. Note that this list must contain 'assets' in order for the app to be
# able to create and retrieve asset reports.
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions, auth, identity').split(',')

# PLAID_COUNTRY_CODES is a comma-separated list of countries for which users
# will be able to select institutions from.
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')


def empty_to_none(field):
  value = os.getenv(field)
  if value is None or len(value) == 0:
    return None
  return value


# Parameters used for the OAuth redirect Link flow.
#
# Set PLAID_REDIRECT_URI to 'http://localhost:3000/'
# The OAuth redirect flow requires an endpoint on the developer's website
# that the bank website should redirect to. You will need to configure
# this redirect URI for your client ID through the Plaid developer dashboard
# at https://dashboard.plaid.com/team/api.
PLAID_REDIRECT_URI = empty_to_none('PLAID_REDIRECT_URI')

plaid_client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      environment=PLAID_ENV,
                      api_version='2019-05-29')






mongo_client = pymongo.MongoClient("mongodb+srv://Gr33nworldwid31:Gr33nworldwid31@activemca-1.ugg7j.mongodb.net")
mongoDB_master_access = mongo_client.Master_Credentials

all_DBs = set([item['DB_name'] for item in mongoDB_master_access.master_user_list.find()])



client = dwollav2.Client(key = DWOLLA_APP_KEY, secret = DWOLLA_APP_SECRET, environment = 'sandbox') # optional - defaults to production

app_token = client.Auth.client()

day_of_week = datetime.today().weekday()
today_date = datetime.today().strftime('%Y-%m-%d')

bank_holidays_2022 = ['2022-01-01', '2022-01-17', '2022-02-21', '2022-05-30', '2022-06-19', '2022-07-04', '2022-09-05', '2022-10-10', '2022-11-11', '2022-11-24', '2022-11-23', '2022-12-25']
#bank_holidays = [datetime.strptime(t, '%Y-%m-%d') for t in bank_holidays_2022]

if day_of_week == 0:
    day_of_week_str = 'weekly_mon'
if day_of_week == 1:
    day_of_week_str = 'weekly_tues'
if day_of_week == 2:
    day_of_week_str = 'weekly_wed'
if day_of_week == 3:
    day_of_week_str = 'weekly_thurs'
if day_of_week == 4:
    day_of_week_str = 'weekly_fri'

print('today_date -------------------------------->', today_date)
print('ACH First Test -------------------------------->')

if today_date not in bank_holidays_2022:
    if day_of_week in [0,1,2,3,4]:
        for DB_name in all_DBs:
            print('DB_name -------------------------------->', DB_name)
            mongo_master = mongoDB_master_access.master_user_list.find_one({ "DB_name": DB_name })
            dwolla_funding_source_destination_account = "https://api-sandbox.dwolla.com/funding-sources/" + mongo_master["dwolla_funding_source_destination_account"]
            mongoDB = eval("mongo_client." + DB_name)
            for xx in mongoDB.Company.find():
                for k1 in xx['Cash_Advance_Contracts']:
                    print('11111 -------------------------------->')
                    if k1['status'] == 'Open' or k1['status'] == 'Defaulted':
                        print('222 -------------------------------->')
                        if k1['pause_until'] == "None" or k1['pause_until'] > today_date:
                            print('4444 -------------------------------->')
                            if k1['ACH_pull_schedule'] == day_of_week_str or k1['ACH_pull_schedule'] == "weekdays":
                                print('5555 -------------------------------->')
                                company_ID = xx['company_ID']
                                company_DBA = xx['company_DBA']
                                access_token = xx['plaid_access_token']
                                dwolla_customer_url_id = xx['dwolla_customer_url_id']
                                contract_ID = k1['contract_ID']
                                expected_repayment_amount = k1['expected_repayment_amount']
                                syndicators = k1['Syndicators']
                                ACH_pull_sched = k1['ACH_pull_schedule']
                                advance_amount = float(k1['advance_amount'])
                                status = k1['status']
                                total_amount_repaid = float(k1['total_amount_repaid'])
                                default_amount = float(k1['default_amount'])
                                percent_paid = float(k1['percent_paid'])
                                pull_amount = float(k1['pull_amount'])
                                selected_account_id = k1['selected_account_ID']
                                transaction_table = k1['Transaction_track']

                                contract_count = 0
                                for ii in mongoDB.Company.find({"company_ID": company_ID}):
                                    for contract in ii['Cash_Advance_Contracts']:
                                        if contract['contract_ID'] == contract_ID:
                                            break
                                        else:
                                            contract_count += 1

                                print('contract_count: ', contract_count)

                                transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track"

                                print('66666 -------------------------------->', company_DBA)
                                #try:
                                payback_table_results = []
                                for transaction in transaction_table:
                                    payback_table_results.append([transaction['transaction_num'], transaction['transaction_date'], transaction['transaction_confirmed_date'], transaction['transaction_amount'], transaction['total_amount_repaid'], transaction['percent_paid'], transaction['note'], transaction['transaction_ID'], transaction['status'], transaction['error']])
                                #except:
                                #    payback_table_results = []


                                #try:
                                payback_latest_row = payback_table_results[-1]
                                payment_num = int(payback_latest_row[0]) + 1
                                #except:
                                #    payment_num = 1



                                #Retrieve real-time balance data for each of an Item's accounts
                                balance_response = plaid_client.Accounts.balance.get(access_token)

                                print('77777 -------------------------------->')

                                for acc in balance_response['accounts']:
                                    print('77777___0000 -------------------------------->', acc['account_id'])
                                    print('77777___0_1 -------------------------------->', selected_account_id)
                                    if acc['account_id'] == selected_account_id:

                                        print('77777___11111 -------------------------------->')

                                        #if pull_amount > float(acc['balances']['available']):
                                        rand_int = int(random.uniform(1, 1000))
                                        if pull_amount > float(acc['balances']['available'] * rand_int):
                                            print(acc['balances']['available'])
                                            print('Insufficient Funds !')

                                            mongoDB.Company.update_one({"company_ID": company_ID}, {"$push": {transaction_var: { "transaction_num": payment_num, "transaction_date": today_date, "transaction_confirmed_date":"Failed", "transaction_amount":pull_amount, "total_amount_repaid":total_amount_repaid, "default_amount":default_amount, "percent_paid":percent_paid, "note":"Insufficient Funds", "transaction_ID":"None - Transaction Intercepted", "status":"Paused", "error":"Insufficient Funds"}}});


                                        else:

                                            print('77777___22222 -------------------------------->')

                                            full_dwolla_customer_url = "https://api-sandbox.dwolla.com/customers/" + dwolla_customer_url_id
                                            funding_sources = app_token.get('%s/funding-sources' % full_dwolla_customer_url)
                                            fs_id = funding_sources.body['_embedded']['funding-sources'][0]['id']
                                            print(fs_id)

                                            print('77777___3333 -------------------------------->')

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
                                                            'value': pull_amount
                                                            },
                                                        'clearing': {
                                                            'destination': 'next-available'
                                                            }
                                                        }


                                            print(request_body)


                                            if True:
                                                transfer = app_token.post('transfers', request_body)
                                                print('TRANSFER SUCCESSS -- > ', transfer)
                                                transfer_url = transfer.headers['location']
                                                print('TRANSFER URL -- > ', transfer_url)
                                                transfer_id = transfer_url[41:]

                                                print('TRANSFER url -------------------------------->', transfer_url)
                                                print('TRANSFER ID -------------------------------->', transfer_id)

                                                transfer_retrieve = app_token.get(transfer_url)
                                                transfer_status = transfer_retrieve.body['status']

                                                try:
                                                    get_transfer_failure_status = app_token.get('%s/failure' % transfer_url)
                                                    transfer_failure_reason = get_transfer_failure_status.body['code']
                                                    if transfer_failure_reason == 'R01':
                                                        failure_reason = "Insufficient Funds. Available balance is not sufficient to cover the dollar value of the debit entry."
                                                    elif transfer_failure_reason == 'R02':
                                                        failure_reason = "Bank Account Closed. Previously active account has been closed."
                                                    elif transfer_failure_reason == 'R03':
                                                        failure_reason = "No Account/Unable to Locate Account. Account number structure is valid, but doesn’t match individual identified in entry or is not an open account."
                                                    elif transfer_failure_reason == 'R04':
                                                        failure_reason = "Invalid Bank Account Number Structure. Account number structure is not valid."
                                                    elif transfer_failure_reason == 'R05':
                                                        failure_reason = "Unauthorized debit to consumer account. A debit entry was transmitted to a consumer account that was not authorized by the Receiver. Written Statement is required."
                                                    elif transfer_failure_reason == 'R06':
                                                        failure_reason = "Returned per ODFI’s request. The ODFI has requested that the RDFI return the ACH entry as an erroneous entry. If the RDFI agrees to return the entry, the ODFI must indemnify the RDFI in accordance with guidelines."
                                                    elif transfer_failure_reason == 'R07':
                                                        failure_reason = "Authorization revoked by customer. The receiver who previously authorized an entry has revoked authorization with the originator for this debit entry."
                                                    elif transfer_failure_reason == 'R08':
                                                        failure_reason = "Payment stopped. The Receiver has placed a stop payment order on this debit entry, which may be placed on one or more debit entries."
                                                    elif transfer_failure_reason == 'R09':
                                                        failure_reason = "Uncollected funds. A sufficient book or ledger balance exists to satisfy the dollar value of the transaction  (i.e., uncollected checks), but the available balance is below the dollar value of the debit entry."
                                                    elif transfer_failure_reason == 'R10':
                                                        failure_reason = "Customer advises unauthorized, improper,  ineligible, or part of an incomplete transaction. The RDFI has been notified by the receiver (ie. customer that the entry is unauthorized, improper or ineligible)."
                                                    elif transfer_failure_reason == 'R11':
                                                        failure_reason = "Check truncation entry return. To be used when returning a check truncation entry. This reason for return should be used only if no other return reason code is applicable."
                                                    elif transfer_failure_reason == 'R12':
                                                        failure_reason = "Branch sold to another DFI. A financial institution received an entry to an account that was sold to another FI."
                                                    elif transfer_failure_reason == 'R13':
                                                        failure_reason = "Invalid ACH routing number. Entry contains a receiving DRI identification or gateway identification that is not a valid ACH routing number."
                                                    elif transfer_failure_reason == 'R14':
                                                        failure_reason = "Representative payee deceased or unable to continue in that capacity. The representative payee is a person either deceased or no longer able to continue in original capacity (ie. legally incapacitated adults or minors), while the beneficiary is not deceased."
                                                    elif transfer_failure_reason == 'R15':
                                                        failure_reason = "Beneficiary or account holder deceased. (1) The beneficiary is deceased. The beneficiary may or may not be the account holder; (2) The account holder (acting in a non-representative payee capacity) is an owner of the account and is deceased."
                                                    elif transfer_failure_reason == 'R16':
                                                        failure_reason = "Account frozen/Entry returned per OFAC instruction. 1) Access to account is restricted due to specific action taken by the RDFI or legal action 2) OFAC has instructed the RDFI or gateway to return the entry."
                                                    elif transfer_failure_reason == 'R17':
                                                        failure_reason = "File record edit criteria. Fields can’t be processed by RDFI."
                                                    elif transfer_failure_reason == 'R18':
                                                        failure_reason = "Improper effective entry date. The effective entry date for a credit entry is more than two banking days after the banking day of processing as established by the originating ACH operator or the effective date is after window of processing."
                                                    elif transfer_failure_reason == 'R19':
                                                        failure_reason = "Amount field error. Amount field is non-numeric, zero, or exceeding $25,000."
                                                    elif transfer_failure_reason == 'R20':
                                                        failure_reason = "Non-transaction account. The ACH entry destined for a non-transaction account, for example, an account against which transactions are prohibited or limited."
                                                    elif transfer_failure_reason == 'R21':
                                                        failure_reason = "Invalid company identification. The company identification information not valid."
                                                    elif transfer_failure_reason == 'R22':
                                                        failure_reason = "Invalid individual ID number. In CIE and MET entries, when the original ID number isn’t used, the receiver has indicated to the RDFI that the number with which the Originator was identified is not correct."
                                                    elif transfer_failure_reason == 'R23':
                                                        failure_reason = "Credit entry refused by receiver.  Receiver returned entry because, for instance,  minimum or exact amount not remitted. Any credit entry that is refused by the receiver may be returned by the RDFI."
                                                    elif transfer_failure_reason == 'R24':
                                                        failure_reason = "Duplicate entry. The RDFI has received what appears to be a duplicate entry; i.e., the trace number, date, dollar amount and/or other data matches another transaction."
                                                    elif transfer_failure_reason == 'R25':
                                                        failure_reason = "Addenda error. Addenda record indicator value is incorrect, with code invalid, out of sequence,  or missing."
                                                    elif transfer_failure_reason == 'R26':
                                                        failure_reason = "Mandatory field error. Erroneous data or missing data in a mandatory field."
                                                    elif transfer_failure_reason == 'R27':
                                                        failure_reason = "Trace number error. Original entry trace number is not present or does not correspond correctly in the addenda record on a return or notification of change entry."
                                                    elif transfer_failure_reason == 'R28':
                                                        failure_reason = "Routing number check digit error. The check digit for the routing number is invalid."
                                                    elif transfer_failure_reason == 'R29':
                                                        failure_reason = "Corporate customer advises not authorized. The RDFI has been notified by receiver (non-consumer) that a specific transaction is unauthorized."
                                                    elif transfer_failure_reason == 'R30':
                                                        failure_reason = "RDFI not participant in check truncation program. The RDFI does not participate in a check truncation program."
                                                    elif transfer_failure_reason == 'R31':
                                                        failure_reason = "Permissible return entry (CCD and CTX only). The REFI may return a CCD or CTX entry that the ODFI agrees to accept."
                                                    elif transfer_failure_reason == 'R32':
                                                        failure_reason = "RDFI non-settlement. The RDFI is not able to settle the entry."
                                                    elif transfer_failure_reason == 'R33':
                                                        failure_reason = "Return of XCK entry. The RDFI determines at its sole discretion to return an XCK entry."
                                                    elif transfer_failure_reason == 'R34':
                                                        failure_reason = "Limited participation DFI. The RDFI participation has been limited by a federal or state supervisor."
                                                    elif transfer_failure_reason == 'R35':
                                                        failure_reason = "Return of improper debit entry. Debit entries are not permitted for CIE entries or to loan accounts."
                                                    elif transfer_failure_reason == 'R36':
                                                        failure_reason = "Return of improper credit entry. ACH credit entries are not permitted for use with ARC, BOC, POP, RCK, TEL, XCK."
                                                    elif transfer_failure_reason == 'R37':
                                                        failure_reason = "Source document presented for payment. The source document to which an ARC, BOX, or POP entry relates has been presented for payment."
                                                    elif transfer_failure_reason == 'R38':
                                                            failure_reason = "Stop payment on source document"
                                                    elif transfer_failure_reason == 'R39':
                                                        failure_reason = "Improper source document/source document presented for payment"
                                                    elif transfer_failure_reason == 'R40':
                                                        failure_reason = "Return of ENR entry by federal government agency"
                                                    elif transfer_failure_reason == 'R41':
                                                        failure_reason = "Invalid transaction code"
                                                    elif transfer_failure_reason == 'R42':
                                                        failure_reason = "Routing number/check digit error"
                                                    elif transfer_failure_reason == 'R43':
                                                        failure_reason = "Invalid DFI account number"
                                                    elif transfer_failure_reason == 'R44':
                                                        failure_reason = "Invalid individual ID number/identification number"
                                                    elif transfer_failure_reason == 'R45':
                                                        failure_reason = "Invalid individual name/company name"
                                                    elif transfer_failure_reason == 'R46':
                                                        failure_reason = "Invalid representative payee indicatort"
                                                    elif transfer_failure_reason == 'R47':
                                                        failure_reason = "Duplicate enrollment"
                                                    elif transfer_failure_reason == 'R50':
                                                        failure_reason = "State law affecting RCK acceptance"
                                                    elif transfer_failure_reason == 'R51':
                                                        failure_reason = "Item related to RCK entry is ineligible or RCK entry is improper"
                                                    elif transfer_failure_reason == 'R52':
                                                        failure_reason = "Stop payment on item related to RCK entry"
                                                    elif transfer_failure_reason == 'R53':
                                                        failure_reason = "Item and RCK entry presented for payment"
                                                    elif transfer_failure_reason == 'R61':
                                                        failure_reason = "Misrouted return"
                                                    elif transfer_failure_reason == 'R62':
                                                        failure_reason = "Return of erroneous or reversing debt"
                                                    elif transfer_failure_reason == 'R67':
                                                        failure_reason = "Duplicate return"
                                                    elif transfer_failure_reason == 'R68':
                                                        failure_reason = "Untimely return"
                                                    elif transfer_failure_reason == 'R69':
                                                        failure_reason = "Field error(s)"
                                                    elif transfer_failure_reason == 'R70':
                                                        failure_reason = "Permissible return entry not accepted/return not requested by ODFI"
                                                    elif transfer_failure_reason == 'R71':
                                                        failure_reason = "Misrouted dishonored return"
                                                    elif transfer_failure_reason == 'R72':
                                                        failure_reason = "Untimely dishonored return"
                                                    elif transfer_failure_reason == 'R73':
                                                        failure_reason = "Timely original return"
                                                    elif transfer_failure_reason == 'R74':
                                                        failure_reason = "Corrected return"
                                                    elif transfer_failure_reason == 'R75':
                                                        failure_reason = "Return not duplicate"
                                                    elif transfer_failure_reason == 'R76':
                                                        failure_reason = "No errors found"
                                                    elif transfer_failure_reason == 'R77':
                                                        failure_reason = "Non-acceptance of R62 dishonored return"
                                                    elif transfer_failure_reason == 'R80':
                                                        failure_reason = "IAT entry coding errors"
                                                    elif transfer_failure_reason == 'R81':
                                                        failure_reason = "Non-participant in IAT program"

                                                    else:
                                                        failure_reason = "Failure Unknown - Contact Admin"

                                                        mongoDB.Company.update({"company_ID": company_ID}, {"$push": {transaction_var: { "transaction_num": payment_num, "transaction_date": today_date, "transaction_confirmed_date":"Failed", "transaction_amount":pull_amount, "total_amount_repaid":total_amount_repaid, "default_amount":default_amount, "percent_paid":percent_paid, "note":failure_reason, "transaction_ID":"None - Transaction Intercepted", "status":"Failed", "error":failure_reason}}});

                                                    print('Failure Reason --> ', failure_reason)

                                                except:

                                                    failure_reason = "None"
                                                    print('No Failure')




                                                    print('88888 -------------------------------->')


                                                    #try:
                                                    payback_latest_row = payback_table_results[-1]
                                                    payment_num = int(payback_latest_row[0]) + 1
                                                    if status == "Defaulted":
                                                        default_amount = round(float(default_amount) - pull_amount, 2)
                                                    #except:
                                                    #    payment_num = 1

                                                    print('99999 -------------------------------->')

                                                    transaction_date = datetime.today().strftime('%Y-%m-%d')
                                                    print('transaction_date -------------------------------->', transaction_date)
                                                    transaction_confirmed_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
                                                    print('transaction_confirmed_date -------------------------------->', transaction_confirmed_date)

                                                    for key, val in syndicators.items():
                                                        synd_collection = mongoDB.Syndicators.find_one({ "syndicator_business_name": key })
                                                        syndicated_percent = float(val) / float(advance_amount)
                                                        print('REV ------------->   ---------------------->', synd_collection['revenue'])
                                                        rev_amount = round(float(synd_collection['revenue']) + (float(total_amount_repaid) * syndicated_percent),2)
                                                        mongoDB.Syndicators.update({ "syndicator_business_name": key }, {"$set": {'revenue': rev_amount}});



                                                    transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track"


                                                    mongoDB.Company.update({"company_ID": company_ID}, {"$push": {transaction_var: { "transaction_num": payment_num, "transaction_date": transaction_date, "transaction_confirmed_date":"Pending", "transaction_amount":pull_amount, "total_amount_repaid":total_amount_repaid, "default_amount":default_amount, "percent_paid":percent_paid, "note":"Automated_ACH_Pull", "transaction_ID":transfer_id, "status":transfer_status, "error":failure_reason}}});



                                                    print('transaction transacted')
                                                    break


                                            else:
                                                print('transaction process failed')






if __name__ == '__main__':
    app
