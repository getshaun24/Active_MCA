from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
from project import db


ISO_Details_Blueprint = Blueprint('MCA_ISO_Details', __name__)
@ISO_Details_Blueprint.route('/api/funder/isos/iso_details/', methods=['GET', 'POST'])
def MCA_ISO_Details():



    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        if access_status != "admin":
            return redirect(url_for('MCA_Login'))


        ISO_ID = request.args.get('ISO_ID', None)
        print(ISO_ID, file=sys.stderr)

        get_iso = mongoDB.ISOs.find_one({"ISO_ID": ISO_ID})


        ISO_business_name = get_iso['ISO_business_name']
        ISO_relationship_manager = get_iso['ISO_relationship_manager']
        ISO_email = get_iso['ISO_email']
        ISO_phone = get_iso['ISO_phone']
        ISO_address = get_iso['ISO_address']
        ISO_city = get_iso['ISO_city']
        ISO_state = get_iso['ISO_state']
        ISO_postal = get_iso['ISO_postal']


        if request.method == 'POST':

            form_data = request.form
            print(form_data, file=sys.stderr)

            try:
                delete_it = form_data["delete"]
                print("DELETE IT: -------> ", delete_it, file=sys.stderr)
                if form_data["delete"]:
                    mongoDB.Syndicators.delete_one({ "syndicator_business_name": syndicator_biz })
                    return redirect('/ISOs/ISOs/')

            except:
                print("Did not delete", file=sys.stderr)



            form_data = request.form

            print(form_data, file=sys.stderr)

            updated_ISO_business_name = form_data["business_name"]
            updated_ISO_relationship_manager = form_data["relationship_manager"]
            updated_ISO_email = form_data["email"]
            updated_ISO_phone = form_data["phone"]
            updated_ISO_address = form_data["address"]
            updated_ISO_city = form_data["city"]
            updated_ISO_state = form_data["state"]
            updated_ISO_postal = form_data["postal"]


            if updated_ISO_business_name:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_business_name": updated_ISO_business_name}});
                ISO_business_name=updated_ISO_business_name
                flash(u' ISO Business Name Updated', 'flash_success')
            if updated_ISO_relationship_manager:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_relationship_manager": updated_ISO_relationship_manager}});
                ISO_relationship_manager=updated_ISO_relationship_manager
                flash(u'Relationship Manager Updated', 'flash_success')
            if updated_ISO_email:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_email": updated_ISO_email}});
                ISO_email=updated_ISO_email
                flash(u'Email Updated', 'flash_success')
            if updated_ISO_phone:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_phone": updated_ISO_phone}});
                ISO_phone=updated_ISO_phone
                flash(u'Phone Number Updated', 'flash_success')
            if updated_ISO_address:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_address": updated_ISO_address}});
                ISO_address=updated_ISO_address
                flash(u'Address Updated', 'flash_success')
            if updated_ISO_city:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_city": updated_ISO_city}});
                ISO_city=updated_ISO_city
                flash(u'City Updated', 'flash_success')
            if updated_ISO_state:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_state": updated_ISO_state}});
                ISO_state=updated_ISO_state
                flash(u'email Updated', 'flash_success')
            if updated_ISO_postal:
                mongoDB.ISOs.update({"ISO_ID": ISO_ID},{"$set": {"ISO_postal": updated_ISO_postal}});
                ISO_postal=updated_ISO_postal
                flash(u'Postal Code Updated', 'flash_success')





    return render_template("/Funder/ISOs/ISO_Details/iso_details.html", ISO_ID=ISO_ID, ISO_business_name=ISO_business_name, ISO_relationship_manager=ISO_relationship_manager, ISO_email=ISO_email, ISO_phone=ISO_phone, ISO_address=ISO_address, ISO_city=ISO_city, ISO_state=ISO_state, ISO_postal=ISO_postal, access_status=access_status, notification_count=notification_count)
