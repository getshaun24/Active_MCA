from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
from project.api.dwolla import dwolla_app_token
from project.api.mail import mail
from project import db
import datetime
from datetime import datetime, timedelta
import dwollav2
import uuid
from flask_mail import Mail
from flask_mail import Message


Funder_Sign_Up_Blueprint = Blueprint('MCA_Funder_Sign_Up', __name__)
@Funder_Sign_Up_Blueprint.route('/api/master/funder_sign_up/', methods=['GET', 'POST']) 
def MCA_Funder_Sign_Up():


    if session.get("access_status") != "master":
        return redirect(url_for('logout'))


    mongoDB = db.Master


    if request.method == 'POST':

        date_added = datetime.today().strftime('%m/%d/%Y')

        form_data = request.form
        print(form_data, file=sys.stderr)



        #------------ company info ------------

        company_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, form_data["businessName"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))).replace("-", "")
        legal_company_name = form_data["businessName"]
        company_DBA = form_data["doingBusinessAs"]
        poc_first_name = form_data["firstName"]
        poc_last_name = form_data["lastName"]
        poc_email = form_data["email"]
        poc_phone = form_data["phone"]
        business_description = form_data["biz_desc"]
        # business_type = form_data["type"] - Not used
        business_address = form_data["address1"] + ' ' + form_data["city"] + ' ' + form_data["state"] + ' ' + form_data["postalCode"]
        business_classification = form_data["businessClassification"]
        business_type = form_data["businessType"]
        business_ein = form_data["ein"]


        # ------------- controller info --------------

        # These variables are not used. Could probably remove them.

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



        #------------ Beneficial Owner info ------------

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




        #-----------------------------------------------
        #-------------------- Dwolla --------------------

        """ 
        Adding steps to make sense of this
        1. Create a customer
        2. Check that the customer status is 'document'
        3. If so, add business and controller docs to customer
        4. Add beneficial owner to customer
        5. Certify beneficial ownership
        """


        # Using dwollav2 - https://github.com/Dwolla/dwolla-v2-python (Recommended)
        request_body = {
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
            }
        }


        # Apparently we are not supposed to do this until we get approval from the user. I would think that by them doing this
        # approval/permission would be implied.

        customer = dwolla_app_token.post('customers', request_body)
        customer_url = customer.headers['location']
        # This might break once we go to production because the URL might be different. I think we should just 
        # split by '/' to be safe
        # dwolla_customer_id = customer_url[41:]
        # 'https://api-sandbox.dwolla.com/customers/62c3aa1b-3a1b-46d0-ae90-17304d60c3d5'
        dwolla_customer_id = customer_url.split('/')[-1]
        print ('fu1l id ----------------------------------------------------->>',dwolla_customer_id, file=sys.stderr)



        customer = dwolla_app_token.get(customer_url)
        customer_status = customer.body['status']

        #print (request.files["business_document"], file=sys.stderr)
        #print (request.files["controller_document"], file=sys.stderr)


        print(customer_status, file=sys.stderr)

        # Why are we making the assumption that the customer status will be "document" instead of say "unverified"? 
        # Because they are an llc or something? Does this mean they need to submit docs to be verified?

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

        beneficial_owner = dwolla_app_token.post('%s/beneficial-owners' % customer_url, request_body_beneficial_owner)
        beneficial_owner_url = beneficial_owner.headers['location']
        beneficial_owner = dwolla_app_token.get(beneficial_owner_url)
        try:
            beneficial_status = beneficial_owner.body['status']
            print(beneficial_status, file=sys.stderr)
        except:
            print('no beneficial status', file=sys.stderr)


        print("certify =======================================================================", file=sys.stderr)


        request_body = {
            "status": "certified"
            }

        dwolla_app_token.post('%s/beneficial-ownership' % customer_url, request_body)


        print("certified =======================================================================", file=sys.stderr)



        business_docs = request.files["business_document"]
        business_docs_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, (form_data["businessName"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")


        print("email start ========================================>>>>>>>>>>>>", file=sys.stderr)


        # Wonder if we should and an expiration for this link
        # body_link = current_app.config['APP_URL'] + "/Active_MCA_Master/Master_Plaid_Confirm/?secure_id=" + dwolla_customer_id + "___" + company_ID
        body_link = current_app.config['APP_URL'] + "/Active_MCA_Master/Master_Plaid_Confirm/?secure_id=" + company_ID

        if current_app.config['ENV'] != 'production':
            recipients = current_app.config['DWOLLA_MASTER_RECIPIENTS'].split(';')
        else:
            recipients = form_data["email"]

        msg = Message(sender="getresources@fastmail.com",
            recipients=recipients,  #[form_data["email"]])
            subject="secure-bank",
            body= body_link
        )
        mail.send(msg)


        print("email sent ========================================>>>>>>>>>>>>", file=sys.stderr)

        legal_company_name_formatted = (legal_company_name).replace(" ", "_").replace("'", "").replace("-", "_").replace("&", "_")
        db_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, (legal_company_name_formatted + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
        DB_company_name = "Funder_" + legal_company_name_formatted + "_" + db_uuid[:5]

        mongoDB.Funders.insert_one({
            "date_added": date_added,
            "company_ID":company_ID, 
            "legal_company_name":legal_company_name, 
            "funder_db_name": DB_company_name,
            "company_DBA":company_DBA, 
            "business_type":business_type, 
            "business_address":business_address, 
            "business_classification":business_classification, 
            "business_type":business_type, 
            "business_ein":business_ein, 
            "business_email":poc_email, 
            "poc_first_name":poc_first_name, 
            "poc_last_name":poc_last_name, 
            "poc_email":poc_email, 
            "poc_phone":poc_phone, 
            "business_description": business_description, 
            "dwolla_customer_url_id": dwolla_customer_id,
            "owners":[{
                "owner_ID": beneficial_owner_ID, 
                "owner_first_name":beneficial_owner_firstName, 
                "owner_last_name":beneficial_owner_lastName, 
                "owner_dob":beneficial_owner_dateOfBirth, 
                "owner_ssn":beneficial_owner_ssn, 
                "owner_address":beneficial_owner_address, 
                "owner_city":beneficial_owner_city, 
                "owner_state":beneficial_owner_stateProvinceRegion, 
                "owner_country":beneficial_owner_country, 
                "owner_postal":beneficial_owner_postalCode, 
                "owner_docs":business_docs_ID
            }], 
            "plaid_pull":[],
            "plaid_access_token": "",
            "dwolla_funding_source_destination_account": "",
            "selected_account_ID": "",
            "dwolla_funding_source_active_pay_account": "",
            "selected_active_pay_account_ID": "" 
        })

        print("Company_table inserted", file=sys.stderr)



        # for additional beneficial owners
        try:
            beneficial_owner_ID_2 = str(uuid.uuid5(uuid.NAMESPACE_DNS, (form_data["beneficial_owner_firstName_2"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
            beneficial_owner_firstName_2 = form_data["beneficial_owner_firstName_2"]
            beneficial_owner_lastName_2 = form_data["beneficial_owner_lastName_2"]
            beneficial_owner_dateOfBirth_2 = form_data["beneficial_owner_dateOfBirth_2"]
            beneficial_owner_ssn_2 = form_data["beneficial_owner_ssn_2"]
            beneficial_owner_address_2 = form_data["beneficial_owner_address_2"]
            beneficial_owner_city_2 = form_data["beneficial_owner_city_2"]
            beneficial_owner_stateProvinceRegion_2 = form_data["beneficial_owner_stateProvinceRegion_2"]
            beneficial_owner_country_2 = form_data["beneficial_owner_country_2"]
            beneficial_owner_postalCode_2 = form_data["beneficial_owner_postalCode_2"]

            mongoDB.Funders.update({"company_ID": company_ID},{"$push": {
                "owners": {
                    "owner_ID": beneficial_owner_ID_2, 
                    "owner_first_name":beneficial_owner_firstName_2, 
                    "owner_last_name":beneficial_owner_lastName_2, 
                    "owner_dob":beneficial_owner_dateOfBirth_2, 
                    "owner_ssn":beneficial_owner_ssn_2, 
                    "owner_address":beneficial_owner_address_2, 
                    "owner_city":beneficial_owner_city_2, 
                    "owner_state":beneficial_owner_stateProvinceRegion_2, 
                    "owner_country":beneficial_owner_country_2, 
                    "owner_postal":beneficial_owner_postalCode_2
                }
            }});

        except:
            print('No Benefical Owner #2', file=sys.stderr)
        try:
            beneficial_owner_ID_3 = str(uuid.uuid5(uuid.NAMESPACE_DNS, (form_data["beneficial_owner_firstName_3"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
            beneficial_owner_firstName_3 = form_data["beneficial_owner_firstName_3"]
            beneficial_owner_lastName_3 = form_data["beneficial_owner_lastName_3"]
            beneficial_owner_dateOfBirth_3 = form_data["beneficial_owner_dateOfBirth_3"]
            beneficial_owner_ssn_3 = form_data["beneficial_owner_ssn_3"]
            beneficial_owner_address_3 = form_data["beneficial_owner_address_3"]
            beneficial_owner_city_3 = form_data["beneficial_owner_city_3"]
            beneficial_owner_stateProvinceRegion_3 = form_data["beneficial_owner_stateProvinceRegion_3"]
            beneficial_owner_country_3 = form_data["beneficial_owner_country_3"]
            beneficial_owner_postalCode_3 = form_data["beneficial_owner_postalCode_3"]

            mongoDB.Funders.update({"company_ID": company_ID}, {"$push": {
                "owners": {
                    "owner_ID": beneficial_owner_ID_3, 
                    "owner_first_name":beneficial_owner_firstName_3, 
                    "owner_last_name":beneficial_owner_lastName_3, 
                    "owner_dob":beneficial_owner_dateOfBirth_3, 
                    "owner_ssn":beneficial_owner_ssn_3, 
                    "owner_address":beneficial_owner_address_3, 
                    "owner_city":beneficial_owner_city_3, 
                    "owner_state":beneficial_owner_stateProvinceRegion_3, 
                    "owner_country":beneficial_owner_country_3, 
                    "owner_postal":beneficial_owner_postalCode_3
                }
            }});

        except:
            print('No Benefical Owner #3', file=sys.stderr)
        try:
            beneficial_owner_ID_4 = str(uuid.uuid5(uuid.NAMESPACE_DNS, (form_data["beneficial_owner_firstName_4"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
            beneficial_owner_firstName_4 = form_data["beneficial_owner_firstName_4"]
            beneficial_owner_lastName_4 = form_data["beneficial_owner_lastName_4"]
            beneficial_owner_dateOfBirth_4 = form_data["beneficial_owner_dateOfBirth_4"]
            beneficial_owner_ssn_4 = form_data["beneficial_owner_ssn_4"]
            beneficial_owner_address_4 = form_data["beneficial_owner_address_4"]
            beneficial_owner_city_4 = form_data["beneficial_owner_city_4"]
            beneficial_owner_stateProvinceRegion_4 = form_data["beneficial_owner_stateProvinceRegion_4"]
            beneficial_owner_country_4 = form_data["beneficial_owner_country_4"]
            beneficial_owner_postalCode_4 = form_data["beneficial_owner_postalCode_4"]

            mongoDB.Funders.update({"company_ID": company_ID}, {"$push": {
                "owners": {
                    "owner_ID": beneficial_owner_ID_4, 
                    "owner_first_name":beneficial_owner_firstName_4, 
                    "owner_last_name":beneficial_owner_lastName_4, 
                    "owner_dob":beneficial_owner_dateOfBirth_4, 
                    "owner_ssn":beneficial_owner_ssn_4, 
                    "owner_address":beneficial_owner_address_4, 
                    "owner_city":beneficial_owner_city_4, 
                    "owner_state":beneficial_owner_stateProvinceRegion_4, 
                    "owner_country":beneficial_owner_country_4, 
                    "owner_postal":beneficial_owner_postalCode_4
                }
            }});

        except:
            print('No Benefical Owner #4', file=sys.stderr)
        try:
            beneficial_owner_ID_5 = str(uuid.uuid5(uuid.NAMESPACE_DNS, (form_data["beneficial_owner_firstName_5"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
            beneficial_owner_firstName_5 = form_data["beneficial_owner_firstName_5"]
            beneficial_owner_lastName_5 = form_data["beneficial_owner_lastName_5"]
            beneficial_owner_dateOfBirth_5 = form_data["beneficial_owner_dateOfBirth_5"]
            beneficial_owner_ssn_5 = form_data["beneficial_owner_ssn_5"]
            beneficial_owner_address_5 = form_data["beneficial_owner_address_5"]
            beneficial_owner_city_5 = form_data["beneficial_owner_city_5"]
            beneficial_owner_stateProvinceRegion_5 = form_data["beneficial_owner_stateProvinceRegion_5"]
            beneficial_owner_country_5 = form_data["beneficial_owner_country_5"]
            beneficial_owner_postalCode_5 = form_data["beneficial_owner_postalCode_5"]

            mongoDB.Funders.update({"company_ID": company_ID}, {"$push": {
                "owners": {
                    "owner_ID": beneficial_owner_ID_5, 
                    "owner_first_name":beneficial_owner_firstName_5, 
                    "owner_last_name":beneficial_owner_lastName_5, 
                    "owner_dob":beneficial_owner_dateOfBirth_5, 
                    "owner_ssn":beneficial_owner_ssn_5, 
                    "owner_address":beneficial_owner_address_5, 
                    "owner_city":beneficial_owner_city_5, 
                    "owner_state":beneficial_owner_stateProvinceRegion_5, 
                    "owner_country":beneficial_owner_country_5, 
                    "owner_postal":beneficial_owner_postalCode_5
                }
            }});

        except:
            print('No Benefical Owner #5', file=sys.stderr)

    # Should we also create users at the same time?

    # Could have a popup that says that the funder was successfully signed up or not.

    return render_template("/Active_MCA_Master/Funder_Sign_Up/funder_sign_up.html")
