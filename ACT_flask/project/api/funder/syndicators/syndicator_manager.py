from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db


Syndicator_Manager_Blueprint = Blueprint('MCA_Syndicator_Manager', __name__)
@Syndicator_Manager_Blueprint.route('/api/funder/syndicators/syndicator_manager/', methods=['GET', 'POST'])
def MCA_Syndicator_Manager():


    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]
    
    # user_table = db.Credentials.Users.find_one({ "email": session.get("email") })
    access_status = session.get('access_status')
    notification_count = session.get('notification_count')


    contract_count = 0
    syndicator_array = []
    for xx in mongoDB.Merchants.find({"cash_advance_contracts.status": "Open"}):
        #print('cash and synd ---------------------------------------------------> ', xx, file=sys.stderr)
        print('cash and synd ---------------------------------------------------> ', xx['cash_advance_contracts'][contract_count]['syndicators'], file=sys.stderr)
        if xx['cash_advance_contracts'][contract_count]['syndicators']:
            current_amount_syndicated = 0
            for key, val in xx['cash_advance_contracts'][contract_count]['syndicators'].items():
                print('key ---------------------------------------------------> ', key, file=sys.stderr)
                print('val ---------------------------------------------------> ', val, file=sys.stderr)
                current_amount_syndicated += float(val)
                contract_count += 1
            contract_count = 0

            print('company ID ---------------------------------------------------> ', xx['company_ID'], file=sys.stderr)

            dba = xx['company_DBA']
            company_ID = xx['company_ID']
            number_of_syndicators = len(xx['cash_advance_contracts'][contract_count]['syndicators'])
            amount_left_to_fund = float(xx['cash_advance_contracts'][contract_count]['advance_amount']) - current_amount_syndicated
            precent_syndicated = round((current_amount_syndicated / float(xx['cash_advance_contracts'][contract_count]['advance_amount'])) * 100, 2)

            syndicator_array.append([dba, company_ID, number_of_syndicators, amount_left_to_fund, precent_syndicated])

        else:

            dba = xx['company_DBA']
            company_ID = xx['company_ID']
            number_of_syndicators = 0
            amount_left_to_fund = float(xx['cash_advance_contracts'][contract_count]['advance_amount'])
            precent_syndicated = 0

            syndicator_array.append([dba, company_ID, number_of_syndicators, amount_left_to_fund, precent_syndicated])




    print('company_sindicators ---------------------------------------------------> ', syndicator_array, file=sys.stderr)



    try:
        all_companies = mongoDB.Merchants.find()
    except:
        all_companies = []




    #all_syndicators = mongoDB.Syndicators.find()


    master_synd_list = []
    for synd in mongoDB.Syndicators.find():
        syndicator_ID = synd['syndicator_ID']
        syndicator_business_name = synd['syndicator_business_name']
        total_syndicated = float(synd['total_syndicated'])
        number_of_advances = int(synd['number_of_advances'])
        revenue = float(synd['revenue'])
        profit = revenue - total_syndicated
        master_synd_list.append([syndicator_ID, syndicator_business_name, number_of_advances, total_syndicated, revenue, profit])


    print('MASTER LIST --- -- - >', master_synd_list, file=sys.stderr)

    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")



    return render_template("/Funder/Syndicators/Syndicator_Manager/syndicator_manager.html", syndicator_array=syndicator_array, master_synd_list=master_synd_list, access_status=access_status, notification_count=notification_count)
