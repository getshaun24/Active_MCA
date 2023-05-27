from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
import re
from flask import render_template
from flask import flash
import datetime
from datetime import datetime, timedelta
from project.api.signnow import signnow_access_token
from project import db
import signnow_python_sdk
import requests
import gridfs
import codecs
# import magic
import base64
from base64 import b64encode
import json
from flask_login import login_required


Edit_Contract_Blueprint = Blueprint('MCA_Edit_Contract', __name__)
@Edit_Contract_Blueprint.route('/api/funder/advances/pre_funded/edit_contract/', methods=['GET', 'POST'])  # <- from '/'
@login_required
def MCA_Edit_Contract():
    
    is_live_production_env = False
    if current_app.config['ENV'] == 'production':
        is_live_production_env = True

    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    else:

        mongoDB = db[session.get("user_database")]

        user_table = db.Credentials.Users.find_one({"email": session.get("email")})
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        company_id_var = request.args.get('mid', None)

        # Create access_token for the user
        print("Creating access token:")
        print("access_token ------------------->>  ", signnow_access_token, file=sys.stderr)

        today_date = datetime.today().strftime('%m/%d/%Y')

        get_company = mongoDB.Merchants.find_one({"company_ID": company_id_var})
        company_name = get_company["company_DBA"]
        legal_company_name = get_company["legal_company_name"]
        business_ein = get_company['business_ein']
        business_type = get_company['business_type']
        business_address = get_company['business_address']
        business_city = get_company['business_city']
        business_state = get_company['business_state']
        business_postal = get_company['business_postal']

        business_email = get_company["business_email"]
        poc_email = get_company["poc_email"]
        len_of_cash = len(get_company["cash_advance_contracts"])
        cash_ad_var = "cash_advance_contracts." + str(len_of_cash - 1)

        start_date = get_company["cash_advance_contracts"][-1]['start_date']
        expected_end_date = get_company["cash_advance_contracts"][-1]['expected_end_date']
        duration = get_company["cash_advance_contracts"][-1]['duration']
        split_percent = get_company["cash_advance_contracts"][-1]['split_percent']
        factor_rate = get_company["cash_advance_contracts"][-1]['factor_rate']
        fico_score = get_company["cash_advance_contracts"][-1]['fico_score']
        funded_via = get_company["cash_advance_contracts"][-1]['funded_via']
        position = get_company["cash_advance_contracts"][-1]['position']
        tags = get_company["cash_advance_contracts"][-1]['tags']
        ACH_pull_schedule = get_company["cash_advance_contracts"][-1]['ACH_pull_schedule']
        advance_amount = get_company["cash_advance_contracts"][-1]['advance_amount']
        pull_amount = get_company["cash_advance_contracts"][-1]['pull_amount']
        try:
            selected_templates = get_company["cash_advance_contracts"][-1]['SignNow']['selected_templates']
        except:
            selected_templates = 'None'
        try:
            signnow_document_id = get_company["cash_advance_contracts"][-1]['signnow_document_id']
            signnow_status = get_company["cash_advance_contracts"][-1]['signnow_status']
        except:
            signnow_document_id = 'None'
            signnow_status = 'None'


        print("selected_templates ------------------->>  ", selected_templates, file=sys.stderr)
        print("signnow_document_id ------------------->>  ", signnow_document_id, file=sys.stderr)
        print("signnow_access_token ------------------->>  ", signnow_access_token, file=sys.stderr)

        email_in_db_list = set([business_email, poc_email])
        email_list = []
        email_count = 0
        for ee in email_in_db_list:
            # add email number for unique checkbox name
            email_number = 'email_num_' + str(email_count)
            email_list.append([email_number, ee])
            email_count += 1


        fs = gridfs.GridFS(mongoDB)


        temp_list = []
        role_num_list = []
        temp_count = 1
        for temp in mongoDB.SignNow_Templates.find():
            for_form_name = "template_" + str(temp_count)
            fsgrid_template_id = temp['fsgrid_template_id']
            template_id = temp['template_id']
            template_name = temp['template_name']
            number_of_roles = int(temp['number_of_roles'])

            role_num_list.append(number_of_roles)

            image = fs.get_last_version(filename=fsgrid_template_id)
            base64_data = codecs.encode(image.read(), 'base64')
            image = base64_data.decode('utf-8')

            temp_list.append([template_id, template_name , image, for_form_name])
            temp_count += 1



        signers_needed = max(role_num_list)

        if request.method == 'POST':

            form_data = request.form
            print('form data ============= ======== =========== >>>: ', form_data, file=sys.stderr)

            try:

                if form_data['contract_method'] == 'new_contract':


                    start_date = form_data["start_date"]
                    expected_end_date = form_data["expected_end_date"]
                    split_percent = form_data["split_percent"]
                    factor_rate = form_data["factor_rate"]
                    fico_score = form_data["fico_score"]
                    funded_via = form_data["funded_via"]
                    position = form_data["position"]
                    tags = form_data["tags"]
                    print("yes a ------------------->>  ", file=sys.stderr)
                    try:
                        ACH_pull_schedule = form_data["ACH_pull_schedule"]
                    except:
                        ACH_pull_schedule = None
                    print("yes b ------------------->>  ", file=sys.stderr)
                    advance_amount_str = form_data["advance_amount"]
                    pull_amount_str = form_data["pull_amount"]
                    non_decimal = re.compile(r'[^\d.]+')
                    advance_amount = float(non_decimal.sub('', advance_amount_str))
                    pull_amount = float(non_decimal.sub('', pull_amount_str))
                    management_fee = float(advance_amount) * (float(form_data["management_fee"].replace('%', '')) / 100)
                    commission = float(advance_amount) * (float(form_data["commission"].replace('%', '')) / 100)
                    bank_fee = (form_data["bank_fee"].replace('$', '')).replace(',', '')

                    duration = abs((datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(expected_end_date, "%Y-%m-%d")).days)
                    expected_repayment_amount = float(advance_amount) * float(factor_rate)


                    selected_templates_list = []
                    for temp in temp_list:
                        try:
                            selected_template_id = form_data[temp[3]]
                            selected_templates_list.append(selected_template_id)
                        except:
                            print('not submitted')
                    print("selected_templates_list ------------------->>  ", selected_templates_list, file=sys.stderr)


                    get_company = mongoDB.Merchants.find_one({"company_ID": company_id_var})
                    contract_ID = get_company["cash_advance_contracts"][-1]['contract_ID']
                    #date_added = get_company["cash_advance_contracts"][-1]['date_added']
                    selected_account_ID = get_company["cash_advance_contracts"][-1]['selected_account_ID']
                    dwolla_funding_source_url = get_company["cash_advance_contracts"][-1]['dwolla_funding_source_url']

                    print("ADDING TO MONGO ------------------->>  ", file=sys.stderr)

                    mongoDB.Merchants.update({"company_ID": company_id_var},
                     {"$set": {cash_ad_var: {"contract_ID": contract_ID, "status": "Prefund", 'last_updated':today_date, "start_date": start_date, "expected_end_date": expected_end_date, "duration": duration, "split_percent": split_percent, "factor_rate": factor_rate, "funded_via": funded_via, "fico_score": fico_score, "position": position, "tags": tags, "advance_amount":advance_amount, "pull_amount":pull_amount, "expected_repayment_amount": expected_repayment_amount, "day":0, "total_amount_repaid":0, "default_amount":0, "percent_paid":0, "bank_fee":bank_fee, "commission": commission, "management_fee":management_fee, "ACH_pull_schedule": ACH_pull_schedule, "pause_until":"None", "dwolla_funding_source_url": dwolla_funding_source_url, "selected_account_ID": selected_account_ID, "SignNow":{'selected_templates': selected_templates_list, 'document_group': { 'document_group_id': '-', 'document_group_name': '-', 'document_group_doc_number':'-', 'document_group_last_modified': '-', 'sent_documents': []}}}}})




                if form_data['contract_method'] == 'update_contract':
                    # ------------ Cash Advance Contract ------------

                    updated_start_date = form_data["start_date"]
                    updated_expected_end_date = form_data["expected_end_date"]
                    updated_split_percent = form_data["split_percent"]
                    updated_factor_rate = form_data["factor_rate"]
                    updated_fico_score = form_data["fico_score"]
                    updated_funded_via = form_data["funded_via"]
                    updated_position = form_data["position"]
                    updated_tags = form_data["tags"]
                    print("yes a ------------------->>  ", file=sys.stderr)
                    try:
                        updated_ACH_pull_schedule = form_data["ACH_pull_schedule"]
                    except:
                        updated_ACH_pull_schedule = None
                    print("yes b ------------------->>  ", file=sys.stderr)
                    updated_advance_amount_str = form_data["advance_amount"]
                    updated_pull_amount_str = form_data["pull_amount"]
                    non_decimal = re.compile(r'[^\d.]+')
                    updated_advance_amount = float(non_decimal.sub('', updated_advance_amount_str))
                    updated_pull_amount = float(non_decimal.sub('', updated_pull_amount_str))
                    updated_management_fee = float(advance_amount) * (float(form_data["management_fee"].replace('%', '')) / 100)
                    updated_commission = float(advance_amount) * (float(form_data["commission"].replace('%', '')) / 100)
                    updated_bank_fee = (form_data["bank_fee"].replace('$', '')).replace(',', '')

                    print("updated_advance_amount 1 ------------------->>  ", updated_advance_amount, file=sys.stderr)


                    selected_templates_list = []
                    for temp in temp_list:
                        try:
                            selected_template_id = form_data[temp[3]]
                            selected_templates_list.append(selected_template_id)
                        except:
                            print('not submitted')

                    start_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".start_date"
                    end_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".expected_end_date"
                    split_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".split_percent"
                    factor_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".factor_rate"
                    funded_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".funded_via"
                    fico_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".fico_score"
                    position_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".position"
                    tags_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".tags"
                    ach_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".ACH_pull_schedule"
                    advance_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".advance_amount"
                    pull_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".pull_amount"
                    duration_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".duration"
                    comission_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".commission"
                    management_fee_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".management_fee"
                    bank_fee_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".bank_fee"
                    repay_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".expected_repayment_amount"
                    selected_templates_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".SignNow.selected_templates"

                    if updated_start_date:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {start_var: updated_start_date}})
                        start_date = updated_start_date
                        flash(u'Start Date Updated', 'flash_success')
                    if updated_expected_end_date:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {end_var: updated_expected_end_date}})
                        expected_end_date = updated_expected_end_date
                        flash(u'Expected End Date Updated', 'flash_success')
                    if updated_split_percent:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {split_var: updated_split_percent}})
                        split_percent = updated_split_percent
                        flash(u'Split Percent Updated', 'flash_success')
                    if updated_factor_rate:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {factor_var: updated_factor_rate}})
                        factor_rate = updated_factor_rate
                        flash(u'Factor rate Updated', 'flash_success')
                    if updated_funded_via:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {funded_var: updated_funded_via}})
                        funded_via = updated_funded_via
                        flash(u'Funded Via', 'flash_success')
                    if updated_fico_score:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {fico_var: updated_fico_score}})
                        fico_score = updated_fico_score
                        flash(u'Fico Score', 'flash_success')
                    if updated_position:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {position_var: updated_position}})
                        position = updated_position
                        flash(u'Position Updated', 'flash_success')
                    if updated_tags:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {tags_var: updated_tags}})
                        tags = updated_tags
                        flash(u'Tags Updated', 'flash_success')
                    if updated_ACH_pull_schedule:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {ach_var: updated_ACH_pull_schedule}})
                        ACH_pull_schedule = updated_ACH_pull_schedule
                        flash(u'ACH Pull Schedule Updated', 'flash_success')
                    if updated_advance_amount:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {advance_var: updated_advance_amount}})
                        advance_amount = updated_advance_amount
                        flash(u' Advance Amount Updated', 'flash_success')
                    if updated_pull_amount:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {pull_var: updated_pull_amount}})
                        pull_amount = updated_pull_amount
                        flash(u' Pull Amount Updated', 'flash_success')
                    if updated_management_fee:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {pull_var: updated_management_fee}})
                        management_fee = updated_management_fee
                        flash(u' Management Fee Updated', 'flash_success')
                    if updated_commission:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {pull_var: updated_commission}})
                        comission = updated_commission
                        flash(u' Comission Updated', 'flash_success')
                    if updated_bank_fee:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {pull_var: updated_bank_fee}})
                        bank_fee = updated_bank_fee
                        flash(u' Bank Fee Updated', 'flash_success')
                    if len(selected_templates_list) > 0:
                        mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {selected_templates_var: selected_templates_list}})
                        flash(u'Selected Contracts Updated', 'flash_success')


                    # -------------------- Math --------------------

                    print("yes ------------------->>  ", file=sys.stderr)

                    duration = abs((datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(expected_end_date, "%Y-%m-%d")).days)
                    expected_repayment_amount = float(advance_amount) * float(factor_rate)

                    print("yes 2 ------------------->>  ", file=sys.stderr)

                    # -----------------------------------------------

                    mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {duration_var: duration}})
                    mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {repay_var: expected_repayment_amount}})

                    print("yes contract update ------------------->>  ", file=sys.stderr)
            except:
                print("skip contract update ", file=sys.stderr)








            try:
                print("send_contract ------------------->>  ", file=sys.stderr)
                if form_data['send_contract'] == 'send_contract':
                    print("yes 3_1 ------------------->>  ", file=sys.stderr)
                    duration = abs((datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(expected_end_date, "%Y-%m-%d")).days)
                    print("yes 3 ------------------->>  ", file=sys.stderr)
                    total_commission = float(advance_amount) * 0.1
                    expected_repayment_amount = float(advance_amount) * float(factor_rate)

                    print("yes 4 ------------------->>  ", file=sys.stderr)

                    submitted_email_list = []
                    for k, v in form_data.items():
                        print(k, v)
                        if 'email_num_' in k:
                            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", v): #check if valid email
                                submitted_email_list.append(v)


                    print(submitted_email_list)


                    doc_info_list_payload = []
                    doc_ids_list = []
                    doc_list_mongo = []
                    for template_id in selected_templates:
                        for temp_info in temp_list:
                            if temp_info[0] == template_id:
                                template_name = temp_info[1]

                                print(signnow_access_token)
                                # Create a document from the template
                                print("Creating a new document from the template:")
                                doc_id = signnow_python_sdk.Template.copy(signnow_access_token, template_id, template_name)
                                print("The docments's id:", doc_id, file=sys.stderr)
                                document_data = signnow_python_sdk.Document.get(signnow_access_token, doc_id['id'])
                                document_id = document_data['id']
                                document_name = document_data['document_name']
                                print("The docments's id:", document_data['id'], file=sys.stderr)
                                print("The document's name:", document_data['document_name'], file=sys.stderr)
                                print("The document's owner:", document_data['owner'], file=sys.stderr)
                                print("The document's page_count:", document_data['page_count'], file=sys.stderr)
                                print("\n", file=sys.stderr)
                                print("The document's Roles:", document_data['roles'], file=sys.stderr)
                                print("\n", file=sys.stderr)

                                doc_info_list_payload.append([document_id, document_data['roles']])
                                doc_ids_list.append(document_id)
                                doc_list_mongo.append({"signnow_document_id": document_id, "signnow_status": 'pending', "signnow_document_name": document_name})




                                # Create the PUT /document payload
                                doc_payload = {
                                    "texts": [
                                        {
                                            "size": 12,
                                            "x": 210,
                                            "y": 179,
                                            "page_number": 0,
                                            "font": "Arial",
                                            "data": today_date,
                                            "line_height": 9.075,
                                            "client_timestamp": datetime.now().strftime("%s")
                                        },

                                        {
                                            "size": 12,
                                            "x": 450,
                                            "y": 530,
                                            "page_number": 0,
                                            "font": "Arial",
                                            "data": pull_amount,
                                            "line_height": 9.075,
                                            "client_timestamp": datetime.now().strftime("%s")
                                        }
                                    ]
                                }
                                print("Updating the document:", file=sys.stderr)
                                put_doc_response = signnow_python_sdk.Document.update(signnow_access_token, document_id, doc_payload)

                                print(put_doc_response)










                    #Create Document group

                    document_group_name = company_name + " Document Group"

                    doc_group_url = "https://api-eval.signnow.com/documentgroup"

                    doc_group_payload = {
                        "document_ids": doc_ids_list,
                        "group_name": document_group_name
                    }
                    doc_group_headers = {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + str(signnow_access_token)
                    }

                    doc_group_response = (requests.request("POST", doc_group_url, json=doc_group_payload, headers=doc_group_headers)).json()
                    print(doc_group_response)
                    doc_group_id = doc_group_response['id']

                    print('doc_group_id', doc_group_id)




                    if is_live_production_env == True:


                        invite_email_payload = []
                        for em in submitted_email_list:
                            invite_email_payload.append({
                                "email":em,
                                "subject": "Sign Docs",
                                "message": "Docs to Sign",
                                "expiration_days": 7,
                                "reminder": 3
                            })


                        invite_actions_payload = []
                        for ii in doc_info_list_payload:
                            doc_id = ii[0]
                            role_count = 0
                            for role in ii[1]:
                                name = role['name']
                                invite_actions_payload.append(
                                {"email": submitted_email_list[role_count],
                                "role_name": name,
                                "action": "sign",
                                "document_id": doc_id,
                                "allow_reassign": 1}
                                )
                                role_count += 1




                        signnow_contract_from_email = 'xxx'



                    else:

                        dev_email_list = current_app.config['EMAIL_LIST'].split(';')

                        invite_email_payload = []
                        for em in dev_email_list:
                            invite_email_payload.append({
                                "email":em,
                                "subject": "Sign Docs",
                                "message": "Docs to Sign",
                                "expiration_days": 7,
                                "reminder": 3
                            })


                        invite_actions_payload = []
                        for ii in doc_info_list_payload:
                            doc_id = ii[0]
                            role_count = 0
                            for role in ii[1]:
                                name = role['name']
                                invite_actions_payload.append(
                                {"email": dev_email_list[role_count],
                                "role_name": name,
                                "action": "sign",
                                "document_id": doc_id,
                                "allow_reassign": 0}
                                )
                                role_count += 1


                        signnow_contract_from_email = 'shaun@thisisget.com'


                    print('invite_email_payload ------> ', invite_email_payload)
                    print('invite_actions_payload ------> ', invite_actions_payload)

                    # send to document group

                    url = "https://api-eval.signnow.com/documentgroup/" + doc_group_id + "/groupinvite"

                    payload = {
                        "invite_steps": [
                            {
                                "order": 1,
                                "invite_emails": invite_email_payload,
                                "invite_actions": invite_actions_payload
                            }
                        ],
                        "cc": dev_email_list,
                        "cc_subject": "CC Subject",
                        "cc_message": "CC Message"

                    }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + str(signnow_access_token)
                    }

                    response = requests.request("POST", url, json=payload, headers=headers)

                    print(response.text)





                    print("The docments's invite has been sent", file=sys.stderr)

                    try:
                        print("The docments's STATUS:", document_data['field_invites'][0]['status'], file=sys.stderr)
                    except:
                        print("No Status yet", file=sys.stderr)




                    num_of_docs = len(doc_ids_list)
                    exact_time = datetime.today().strftime('%m/%d/%Y - %H:%M')


                    signnow_var = "cash_advance_contracts." + str(len_of_cash - 1) + ".SignNow.document_group"
                    mongoDB.Merchants.update({"company_ID": company_id_var}, {"$set": {signnow_var: {'document_group_id': doc_group_id, 'document_group_name': document_group_name, 'document_group_doc_number':num_of_docs, 'document_group_last_modified': exact_time, 'total_group_recipients' : signers_needed, 'sent_documents':doc_list_mongo}}})

                    return redirect(url_for('MCA_Prefunded.MCA_Prefunded'))

            except:
                print("skip contract send", file=sys.stderr)


    return render_template("/Funder/Advances/Pre_Funded/Edit_Contract/edit_contract.html", company_name=company_name, company_id_var=company_id_var, access_status=access_status, notification_count=notification_count, start_date=start_date, expected_end_date=expected_end_date, duration=duration, split_percent=split_percent, factor_rate=factor_rate, fico_score=fico_score, funded_via=funded_via, position=position, tags=tags, temp_list=temp_list, ACH_pull_schedule=ACH_pull_schedule, advance_amount=advance_amount, pull_amount=pull_amount, business_email=business_email, signnow_status=signnow_status, email_list=email_list, signers_needed=signers_needed)
