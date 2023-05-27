from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db
import datetime
import uuid


New_Advance_Blueprint = Blueprint('MCA_New_Advance', __name__)
@New_Advance_Blueprint.route('/api/funder/merchants/new_advance/', methods=['GET', 'POST']) 
def MCA_New_Advance():


    if not session.get("email"):
        return redirect("../../user_settings/login/")

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        if access_status != "admin":
            return redirect(url_for('MCA_Login'))



        if 'merchant' in request.args.get('company_id_var', None):
            comp_id_var = request.args.get('company_id_var', None)
            company_id_var = comp_id_var[:-9]
            from_merchant = True
            print('COMP VAR merchant --------------------> ', company_id_var, file=sys.stderr)
        else:
            company_id_var = request.args.get('company_id_var', None)
            from_merchant = False
            print('COMP VAR --------------------> ', company_id_var, file=sys.stderr)



        get_company = mongoDB.Company.find_one({"company_ID": company_id_var})
        company_name = get_company["company_DBA"]
        cash_ads = get_company["Cash_Advance_Contracts"]
        len_of_cash = len(cash_ads)


        if request.method == 'POST':


            form_data = request.form
            print(form_data, file=sys.stderr)


            #------------ Cash Advance Contract ------------

            contract_ID = uuid.uuid5(uuid.NAMESPACE_DNS, (str(company_id_var) + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            status = 'Open'
            start_date = form_data["start_date"]
            expected_end_date = form_data["expected_end_date"]
            split_percent = form_data["split_percent"]
            factor_rate = form_data["factor_rate"]
            fico_score = form_data["fico_score"]
            funded_via = form_data["funded_via"]
            position = form_data["position"]
            tags = form_data["tags"]
            ACH_pull_schedule = form_data["ACH_pull_schedule"]
            advance_amount = form_data["advance_amount"]
            initiated_email = session.get("email")


            #-------------------- Math --------------------

            duration = abs((datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(expected_end_date, "%Y-%m-%d")).days)
            print("duration: ", duration, file=sys.stderr)
            total_commission = float(advance_amount) * 0.1
            expected_repayment_amount = float(advance_amount) * float(factor_rate)

            #-----------------------------------------------



            mongoDB.Company.update({"company_ID": company_id_var},
                {"$push": {"Cash_Advance_Contracts": { "contract_ID": contract_ID, "status": status, "start_date": start_date, "expected_end_date": expected_end_date, "duration": duration, "split_percent": split_percent, "factor_rate": factor_rate, "funded_via": funded_via, "fico_score": fico_score, "position": position, "tags": tags, "advance_amount":advance_amount, "expected_repayment_amount": expected_repayment_amount, "day":0, "total_commission": total_commission, "open_amount_repaid":0, "open_percent_paid":0, "default_amount_repaid":0, "default_percent_paid":0, "total_amount_repaid":0, "total_percent_paid":0, "performance":0, "Syndicators":[{}], "ACH_pull_schedule": ACH_pull_schedule, "pause_until":"None", "initiated_email":initiated_email, "selected_account_id": "None",
                "Transaction_track":[] }}});


    return render_template("/Funder/Merchants/New_Advance/new_advance.html", company_name=company_name, company_id_var=company_id_var, from_merchant=from_merchant, access_status=access_status, notification_count=notification_count)
