from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db
import pandas as pd


Data_Upload_Blueprint = Blueprint('MCA_Data_Upload', __name__)
@Data_Upload_Blueprint.route('/api/master/data_upload/', methods=['GET', 'POST'])
def MCA_Data_Upload():


    if session.get("access_status") != "master":
        return redirect(url_for('logout'))
        

    mongoDB = db[session.get("user_database")]

    user_table = mongoDB.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]
    notification_count = user_table["notification_count"]

    if access_status != "admin":
        return redirect(url_for('MCA_Login'))


    if request.method == 'POST':

        # get the uploaded file
        uploaded_file = request.files['file']
        form_data = request.form
        company_ID = form_data['company_ID']
        contract_count = form_data['contract_count']


        print("111111111111   =======================================================================", file=sys.stderr)
        print (uploaded_file, file=sys.stderr)
        print("222222222    =======================================================================", file=sys.stderr)


        col_names = ['contract_num','payment_num','transaction_date', 'transaction_confirmed_date', 'transaction_amount' , 'open_amount_repaid', 'expected_repayment_amount', 'open_percent_paid', 'note', 'transaction_ID', 'status', 'error']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(uploaded_file,names=col_names, header=None)
        # Loop through the Rows

        print (csvData.head(), file=sys.stderr)
        for i,row in csvData.iterrows():
            if i == 0:
                print (row['contract_num'], file=sys.stderr)
                print(i,row['contract_num'],row['payment_num'],row['transaction_date'],row['transaction_confirmed_date'],row['transaction_amount'],row['open_amount_repaid'], row['expected_repayment_amount'],row['open_percent_paid'],row['note'],row['transaction_ID'],row['status'],row['error'], file=sys.stderr)
            else:
                print (row['contract_num'], file=sys.stderr)
                print(i,row['contract_num'],row['payment_num'],row['transaction_date'],row['transaction_confirmed_date'],row['transaction_amount'],row['open_amount_repaid'], row['expected_repayment_amount'],row['open_percent_paid'],row['note'],row['transaction_ID'],row['status'],row['error'], file=sys.stderr)


                transaction_var = "Cash_Advance_Contracts." + str(contract_count) + ".Transaction_track"
                contract_var = "Cash_Advance_Contracts." + str(contract_count) + ".open_amount_repaid"


                mongoDB.Company.update({"company_ID": company_ID},
                {"$set": {contract_var:row['open_amount_repaid']}});


                mongoDB.Company.update({"company_ID": company_ID},
                 {"$push": {transaction_var: { "transaction_num": row['payment_num'], "transaction_date": row['transaction_date'], "transaction_confirmed_date":row['transaction_confirmed_date'], "transaction_amount":row['transaction_amount'], "open_amount_repaid":row['open_amount_repaid'], "open_percent_paid":row['open_percent_paid'], "note":row['note'], "transaction_ID":row['transaction_ID'], "status":row['status'], "error":row['error']}}});



    return render_template("/Active_MCA_Master/Data_Upload/data_upload.html", access_status=access_status, notification_count=notification_count)
