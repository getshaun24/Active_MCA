from flask import Blueprint, session, url_for, request, redirect, render_template, current_app
from flask_session import Session
import pymongo
import sys
# from server import mongo_client, mongoDB_master_access
from project import db
import dwollav2
from project.api.dwolla import dwolla_app_token
from flask import flash
import flask_login
from project.api.models import User
import bcrypt
from project.api.plaid import plaid_client


Secure_Register_Blueprint = Blueprint('MCA_Secure_Register', __name__)
@Secure_Register_Blueprint.route('/api/merchant/plaid/secure_register/', methods=['GET', 'POST']) # <- from '/'
def MCA_Secure_Register():


    
    funder_id = request.args.get('fid', None)
    merchant_id = request.args.get('mid', None)
    print('Merchant ID: ', merchant_id)
    print('Funder ID: ', funder_id)

    if funder_id is None or merchant_id is None:
        flash(u'The link appears to be broken.', 'flash_error')

    if request.method == 'POST':


        form_data = request.form
        print('form_data form_data form_data ---------------------------------------------->', form_data, file=sys.stderr)


        access_status = "merchant"
        email = form_data["email"]
        password_1 = form_data["password_1"]
        password_2 = form_data["password_2"]

        print('email email email---------------------------------------------->', email, file=sys.stderr)

        # Make sure form data is good
        funder_doc = db.Master.Funders.find_one({"company_ID": funder_id})
        print(funder_doc)
        if funder_doc is None:
            raise Exception('Funder does not exist.')

        funder_db_name = funder_doc["funder_db_name"]

        user = db.Credentials.Users.find_one({"email": email, "access_status": access_status, "metadata.funder_dbs": { "$in": [funder_db_name]}})
        if user is None:
            flash(u'Your email has not been registered by the funder.', 'flash_error')
            print('Email not in users collection. -------------------------------------->', file=sys.stderr)

        elif password_1 != password_2:
            flash(u'Passwords Do Not Match', 'flash_error')
            print('Passwords Do Not Match ---------------------------------------------->', file=sys.stderr)

        else:
            # Let's do a number of things:
            # 1. Verify that the user has access to the funder db
            # 2. Verify that the user business_id and the merchant id in the link match 
            # (this is so that another merchant using the same funder does not set up the wrong account)
            # 3. Verify that merchant company id exists in the merchant table in the funder db based on the mid in the link
            # and that it matches the user business id.
            # 4. If all of these things work then update password and proceed. We don't want someone to be able to update a 
            # password for another user. This would be a security risk.

            # 1. Verify that the user has access to the funder db
            # funder_doc = db.Master.Funders.find_one({"company_ID": funder_id})
            # print(funder_doc)
            # if funder_doc is None:
            #     raise Exception('Funder does not exist.')

            # funder_db_name = funder_doc["funder_db_name"]

            # funder_db_match = False
            # for f_db in user['metadata']['funder_dbs']:
            #     if f_db == funder_db_name:
            #         funder_db_match = True
            #         break
            # if funder_db_match is False:
            #     flash(u'This user does not have access to funder information.', 'flash_error')

            # 2. Verify that the user business_id and the merchant id in the link match 
            if user['business_id'] != merchant_id:
                flash(u'The user business id and the merchant id do not match.', 'flash_error')

            # 3. Verify that merchant company id exists in the merchant table in the funder db based on the mid in the link
            # and that it matches the user business id.
            mongoDB = db[funder_db_name]
            company_info = mongoDB.Merchants.find_one({"company_ID": merchant_id})
            if company_info['company_ID'] != user['business_id']:
                flash(u'This user business id does not match the merchant id in the funder records.', 'flash_error')

            # 4. If all of these things work then update password and proceed.
            user = User(email=email, db=db)
            hashed = bcrypt.hashpw(password_1.encode('utf8'), bcrypt.gensalt(14))
            user.update_password(password=hashed, db=db)
        

            # Let's check if this merchant has already registered an account with dwolla
            
            dwolla_exists = True
            dwolla_id = company_info['dwolla_customer_url_id']
            try:
                dwolla_customer = dwolla_app_token.get(current_app.config['DWOLLA_APP_URL'] + '/customers/' + dwolla_id).body['firstName']
                print(dwolla_customer)
            except:
                dwolla_exists = False
            
            print("Dwolla_exists: ------------> ", dwolla_exists)

            company_ID = company_info['company_ID']
            legal_company_name = company_info['legal_company_name']
            company_DBA = company_info['company_DBA']
            poc_first_name = company_info['poc_first_name']
            poc_last_name = company_info['poc_last_name']
            poc_email = company_info['poc_email']
            poc_phone = company_info['poc_phone']
            business_type = company_info['business_type']
            business_classification = company_info['business_classification']
            business_ein = company_info['business_ein']
            business_address = company_info["business_address"]
            business_city = company_info["business_city"]
            business_state = company_info["business_state"]
            business_postal = company_info["business_postal"]

            owner_first_name = company_info['owners'][0]['owner_first_name']
            owner_last_name = company_info['owners'][0]['owner_last_name']
            owner_dob = company_info['owners'][0]['owner_dob']
            owner_ssn = company_info['owners'][0]['owner_ssn']
            owner_address = company_info['owners'][0]['owner_address']
            owner_city = company_info['owners'][0]['owner_city']
            owner_state = company_info['owners'][0]['owner_state']
            owner_country = company_info['owners'][0]['owner_country']
            owner_postal = company_info['owners'][0]['owner_postal']
            controller_firstName = company_info['controller'][0]['controller_firstName']
            controller_lastName = company_info['controller'][0]['controller_lastName']
            controller_title = company_info['controller'][0]['controller_title']
            controller_dateOfBirth = company_info['controller'][0]['controller_dateOfBirth']
            controller_ssn = company_info['controller'][0]['controller_ssn']
            controller_address = company_info['controller'][0]['controller_address']
            controller_city = company_info['controller'][0]['controller_city']
            controller_stateProvinceRegion = company_info['controller'][0]['controller_stateProvinceRegion']
            controller_postalCode = company_info['controller'][0]['controller_postalCode']
            controller_country = company_info['controller'][0]['controller_country']


            if business_type == 'soleProprietorship' and not dwolla_exists:

                print(poc_email)
                request_body = {
                    'firstName': poc_first_name,
                    'lastName': poc_last_name,
                    'email': poc_email, #should we rather have business email here ???
                    'type': 'business',
                    'dateOfBirth': owner_dob,
                    'ssn': owner_ssn,
                    'address1': business_address,
                    'city': business_city,
                    'state': business_state,
                    'postalCode': business_postal,
                    'businessClassification': business_classification,
                    'businessType': business_type,
                    'businessName': legal_company_name,
                    'ein': business_ein
                }



                customer = dwolla_app_token.post('customers', request_body)
                customer_url = customer.headers['location']
                dwolla_id = customer_url.split('/')[-1]
                print ('fu1l id ----------------------------------------------------->>',dwolla_id, file=sys.stderr)

                mongoDB.Merchants.update({"company_ID": company_ID}, {"$set": {"dwolla_customer_url_id": dwolla_id}});


            elif not dwolla_exists:

                # Using dwollav2 - https://github.com/Dwolla/dwolla-v2-python (Recommended)
                request_body = {
                    'firstName': poc_first_name,
                    'lastName': poc_last_name,
                    'email': poc_email,  #should we rather have business email here ???
                    'type': 'business',
                    'address1': business_address,
                    'city': business_city,
                    'state': business_state,
                    'postalCode': business_postal,
                    'businessClassification': business_classification,
                    'businessType': business_type,
                    'businessName': legal_company_name,
                    'doingBusinessAs': company_DBA,
                    'ein': business_ein,
                    'controller': {
                        'firstName': controller_firstName,
                        'lastName': controller_lastName,
                        'title': controller_title,
                        'dateOfBirth': controller_dateOfBirth,
                        'ssn': controller_ssn,
                        'address': {
                            'address1': controller_address,
                            'city': controller_city,
                            'stateProvinceRegion': controller_stateProvinceRegion,
                            'postalCode': controller_postalCode,
                            'country': controller_country,
                                    }
                                },
                        }




                customer = dwolla_app_token.post('customers', request_body)
                customer_url = customer.headers['location']
                dwolla_id = customer_url.split('/')[-1]
                print ('fu1l id ----------------------------------------------------->>',dwolla_id, file=sys.stderr)



                customer = dwolla_app_token.get(customer_url)
                customer_status = customer.body['status']



                request_body_beneficial_owner = {
                    'firstName': owner_first_name,
                    'lastName': owner_last_name,
                    'dateOfBirth': owner_dob,
                    'ssn': owner_ssn,
                    'address': {
                        'address1': owner_address,
                        'city': owner_city,
                        'stateProvinceRegion': owner_state,
                        'country': owner_country,
                        'postalCode': owner_postal,
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



                mongoDB.Merchants.update({"company_ID": company_ID}, {"$set": {"dwolla_customer_url_id": dwolla_id}});


            response = plaid_client.link_token_create({
                'user': {
                    # This should correspond to a unique id for the current user.
                    'client_user_id': 'user-id'
                    # 'client_user_id': session.get('email')
                },
                'client_name': "Plaid Quickstart",
                'products': ['auth','transactions','identity'],
                'country_codes': current_app.config['PLAID_COUNTRY_CODES'],
                'language': "en",
                #'redirect_uri': PLAID_REDIRECT_URI,
            })


            link_token = response['link_token']

            print('LINK TOKEN: ', link_token)


            session["email"] = email
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['access_status'] = user.access_status
            session['notification_count'] = user.notification_count
            session['business_id'] = user.business_id
            session["user_databases"] = user.user_databases

            flask_login.login_user(user)

            print('success ---------------------------------------------->', file=sys.stderr)
            flash(u'Success New User Registered', 'flash_success')


            print('redirecting ---------------------------------------------->', file=sys.stderr)
            return redirect(url_for('MCA_Plaid_Confirm.MCA_Plaid_Confirm', did=dwolla_id, mid=company_ID, fid=funder_id, link_token=link_token))
            print('redirected ---------------------------------------------->', file=sys.stderr)



    return render_template("/Merchant/Secure_Bank/Secure_Register/secure_register.html", mid=merchant_id, fid=funder_id)