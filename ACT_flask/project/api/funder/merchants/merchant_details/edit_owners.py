from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
from flask_login import login_required
from flask import flash


Edit_Owners_Blueprint = Blueprint('MCA_Edit_Owners', __name__)
@Edit_Owners_Blueprint.route('/api/funder/merchants/merchant_details/edit_owners/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Edit_Owners():

    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))

    mongoDB = db[session.get("user_database")]

    merchant_id = request.args.get('mid', None)
    owner_id = request.args.get('oid', None)


    # company_info = mongoDB.Merchants.find_one({"company_ID": merchant_id})
    owner = mongoDB.Merchants.find_one({'company_ID': merchant_id, 'owners.owner_ID': owner_id}, {'owners.$': 1, '_id': 0})['owners'][0]
    print(owner)


    owner_first_name = owner['owner_first_name']
    owner_last_name = owner['owner_last_name']
    owner_dob = owner['owner_dob']
    owner_ssn = owner['owner_ssn']
    owner_address = owner['owner_address']
    owner_city = owner['owner_city']
    owner_state = owner['owner_state']
    owner_country = owner['owner_country']
    owner_postal = owner['owner_postal']
    # owner_count = 0
    # for own in company_info['owners']:
    #     if own['owner_ID'] == owner_id:
    #         owner_first_name = own['owner_first_name']
    #         owner_last_name = own['owner_last_name']
    #         owner_dob = own['owner_dob']
    #         owner_ssn = own['owner_ssn']
    #         owner_address = own['owner_address']
    #         owner_city = own['owner_city']
    #         owner_state = own['owner_state']
    #         owner_country = own['owner_country']
    #         owner_postal = own['owner_postal']
    #         break
    #     owner_count += 1



    if request.method == 'POST':


        form_data = request.form
        print(form_data, file=sys.stderr)


        try:
            delete_it = form_data["delete"]
            print("DELETE IT: -------> ", delete_it, file=sys.stderr)
            if form_data["delete"]:
                mongoDB.Merchants.update({"company_ID": merchant_id},{"$pull": {"owners": {"owner_ID": owner_id}}});
                return redirect('/merchants/merchant_manager/')

        except:
            print("Did not delete", file=sys.stderr)

        updated_owner_first_name = form_data['owner_first_name']
        updated_owner_last_name = form_data['owner_last_name']
        updated_owner_dob = form_data['owner_dob']
        updated_owner_ssn = form_data['owner_ssn']
        updated_owner_address = form_data['owner_address']
        updated_owner_city = form_data['owner_city']
        updated_owner_state = form_data['owner_state']
        updated_owner_country = form_data['owner_country']
        updated_owner_postal = form_data['owner_postal']


        if updated_owner_first_name:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_first_name": updated_owner_first_name}});
            owner_first_name=updated_owner_first_name
            flash(u'Owner First Name Updated', 'flash_success')
        if updated_owner_last_name:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_last_name": updated_owner_last_name}});
            owner_dob=updated_owner_last_name
            flash(u'Owner Date of Birth Updated', 'flash_success')
        if updated_owner_dob:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_dob": updated_owner_dob}});
            owner_dob=updated_owner_dob
            flash(u'Owner Date of Birth Updated', 'flash_success')
        if updated_owner_ssn:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_ssn": updated_owner_ssn}});
            owner_ssn=updated_owner_ssn
            flash(u'Owner SSN Updated', 'flash_success')
        if updated_owner_address:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_address": updated_owner_address}});
            owner_address=updated_owner_address
            flash(u'Owner Address Updated', 'flash_success')
        if updated_owner_city:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_city": updated_owner_city}});
            owner_city=updated_owner_city
            flash(u'Owner City Updated', 'flash_success')
        if updated_owner_state:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_state": updated_owner_state}});
            owner_state=updated_owner_state
            flash(u'Owner State Updated', 'flash_success')
        if updated_owner_country:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_country": updated_owner_country}});
            owner_country=updated_owner_country
            flash(u'Owner Country Updated', 'flash_success')
        if updated_owner_postal:
            mongoDB.Merchants.update({"company_ID": merchant_id, "owners.owner_ID": owner_id},{"$set": {"owners.$.owner_postal": updated_owner_postal}});
            owner_postal=updated_owner_postal
            flash(u'Owner Postal Code Updated', 'flash_success')


        owner = mongoDB.Merchants.find_one({'company_ID': merchant_id, 'owners.owner_ID': owner_id}, {'owners.$': 1, '_id': 0})['owners'][0]
        owner_first_name = owner['owner_first_name']
        owner_last_name = owner['owner_last_name']
        owner_dob = owner['owner_dob']
        owner_ssn = owner['owner_ssn']
        owner_address = owner['owner_address']
        owner_city = owner['owner_city']
        owner_state = owner['owner_state']
        owner_country = owner['owner_country']
        owner_postal = owner['owner_postal']

    return render_template("/Funder/Merchants/Merchant_Details/Edit_Owners/edit_owners.html", mid=merchant_id, oid=owner_id, access_status=session.get('access_status'), notification_count=session.get('notification_count'),
    owner_first_name=owner_first_name, owner_last_name=owner_last_name, owner_dob=owner_dob, owner_ssn=owner_ssn, owner_address=owner_address, owner_city=owner_city, owner_state=owner_state, owner_country=owner_country, owner_postal=owner_postal)
