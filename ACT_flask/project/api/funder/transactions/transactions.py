from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
import pandas as pd


Transactions_Blueprint = Blueprint('MCA_Transactions', __name__)
@Transactions_Blueprint.route('/api/funder/transactions/', methods=['GET', 'POST'])
def MCA_Transactions():


    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    mongoDB = db[session.get("user_database")]

    transaction_list = []
    for company in mongoDB.Merchants.find():
        for cash_ad in company['cash_advance_contracts']:
            try:
                for transaction in cash_ad['transaction_track']:
                    transaction_list.append([company['company_DBA'], transaction['transaction_date'], transaction['transaction_confirmed_date'], transaction['transaction_amount'], transaction['transaction_ID']])

            except:
                print('no val')

    try:
        transaction_list_sorted = reversed(pd.DataFrame(transaction_list).sort_values(by=[1]).values)
    except:
        transaction_list_sorted = []

    return render_template("/Funder/Transactions/transactions.html",  transaction_list_sorted=transaction_list_sorted, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
