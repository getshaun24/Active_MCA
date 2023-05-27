from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import dwollav2
import sys
import datetime
from datetime import datetime, timedelta
# from server import mongoDB_master_access, dwolla_app_token
from project import db 
from project.api.dwolla import dwolla_app_token
from flask_login import login_required


Fund_Blueprint = Blueprint('MCA_Fund', __name__)
@Fund_Blueprint.route('/api/funder/advances/pre_funded/fund/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Fund():

    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongo_master = db.Master_Credentials.master_user_list.find_one({ "email": session.get("email") })
        dwolla_funding_source_destination_account = "https://api-sandbox.dwolla.com/funding-sources/" + mongo_master["dwolla_funding_source_destination_account"]

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        if access_status != "admin":
            return redirect(url_for('MCA_Login'))



        company_id_var = request.args.get('company_id_var', None)




        get_company = mongoDB.Company.find_one({"company_ID": company_id_var})
        company_name = get_company["company_DBA"]
        cash_ads = get_company["Cash_Advance_Contracts"]
        len_of_cash = len(cash_ads)
        dwolla_customer_url_id = get_company["dwolla_customer_url_id"]
        dwolla_funding_source_url = get_company["Cash_Advance_Contracts"][(len_of_cash -1)]["dwolla_funding_source_url"]
        selected_account_ID = get_company["Cash_Advance_Contracts"][(len_of_cash -1)]["selected_account_ID"]
        contract_ID = get_company["Cash_Advance_Contracts"][(len_of_cash -1)]["contract_ID"]
        advance_amount = get_company["Cash_Advance_Contracts"][(len_of_cash -1)]["advance_amount"]

        print("dwolla_funding_source_url ------------------->>  ", dwolla_funding_source_url, file=sys.stderr)



        all_syndicators = []
        for synd in mongoDB.Syndicators.find():
            all_syndicators.append(synd['syndicator_business_name'])
        all_syndicators = sorted(all_syndicators, key=lambda v: (v.upper(), v[0].islower()))

        print("all_syndicators ------------------->>  ", all_syndicators, file=sys.stderr)


        all_presets = []
        preset_names = []
        for preset in mongoDB.Synd_preset.find():
            kv_list = []
            for k, v in preset['preset_dict'].items():
                if k == 'preset_name':
                    preset_names.append(v)
                kv_list.append([k, v])
            all_presets.append(kv_list)
            #all_presets.append(dumps(preset))

        print("preset names ------------------->>  ", preset_names, file=sys.stderr)
        print("preset ------------------->>  ", all_presets, file=sys.stderr)


        if request.method == 'POST':

            print("POST ------------------->>  ", file=sys.stderr)


            company_id_var = request.args.get('company_id_var', None)


            get_company = mongoDB.Company.find_one({"company_ID": company_id_var})
            company_name = get_company["company_DBA"]

            print(get_company["Cash_Advance_Contracts"][-1]['advance_amount'])

            advance_amount = get_company["Cash_Advance_Contracts"][-1]['advance_amount']

            print('advance amount ---->', advance_amount)

            form_data = request.form
            print('form data -- >', form_data, file=sys.stderr)






            syndicator_dict = {}
            for elm in all_syndicators:
                if form_data[elm] != '' or form_data['presets'] == True:
                    print("elm ------------------->>  ", form_data[elm], file=sys.stderr)
                    percent_to_amount = round(float(advance_amount) * (float(form_data[elm].replace('%', '')) / 100), 2)
                    print("percent_to_amount ------------------->>  ", percent_to_amount, file=sys.stderr)
                    syndicator_dict[elm] = percent_to_amount
                    synd_collection = mongoDB.Syndicators.find_one({ "syndicator_business_name": elm })
                    total_syndicated = synd_collection['total_syndicated'] + float(percent_to_amount)
                    total_active_syndicated = synd_collection['total_active_syndicated'] + float(percent_to_amount)
                    number_of_advances = synd_collection['number_of_advances'] + 1
                    number_of_active_advances = synd_collection['number_of_active_advances'] + 1

                    mongoDB.Syndicators.update({ "syndicator_business_name": elm }, {"$set": {'total_syndicated': total_syndicated, 'total_active_syndicated': total_active_syndicated, 'number_of_advances': number_of_advances, 'number_of_active_advances': number_of_active_advances}});






            request_body = {
                    '_links': {
                        'source': {
                             'href': dwolla_funding_source_destination_account
                                    },
                        'destination': {
                            'href': 'https://api-sandbox.dwolla.com/funding-sources/'  + dwolla_funding_source_url
                                    }
                        },
                    'amount': {
                        'currency': 'USD',
                        #'value': advance_amount_to_send
                        'value': 5000
                        },
                    'clearing': {
                        'destination': 'next-available'
                        }
                    }




            if True:
                transfer = dwolla_app_token.post('transfers', request_body)
                transfer_url = transfer.headers['location']
                transfer_id = transfer_url[41:]


                transfer_retrieve = dwolla_app_token.get(transfer_url)
                transfer_status = transfer_retrieve.body['status']


                try:
                    payback_latest_row = payback_table_results[-1]
                    payment_num = int(payback_latest_row[0]) + 1
                except:
                    payment_num = 1


                transaction_date = datetime.today().strftime('%Y-%m-%d')

            else:
                print('transaction failed', file=sys.stderr)



            transaction_var = "Cash_Advance_Contracts." + str(len_of_cash - 1) + ".Transaction_track"

            cash_ad_var = "Cash_Advance_Contracts." + str(len_of_cash - 1)   + ".Syndicators"




            mongoDB.Company.update({"company_ID": company_id_var},
                 {"$push": {cash_ad_var: syndicator_dict}})


            status_var = "Cash_Advance_Contracts." + str(len_of_cash - 1) + ".status"
            mongoDB.Company.update({"company_ID": company_id_var}, {"$set": {status_var: "Open"}})



            mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {transaction_var: { "transaction_num": 0, "transaction_date": transaction_date, "transaction_confirmed_date":'Pending', "transaction_amount":float(advance_amount), "total_amount_repaid":0, "default_amount":0, "percent_paid":0, "note":"First Payment Deposit", "transaction_ID":transfer_id, "status":transfer_status, "error":"None"}}})




            print('transaction transacted', file=sys.stderr)
            return redirect(url_for('MCA_Prefunded.MCA_Prefunded'))



    return render_template("/Funder/Advances/Pre_Funded/Fund/fund.html", preset_names=preset_names, all_presets=all_presets, all_syndicators=all_syndicators, company_name=company_name, company_id_var=company_id_var, access_status=access_status, notification_count=notification_count, advance_amount=advance_amount)
