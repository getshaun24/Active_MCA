from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
from flask_login import login_required
import uuid
import datetime
from project.api.dwolla import dwolla_app_token


KYC_Update_Blueprint = Blueprint('MCA_KYC_Update', __name__)
@KYC_Update_Blueprint.route('/api/funder/merchants/merchant_details/kyc_update/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_KYC_Update():



    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    else:

        mongoDB = db[session.get("user_database")]

        company_id_var = request.args.get('mid', None)
        company_info = mongoDB.Merchants.find_one({"company_ID": company_id_var})
        company_DBA = company_info['company_DBA']


        dwolla_customer_url_id = company_info['dwolla_customer_url_id']

        customer_url = 'https://api-sandbox.dwolla.com/customers/' + dwolla_customer_url_id


        if request.method == 'POST':

            form_data = request.form
            print(form_data, file=sys.stderr)

            #------------ company info ------------

            try:
                #company_ID = company_ID # declared under merchant info
                legal_company_name = form_data["businessName"]
                company_DBA = form_data["doingBusinessAs"]
                poc_first_name = form_data["firstName"]
                poc_last_name = form_data["lastName"]
                poc_email = form_data["email"]
                poc_phone = form_data["phone"]
                business_description = form_data["biz_desc"]
                business_type = form_data["type"]
                business_address = form_data["address1"] + ' ' + form_data["city"] + ' ' + form_data["state"] + ' ' + form_data["postalCode"]
                business_classification = form_data["businessClassification"]
                business_type = form_data["businessType"]
                business_ein = form_data["ein"]


             # ------------- controller info --------------

                controller_firstName = form_data["controller_firstName"]
                controller_lastName = form_data["controller_lastName"]
                controller_title = form_data["title"]
                controller_dateOfBirth = form_data["dateOfBirth"]
                controller_ssn = form_data["ssn"]
                controller_address = form_data["controller_address"]
                controller_city = form_data["controller_city"]
                controller_stateProvinceRegion = form_data["controller_stateProvinceRegion"]
                controller_postalCode = form_data["controller_postalCode"]
                controller_country = form_data["controller_country"]
            except:
                print('skip')



            #------------ Beneficial Owner info ------------

            try:
                beneficial_owner_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, (form_data["beneficial_owner_firstName"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
                beneficial_owner_firstName = form_data["beneficial_owner_firstName"]
                beneficial_owner_lastName = form_data["beneficial_owner_lastName"]
                beneficial_owner_dateOfBirth = form_data["beneficial_owner_dateOfBirth"]
                beneficial_owner_ssn = form_data["beneficial_owner_ssn"]
                beneficial_owner_address = form_data["beneficial_owner_address"]
                beneficial_owner_city = form_data["beneficial_owner_city"]
                beneficial_owner_stateProvinceRegion = form_data["beneficial_owner_stateProvinceRegion"]
                beneficial_owner_country = form_data["beneficial_owner_country"]
                beneficial_owner_postalCode = form_data["beneficial_owner_postalCode"]
            except:
                print('skip')




            try:
                # Using dwollav2 - https://github.com/Dwolla/dwolla-v2-python (Recommended)
                customer_request_body = {
                    'firstName': form_data["firstName"],
                    'lastName': form_data["lastName"],
                    'email': form_data["email"],
                    'type': form_data["type"],
                    'address1': form_data["address1"],
                    'city': form_data["city"],
                    'state': form_data["state"],
                    'postalCode': form_data["postalCode"],
                    'businessClassification': form_data["businessClassification"],
                    'businessType': form_data["businessType"],
                    'businessName': form_data["businessName"],
                    'doingBusinessAs': form_data["doingBusinessAs"],
                    'ein': form_data["ein"],
                    'controller': {
                        'firstName': form_data["controller_firstName"],
                        'lastName': form_data["controller_lastName"],
                        'title': form_data["title"],
                        'dateOfBirth': form_data["dateOfBirth"],
                        'ssn': form_data["ssn"],
                        'address': {
                            'address1': form_data["controller_address"],
                            'city': form_data["controller_city"],
                            'stateProvinceRegion': form_data["controller_stateProvinceRegion"],
                            'postalCode': form_data["controller_postalCode"],
                            'country': form_data["controller_country"],
                                    }
                                },
                        }

                customer = dwolla_app_token.post('customers', customer_request_body)
                customer_url = customer.headers['location']
                customer_id = customer_url[41:]
                print ('fu1l id ----------------------------------------------------->>',customer_id, file=sys.stderr)

                customer = dwolla_app_token.get(customer_url)
                customer_status = customer.body['status']
                print(customer_status, file=sys.stderr)

            except:
                print('skip')


            print("222  =======================================================================", file=sys.stderr)



            try:
                if customer_status == 'document':
                    business_docs = request.files["business_document"]
                    controller_docs = request.files["controller_document"]
                    print (business_docs, file=sys.stderr)
                    print (controller_docs, file=sys.stderr)
                    document_1 = dwolla_app_token.post('%s/documents' % customer_url + '/documents', file = business_docs, documentType = 'other')
                    document_2 = dwolla_app_token.post('%s/documents' % customer_url + '/documents', file = controller_docs, documentType = 'license')
                    document_url_1 = document_1.headers['location'] # => 'https://api.dwolla.com/documents/11fe0bab-39bd-42ee-bb39-275afcc050d0'
                    document_url_2 = document_2.headers['location'] # => 'https://api.dwolla.com/documents/11fe0bab-39bd-42ee-bb39-275afcc050d0'

                    print(document_url_1, file=sys.stderr)
                    print(document_url_2, file=sys.stderr)

                    documents_1 = dwolla_app_token.get(document_url_1)
                    documents_1.body['failureReason'] # => 'ScanNotReadable'
                    documents_2 = dwolla_app_token.get(document_url_2)
                    documents_2.body['failureReason'] # => 'ScanNotReadable'

                    print(documents_1, file=sys.stderr)
                    print(documents_2, file=sys.stderr)
            except:
                print('skip')


            try:
                request_body_beneficial_owner = {
                    'firstName': form_data["beneficial_owner_firstName"],
                    'lastName': form_data["beneficial_owner_lastName"],
                    'dateOfBirth': form_data["beneficial_owner_dateOfBirth"],
                    'ssn': form_data["beneficial_owner_ssn"],
                    'address': {
                        'address1': form_data["beneficial_owner_address"],
                        'city': form_data["beneficial_owner_city"],
                        'stateProvinceRegion': form_data["beneficial_owner_stateProvinceRegion"],
                        'country': form_data["beneficial_owner_country"],
                        'postalCode': form_data["beneficial_owner_postalCode"],
                        }
                    }

                print(request_body_beneficial_owner, file=sys.stderr)

                customer_url = 'https://api-sandbox.dwolla.com/customers/' + dwolla_customer_url_id
                beneficial_owners = dwolla_app_token.get('%s/beneficial-owners' % customer_url)
                beneficial_owner_url = beneficial_owners.body['_embedded']['beneficial-owners'][0]['_links']['self']['href']
                print("beneficial_owner_url =======================================================================", beneficial_owner_url, file=sys.stderr)
                update_beneficial_owner = dwolla_app_token.post(beneficial_owner_url, request_body_beneficial_owner)

                try:
                    beneficial_status = update_beneficial_owner.body['status']
                    print(beneficial_status, file=sys.stderr)
                except:
                    print('no beneficial status', file=sys.stderr)


                print("certify =======================================================================", file=sys.stderr)


                request_body_certify = {
                    "status": "certified"
                    }

                dwolla_app_token.post('%s/beneficial-ownership' % customer_url, request_body_certify)


                print("certified =======================================================================", file=sys.stderr)

            except:
                print('skip')


    return render_template("/Funder/Merchants/Merchant_Details/KYC_Update/kyc_update.html", mid=company_id_var, company_DBA=company_DBA, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
