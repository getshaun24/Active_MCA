from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
import os
from project import db
from project.api.mail import mail
from project.api.mongo import db
import uuid
import datetime
from datetime import datetime, timedelta
import gridfs
from flask_mail import Mail
from flask_mail import Message
from project.api.models import User
from project.api.functions import generate_secure_password


New_MCA_Blueprint = Blueprint('MCA_New_MCA', __name__)
@New_MCA_Blueprint.route('/api/funder/merchants/new_mca/', methods=['GET', 'POST'])
def MCA_New_MCA():


    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    print("business_id " + session.get('business_id'))

    mongoDB = db[session.get("user_database")]

    funder_db = session.get("user_database")
    print('funder_db --------> ', funder_db, file=sys.stderr)

    company_id_var = request.args.get('company_id_var', None)

    pre_contract_info = mongoDB.Pre_Contract.find_one({"company_ID":company_id_var})
    company_DBA = pre_contract_info['company_DBA']
    ISO_document = pre_contract_info['ISO_document']
    bank_statements = pre_contract_info['bank_statements']



    ISO_names = [item['ISO_business_name'] for item in mongoDB.ISOs.find()]
    print("ISO NAMES " + str(ISO_names))


    if request.method == 'POST':


        form_data = request.form
        print(form_data, file=sys.stderr)


        print("FORM BREAKDOWN! ------------------------------>", file=sys.stderr)

        date_added = datetime.today()
        #------------ merchant info ------------

        merchant_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, (session.get("email") + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
        #company_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, form_data["businessName"] + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))).replace("-", "")
        funder = form_data["funder"]
        under_writer = form_data["under_writer"]
        ISO = form_data["ISO"]
        sales_rep = form_data["sales_rep"]
        MCC = form_data["MCC"]
        SIC = form_data["SIC"]




        #------------ company info ------------

        legal_company_name = form_data["businessName"]
        company_DBA = form_data["doingBusinessAs"]
        poc_first_name = form_data["firstName"]
        poc_last_name = form_data["lastName"]
        poc_email = form_data["email"]
        poc_phone = form_data["phone"]
        business_description = form_data["biz_desc"]
        business_type = form_data["type"]
        business_ad = form_data["address1"]
        business_city = form_data["city"]
        business_state = form_data["state"]
        business_postal = form_data["postalCode"]
        business_address = business_ad + ' ' + business_city  + ' ' + business_state + ' ' + business_postal
        business_classification = form_data["businessClassification"]
        business_type = form_data["businessType"]
        business_ein = form_data["ein"]
        business_docs = request.files["business_document"]
        business_docs_ID = 'Business_Document_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (legal_company_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

        if business_type == 'soleProprietorship':
            sole_prop_ssn = form_data['sole_p_ssn']
            sole_p_dateOfBirth = form_data['sole_p_dateOfBirth']
            print("sole_p ------------------------------>", file=sys.stderr)


        print("BIZ ------------------------------>", file=sys.stderr)


        if business_type != 'soleProprietorship':

            print("NOT SOL_P ------------------------------>", file=sys.stderr)

            # ------------- controller info --------------

            controller_firstName = form_data["controller_firstName"]
            controller_lastName = form_data["controller_lastName"]
            controller_title = form_data["title"]
            print("111 ------------------------------>", file=sys.stderr)
            controller_dateOfBirth = form_data["dateOfBirth"]
            controller_ssn = form_data["ssn"]
            controller_address = form_data["controller_address"]
            controller_city = form_data["controller_city"]
            print("222 ------------------------------>", file=sys.stderr)
            controller_stateProvinceRegion = form_data["controller_stateProvinceRegion"]
            controller_postalCode = form_data["controller_postalCode"]
            controller_country = form_data["controller_country"]
            print("333 ------------------------------>", file=sys.stderr)
            controller_docs_ID = 'Controller_Document_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (legal_company_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")
            controller_docs = request.files["controller_document"]
            print("Beneficial ------------------------------>", file=sys.stderr)

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
            beneficial_owner_docs = request.files["beneficial_owner_document"]
            beneficial_owner_docs_ID = 'Beneficial_Owner_Document_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (legal_company_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

            print("NOT Complete ------------------------------>", file=sys.stderr)




        # Now that we are adding a list of funders to each merchant db this loop is probably unnessisary

        # Loops through all databases and companies to check if the submitted EIN already exists.
        # Loop placed here so it does not include this same company that will added below

        # all_dbs = set([item['DB_name'] for item in mongoDB_master_access.master_user_list.find()])
        # all_dbs = set([item['metadata']['funder_db'] for item in db.Credentials.Users.find()])
        all_dbs = db.Credentials.Users.distinct("metadata.funder_db", {"access_status": "admin"})

        print("all_dbs ------------------------------>", all_dbs, file=sys.stderr)

        eins = []
        EIN_exists = False
        dwolla_customer_id = ''
        for database in all_dbs:
            dwolla_ids = db[database].Merchants.aggregate([{"$match": {"business_ein": business_ein}}, { "$project": {"dwolla_customer_url_id":1}}])
            for doc in dwolla_ids:
                if doc is not None:
                    EIN_exists = True
                    dwolla_customer_id = doc['dwolla_customer_url_id']
                    break


        print("Post EIN ------------------------------>", file=sys.stderr)
        #-----------------------------------------------



        if business_type == 'soleProprietorship':


            sol_prop_owner_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, (poc_first_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

            mongoDB.Merchants.insert_one({
                "date_added": date_added,
                "company_ID":company_id_var, 
                "legal_company_name":legal_company_name, 
                "company_DBA":company_DBA, 
                "business_type":business_type, 
                "business_classification":business_classification, 
                "business_type":business_type, 
                "business_ein":business_ein, 
                "business_description": business_description, 
                "business_email":poc_email, 
                "poc_first_name":poc_first_name, 
                "poc_last_name":poc_last_name, 
                "poc_email":poc_email, 
                "poc_phone":poc_phone, 
                "business_address":business_address, 
                "business_city":business_city, 
                "business_state":business_state, 
                "business_postal":business_postal, 
                "funder":funder, 
                "under_writer":under_writer, 
                "ISO":ISO, 
                "sales_rep":sales_rep, 
                "MCC":MCC, 
                "SIC":SIC, 
                "dwolla_customer_url_id": dwolla_customer_id, 
                "clear_decrypted":"-",
                "owners":[
                    {
                        "owner_ID": sol_prop_owner_ID, 
                        "owner_first_name":poc_first_name, 
                        "owner_last_name":poc_last_name, 
                        "owner_dob":sole_p_dateOfBirth, 
                        "owner_ssn":sole_prop_ssn, 
                        "owner_address":business_ad, 
                        "owner_city":business_city, 
                        "owner_state":business_state, 
                        "owner_country":'N/A',
                        "owner_postal":business_postal, 
                        "owner_docs":business_docs_ID
                    }
                ],
                "controller":[
                    {
                        "controller_firstName":poc_first_name, 
                        "controller_lastName":poc_last_name, 
                        "controller_title":"N/A", 
                        "controller_dateOfBirth":sole_p_dateOfBirth, 
                        "controller_ssn":sole_prop_ssn, 
                        "controller_address":business_ad, 
                        "controller_city":business_city, 
                        "controller_stateProvinceRegion":business_state, 
                        "controller_postalCode":business_postal, 
                        "controller_country":"N/A"
                    }
                ],
                "uploaded_documents":[
                    {
                        "business_docs": business_docs_ID, 
                        "ISO_document":ISO_document, 
                        "bank_statements":bank_statements
                    }
                ],
                "cash_advance_contracts":[],
                "plaid_access_token": '-', 
                "plaid_pull":[]
            })



            fs = gridfs.GridFS(mongoDB)
            fs.put(business_docs, filename=business_docs_ID)

            print("Company_table inserted", file=sys.stderr)


        else:


            print("Pre COMPANY ------------------------------>", file=sys.stderr)

            mongoDB.Merchants.insert_one({
                "date_added": date_added,
                "company_ID":company_id_var, 
                "legal_company_name":legal_company_name, 
                "company_DBA":company_DBA, 
                "business_type":business_type, 
                "business_classification":business_classification, 
                "business_type":business_type, 
                "business_description": business_description, 
                "business_ein":business_ein, 
                "business_email":poc_email, 
                "poc_first_name":poc_first_name, 
                "poc_last_name":poc_last_name, 
                "poc_email":poc_email, 
                "poc_phone":poc_phone, 
                "business_address":business_address, 
                "business_city":business_city, 
                "business_state":business_state, 
                "business_postal":business_postal, 
                "funder":funder, 
                "under_writer":under_writer, 
                "ISO":ISO, 
                "sales_rep":sales_rep, 
                "MCC":MCC, 
                "SIC":SIC, 
                "dwolla_customer_url_id": dwolla_customer_id, 
                "clear_decrypted":"-",
                "owners":[
                    {
                        "owner_ID": beneficial_owner_ID, 
                        "owner_first_name":beneficial_owner_firstName, 
                        "owner_last_name":beneficial_owner_lastName, 
                        "owner_dob":beneficial_owner_dateOfBirth, 
                        "owner_ssn":beneficial_owner_ssn, 
                        "owner_address":beneficial_owner_address, 
                        "owner_city":beneficial_owner_city, 
                        "owner_state":beneficial_owner_stateProvinceRegion, 
                        "owner_country":beneficial_owner_country, 
                        "owner_postal":beneficial_owner_postalCode
                    }
                ],
                "controller":[
                    {
                        "controller_firstName":controller_firstName, 
                        "controller_lastName":controller_lastName, 
                        "controller_title":controller_title, 
                        "controller_dateOfBirth":controller_dateOfBirth, 
                        "controller_ssn":controller_ssn, 
                        "controller_address":controller_address, 
                        "controller_city":controller_city, 
                        "controller_stateProvinceRegion":controller_stateProvinceRegion, 
                        "controller_postalCode":controller_postalCode, 
                        "controller_country":controller_country
                        }
                    ],
                "uploaded_documents":[
                    {
                        "business_docs": business_docs_ID, 
                        "controller_docs": controller_docs_ID, 
                        "beneficial_owner_docs": beneficial_owner_docs_ID, 
                        "ISO_document":ISO_document, 
                        "bank_statements":bank_statements
                    }
                ],
                "cash_advance_contracts":[], 
                "plaid_access_token": '', 
                "plaid_pull":[]
            })



            fs = gridfs.GridFS(mongoDB)
            try:
                fs.put(business_docs, filename=business_docs_ID)
            except:
                print("No Business Docs", file=sys.stderr)
            try:
                fs.put(controller_docs, filename=controller_docs_ID)
            except:
                print("No Controller Docs", file=sys.stderr)
            try:
                fs.put(beneficial_owner_docs, filename=beneficial_owner_docs_ID)
            except:
                print("No Owner Docs", file=sys.stderr)

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
                beneficial_owner_docs_2 = request.files["beneficial_owner_document_2"]
                beneficial_owner_docs_ID_2 = 'Beneficial_Owner_Document_2_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (beneficial_owner_firstName_2 + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
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

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
                    "uploaded_documents": {
                        "beneficial_owner_docs_2": beneficial_owner_docs_ID_2
                    }
                }})

                fs.put(beneficial_owner_docs_2, filename=beneficial_owner_docs_ID_2)

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
                beneficial_owner_docs_3 = request.files["beneficial_owner_document_3"]
                beneficial_owner_docs_ID_3 = 'Beneficial_Owner_Document_3_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (beneficial_owner_firstName_3 + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
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

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
                    "uploaded_documents":{
                        "beneficial_owner_docs_3": beneficial_owner_docs_ID_3
                    }
                }})

                fs.put(beneficial_owner_docs_3, filename=beneficial_owner_docs_ID_3)

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
                beneficial_owner_docs_4 = request.files["beneficial_owner_document_4"]
                beneficial_owner_docs_ID_4 = 'Beneficial_Owner_Document_4_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (beneficial_owner_firstName_4 + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")


                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
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

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
                    "uploaded_documents":{
                        "beneficial_owner_docs_4": beneficial_owner_docs_ID_4
                    }
                }})

                fs.put(beneficial_owner_docs_4, filename=beneficial_owner_docs_ID_4)

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
                beneficial_owner_docs_5 = request.files["beneficial_owner_document_5"]
                beneficial_owner_docs_ID_5 = 'Beneficial_Owner_Document_5_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (beneficial_owner_firstName_5 + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
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

                mongoDB.Company.update({"company_ID": company_id_var}, {"$push": {
                    "uploaded_documents":{
                        "beneficial_owner_docs_5": beneficial_owner_docs_ID_5
                    }
                }})

                fs.put(beneficial_owner_docs_5, filename=beneficial_owner_docs_ID_5)

            except:
                print('No Benefical Owner #5', file=sys.stderr)



        # Now that we have added the merchant to the funder database, we want to see if that user exists (by email and company id)
        # If it does then we add the funder db to the user profile and send them an email that they were signe up otherwise we create 
        # a new user and add it to the users collection and then send them a secure link to sign in.


        userExists = False
        users = db.Credentials.Users.aggregate([{"$match": {"email": poc_email, "business_id": company_id_var}}, { "$project": {"email":1}}])
        if len(list(users)) != 0:
            userExists = True

        email_recipients = current_app.config['EMAIL_LIST'].split(';')

        if current_app.config['ENV'] == 'production':
            email_recipients = [poc_email]

        if userExists and EIN_exists and dwolla_customer_id != '':
            # Add funder db to metadata if it does not exist and send end secure login email
            print("USER EXISTS")
            funderExists = db.Credentials.Users.find({"email": poc_email, "business_id": company_id_var, "access_status": "merchant"}, {"metadata.funder_dbs": {"$in": [session.get("user_database")]}}).count()
            if funderExists == 0:
                db.Credentials.Users.update({"email": poc_email, "business_id": company_id_var, "access_status": "merchant"}, {"$push": {"metadata.funder_dbs": session.get('user_database')}})
            msg = Message(
                sender="getresources@fastmail.com",
                recipients=email_recipients,
                subject="secure-bank",
                body=current_app.config['APP_URL'] + "/Merchant/Secure_Bank/Secure_Login/?mid=" + company_id_var + "&fid=" + session.get('business_id')
            )
            mail.send(msg)

        elif not userExists:
            # Create user with temporary password and end secure login email
            print("USER DOES NOT EXIST")
            passwordGenerator = generate_secure_password()
            # db.Credentials.Users.update({"email": poc_email}, {"$set": {"password": hashed_password}})
            db.Credentials.Users.insert_one({
                "date_added": date_added,
                "email": poc_email, 
                "password": passwordGenerator['hashed'], # create one
                "access_status": "merchant",
                "reset_code": "",
                "two_factor_code": "",
                "first_name": poc_first_name,
                "last_name": poc_last_name,
                "notification_count": 0,
                "notfications": [],
                "metadata": {
                    "funder_dbs": [session.get('user_database')]
                },
                "business_id": company_id_var
            })

            # newUser = User(email=poc_email, db=db)
            # userPass = newUser.generate_and_update_password(db=db)

            # Get business name
            businessName = db.Master.Funders.find_one({"company_ID": session.get('business_id')},{"legal_company_name":1})['legal_company_name']

            body = "Welcome to Active MCA!\n\n"
            body += "Please click the link below to complete your account set up with " + businessName + ". \n\n"
                

            if EIN_exists and dwolla_customer_id != '':
                print("EIN EXISTS")
                body += "Your password is " + passwordGenerator['password'] + " \n\n"
                body += current_app.config['APP_URL'] + "/Merchant/Secure_Bank/Secure_Login/?mid=" + company_id_var + "&fid=" + session.get('business_id')
            
            if not EIN_exists or dwolla_customer_id == '':
                print("EIN DOES NOT EXIST")

                body += current_app.config['APP_URL'] + "/Merchant/Secure_Bank/Secure_Register/?mid=" + company_id_var + "&fid=" + session.get('business_id')
            
            msg = Message(
                sender="getresources@fastmail.com",
                recipients=email_recipients,
                subject="secure-bank",
                body=body
            )
            mail.send(msg)
            print("EMAIL SENT")


        mongoDB.Pre_Contract.update({"company_ID": company_id_var}, {"$set": {"status":"Pending"}})


        print('should redirect')
        return redirect(url_for('MCA_Prefunded.MCA_Prefunded'))



    return render_template("/Funder/Merchants/New_MCA/new_mca.html", access_status=session.get('access_status'), notification_count=session.get('notification_count'), ISO_names=ISO_names, company_id_var=company_id_var, company_DBA=company_DBA)
