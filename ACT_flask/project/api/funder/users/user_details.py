from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
# from server import mongo_client
from project import db


User_Details_Blueprint = Blueprint('MCA_User_Details', __name__)
@User_Details_Blueprint.route('/api/funder/users/user_details/', methods=['GET', 'POST'])
def MCA_User_Details():


    if not session.get("email"):
        return redirect(url_for('MCA_Login'))

    else:

        mongoDB = db[session.get("user_database")]


        email = request.args.get('selected_user', None)


        user_table = mongoDB.Users.find_one({ "email": session.get("email") })

        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]
        first_name = user_table["first_name"]
        last_name = user_table["last_name"]
        password = user_table["password"]
        email = user_table["email"]


        if access_status != "admin":
            return redirect(url_for('MCA_Login'))


        if request.method == 'POST':

            form_data = request.form
            print(form_data, file=sys.stderr)


            delete_it = form_data["delete"]
            print(delete_it, file=sys.stderr)
            if delete_it == "delete":
                mongoDB.Users.delete_one({ "email": email })
                db.Master_Credentials.master_user_list.delete_one({ "email": email })
                return redirect('/../User_Manager/')






            #------------ merchant info ------------

            updated_access_status = form_data["access_status"]
            updated_first_name = form_data["first_name"]
            updated_last_name = form_data["last_name"]
            updated_email = form_data["email"]
            updated_password_1 = form_data["password_1"]
            updated_password_2 = form_data["password_2"]

            if updated_password_1 != updated_password_2:
                # passwords do not match
                pass

            else:

                if updated_access_status:
                    mongoDB.Users.update({"email": email},{"$set": {"access_status": updated_access_status}});
                    db.Master_Credentials.master_user_list.update({"email": email},{"$set": {"access_status": updated_access_status}});
                    access_status=updated_access_status
                    
                if updated_first_name:
                    mongoDB.Users.update({"email": email},{"$set": {"first_name": updated_first_name}});
                    first_name=updated_first_name
                    
                if updated_last_name:
                    mongoDB.Users.update({"email": email},{"$set": {"last_name": updated_last_name}});
                    last_name=updated_last_name
                    
                if updated_email:
                    mongoDB.Users.update({"email": email},{"$set": {"email": updated_email}});
                    db.Master_Credentials.master_user_list.update({"email": email},{"$set": {"email": updated_email}});
                    email=updated_email
                if updated_password_1:
                    mongoDB.Users.update({"email": email},{"$set": {"password": updated_password_1}});
                    db.Master_Credentials.master_user_list.update({"email": email},{"$set": {"password": updated_password_1}});
                    password=updated_password_1
                    



    return render_template("/Funder/Users/User_Details/user_details.html", access_status=access_status, notification_count=notification_count, first_name=first_name, last_name=last_name, email=email, password=password)
