from flask import Blueprint, session, url_for, request, redirect, render_template
import sys
from project import db


Syndicator_Details_Blueprint = Blueprint('MCA_Syndicator_Details', __name__)
@Syndicator_Details_Blueprint.route('/api/funder/syndicators/syndicator_details/', methods=['GET', 'POST']) 
def MCA_Syndicator_Details():


    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    mongoDB = db[session.get("user_database")]


    user_table = mongoDB.Users.find_one({ "email": session.get("email") })
    access_status = user_table["access_status"]
    notification_count = user_table["notification_count"]


    if access_status != "admin":
        return redirect("../../user_settings/login/")

    else:


        syndicator_biz = request.args.get('syndicator_biz', None) # -- Should be contract_num later !!!
        print(syndicator_biz, file=sys.stderr)


        syndicator_collection = mongoDB.Syndicators.find_one({ "syndicator_business_name": syndicator_biz })

        syndicator_business_name = syndicator_collection['syndicator_business_name']
        syndicator_email = syndicator_collection['syndicator_email']
        syndicator_phone = syndicator_collection['syndicator_phone']
        syndicator_address = syndicator_collection['syndicator_address']
        syndicator_city = syndicator_collection['syndicator_city']
        syndicator_state = syndicator_collection['syndicator_state']
        syndicator_zip = syndicator_collection['syndicator_zip']
        syndicator_state = syndicator_collection['syndicator_state']
        syndicator_is_ISO = syndicator_collection['syndicator_is_ISO']
        #revenue = syndicator_collection['revenue']
        #profit = syndicator_collection['profit']
        email = syndicator_collection['syndicator_email']
        password = syndicator_collection['password']





        if request.method == 'POST':

            form_data = request.form
            print(form_data, file=sys.stderr)


            try:
                delete_it = form_data["delete"]
                print("DELETE IT: -------> ", delete_it, file=sys.stderr)
                if form_data["delete"]:
                    mongoDB.Syndicators.delete_one({ "syndicator_business_name": syndicator_biz })
                    return redirect('/syndicators/syndicators/')

            except:
                print("Did not delete", file=sys.stderr)




            updated_syndicator_business_name = form_data["business_name"]
            updated_syndicator_email = form_data["email"]
            updated_syndicator_phone = form_data["phone"]
            updated_syndicator_address = form_data["address"]
            updated_syndicator_city = form_data["city"]
            updated_syndicator_state = form_data["state"]
            updated_syndicator_zip = form_data["zip"]
            try:
                updated_syndicator_is_ISO = form_data["Is_ISO"]
            except:
                updated_syndicator_is_ISO = ""
            updated_syndicator_email = form_data["email"]
            updated_syndicator_password_1 = form_data["password_1"]
            updated_syndicator_password_2 = form_data["password_2"]

            if updated_syndicator_password_1 != updated_syndicator_password_2:
                pass
            else:
                if updated_syndicator_business_name:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_business_name": updated_syndicator_business_name}});
                    syndicator_business_name=updated_syndicator_business_name

                if updated_syndicator_email:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_email": updated_syndicator_email}});
                    syndicator_email=updated_syndicator_email

                if updated_syndicator_phone:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_phone": updated_syndicator_phone}});
                    syndicator_phone=updated_syndicator_phone

                if updated_syndicator_address:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_address": updated_syndicator_address}});
                    syndicator_address=updated_syndicator_address

                if updated_syndicator_city:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_city": updated_syndicator_city}});
                    syndicator_city=updated_syndicator_city

                if updated_syndicator_state:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_state": updated_syndicator_state}});
                    syndicator_state=updated_syndicator_state

                if updated_syndicator_zip:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_zip": updated_syndicator_zip}});
                    syndicator_zip=updated_syndicator_zip

                if updated_syndicator_is_ISO:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"syndicator_is_ISO": updated_syndicator_is_ISO}});
                    syndicator_is_ISO=updated_syndicator_is_ISO

                if updated_syndicator_email:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"email": updated_syndicator_email}});
                    email=updated_syndicator_email

                if updated_syndicator_password_1:
                    mongoDB.Syndicators.update({"syndicator_business_name": syndicator_biz},{"$set": {"password": updated_syndicator_password_1}});
                    password=updated_syndicator_password_1



    return render_template("/Funder/Syndicators/Syndicator_Details/syndicator_details.html", syndicator_biz=syndicator_biz, syndicator_business_name=syndicator_business_name, syndicator_email=syndicator_email, syndicator_phone=syndicator_phone, syndicator_address=syndicator_address, syndicator_city=syndicator_city, syndicator_state=syndicator_state, syndicator_zip=syndicator_zip, syndicator_is_ISO=syndicator_is_ISO, email=email, password=password, access_status=access_status, notification_count=notification_count)
