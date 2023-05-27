from flask import Blueprint, session, url_for, request, redirect, render_template, jsonify
from flask_session import Session
import sys
import pymongo
import os
# from server import signnow_access_token, ocrolus_access_token
from project.api.signnow import signnow_access_token
from project.api.ocrolus import ocrolus_access_token
from project import db
import signnow_python_sdk
import uuid
from random import random
import datetime
from datetime import datetime, timedelta
import gridfs
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


All_Precontract_Blueprint = Blueprint('MCA_All_Precontract', __name__)
@All_Precontract_Blueprint.route('/api/funder/advances/pre_funded/all_precontract/', methods=['GET', 'POST']) # <- from '/'
@jwt_required
def MCA_All_Precontract():

    if current_user.access_status != 'admin':
        return jsonify({'msg': 'Access denied'}), 403

    mongoDB = db[current_user.user_database]

    all_companies = mongoDB.Merchants.find()
    all_pre_contracts = mongoDB.Pre_Contract.find()

    companies = []
    for comp in all_companies:
        for cash_ad in comp['cash_advance_contracts']:
            if cash_ad['status'] == "Prefund":
                signnow_document_id = cash_ad['signnow_document_id']
                document_data = signnow_python_sdk.Document.get(signnow_access_token['access_token'], signnow_document_id)
                try:
                    signnow_status = document_data['field_invites'][0]['status']
                except:
                    signnow_status = 'None'

                companies.append([comp['company_DBA'], comp['company_ID'], signnow_status] )


    pre_contracts_list = []
    try:
        for pre in all_pre_contracts:
            pre_contracts_list.append([pre['company_DBA'], pre['company_ID'], pre['ISO_document'], pre['ISO_document'], pre['date_added']])
    except:
        pre_contracts_list = []




    if request.method == 'POST':

        print("POST ------------------->>  ", file=sys.stderr)

        form_data = request.form


        #------------ Cash Advance Contract ------------

        company_DBA = form_data['merchant_name']
        ISO_document = request.files["ISO_document"]
        ISO_document_stream = request.files["ISO_document"] #make a copy so a streamed version can be sent to Ocrolus
        bank_statements_1 = request.files["bank_statements_1"]

        if request.files['bank_statements_2'].filename != '':
            bank_statements_2 = request.files["bank_statements_2"]
            bank_statements_ID_2 = 'bank_statements_2' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (str(random()) + 'bank_statements' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
        if request.files['bank_statements_3'].filename != '':
            bank_statements_3 = request.files["bank_statements_3"]
            bank_statements_ID_3 = 'bank_statements_3' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (str(random()) + 'bank_statements' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")



        company_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(random()) + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))).replace("-", "")
        ISO_document_ID = 'ISO_Document_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (str(random()) + 'ISO_document' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
        bank_statements_ID_1 = 'bank_statements_1' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (str(random()) + 'bank_statements' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

        print('company_ID -- >', company_ID, file=sys.stderr)
        print('ISO_document_ID -- >', ISO_document_ID, file=sys.stderr)
        print('bank_statements_ID -- >', bank_statements_ID_1, file=sys.stderr)


        # gridfs code block is placed here becasue of a save error coming
        # downstream from the save image to static ocrolus folder line
        fs = gridfs.GridFS(mongoDB)
        try:
            fs.put(ISO_document, filename=ISO_document_ID)
        except:
            print("No ISO Docs", file=sys.stderr)
        try:
            fs.put(bank_statements_1, filename=bank_statements_ID_1)
        except:
            print("No Bank Statements 1", file=sys.stderr)
        try:
            fs.put(bank_statements_2, filename=bank_statements_ID_2)
            mongoDB.Pre_Contract.update({"company_ID": company_ID}, {"$push": {"beneficial_owner_docs_2": beneficial_owner_docs_ID_2}})
        except:
            print("No Bank Statements 2", file=sys.stderr)
        try:
            fs.put(bank_statements_3, filename=bank_statements_ID_3)
            mongoDB.Pre_Contract.update({"company_ID": company_ID}, {"$push": {"beneficial_owner_docs_3": beneficial_owner_docs_ID_3}})
        except:
            print("No Bank Statements 3", file=sys.stderr)




        book_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(ocrolus_access_token)
            }

        book_url = "https://api.ocrolus.com/v1/book/add"
        book_payload = {"name": company_ID}
        #book_response = (requests.request("POST", book_url, json=book_payload, headers=book_headers)).json()
        #print('book_response -- > ', book_response, file=sys.stderr)
        #book_uuid = str(book_response['response']['uuid'])
        #book_pk = str(book_response['response']['pk'])
        #print('UUID -- > ', book_uuid, file=sys.stderr)
        #print('PK -- > ', book_pk, file=sys.stderr)


        upload_headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + str(ocrolus_access_token)
        }


        filepath = 'static/ocrolus/' + ISO_document_ID + '.pdf'
        ISO_document_stream.stream.seek(0)
        ISO_document_stream.save('static/ocrolus/' + ISO_document_ID + '.pdf')
        upload_url = "https://api.ocrolus.com/v1/book/upload"
        #upload_data = {'pk':book_pk} # The book's primary key
        upload_files = { 'upload': open(filepath,'rb') }
        #upload_response = (requests.post(upload_url, headers=upload_headers, data=upload_data, files=upload_files)).json()
        os.remove(filepath)
        #print(upload_response, file=sys.stderr)


        #page_count_total = upload_response['response']['uploaded_docs'][0]['page_count']
        page_count_total = 1


        bank_statements_id_dict = {'bank_statements_ID_1':bank_statements_ID_1}

        ii = 1
        while ii <= 6:

            try:
                if request.files['bank_statements_' + str(ii)].filename != '':
                    loop_statement = eval('bank_statements_' + str(ii))
                    loop_ID = eval('bank_statements_ID_' + str(ii))
                    print('loop_statement -- > ', loop_statement, file=sys.stderr)
                    print('loop_ID -- > ', loop_ID, file=sys.stderr)



                    upload_headers = {
                         "Accept": "application/json",
                         "Authorization": "Bearer " + str(ocrolus_access_token)
                         }


                    filepath = 'static/ocrolus/' + loop_ID + '.pdf'
                    loop_statement.stream.seek(0)
                    loop_statement.save('static/ocrolus/' + loop_ID + '.pdf')
                    upload_url = "https://api.ocrolus.com/v1/book/upload"
                    upload_data = {'pk':book_pk} # The book's primary key
                    upload_files = { 'upload': open(filepath,'rb') }
                    #upload_response = (requests.post(upload_url, headers=upload_headers, data=upload_data, files=upload_files)).json()
                    os.remove(filepath)
                    #page_count = upload_response['response']['uploaded_docs'][0]['page_count']
                    page_count = 2
                    page_count_total += page_count

                    #print(upload_response, file=sys.stderr)

                    bank_statements_id_dict['bank_statements_ID_' + str(ii)] = loop_ID

                    ii += 1
                else:
                    ii += 1
            except:
                ii +=1






        today_date = datetime.today().strftime('%m/%d/%Y')

        print('begin insertion -- >', file=sys.stderr)

        mongoDB.Pre_Contract.insert_one({"company_ID":company_ID, "company_DBA": company_DBA, "ISO_document": ISO_document_ID, "bank_statements":bank_statements_id_dict, "date_added":today_date,
        #"Ocrolus":{'book_uuid':book_uuid, 'book_pk':book_pk, 'page_count':page_count_total} })
        "ocrolus":{'book_uuid':'book_uuid', 'book_pk':'book_pk', 'page_count':'page_count_total'} })


        print('insertion complete -- >', file=sys.stderr)




    return render_template("/Funder/Advances/Pre_Funded/All_Precontract/all_precontract.html", companies=companies, access_status=session.get('access_status'), notification_count=session.get('notification_count'), pre_contracts_list=pre_contracts_list)
