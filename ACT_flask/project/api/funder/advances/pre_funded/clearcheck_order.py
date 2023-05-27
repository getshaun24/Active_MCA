from flask import Blueprint
from flask import session
from flask_session import Session
from flask import request
from flask import render_template
import pymongo
import sys
from project import db
from flask_login import login_required


Clearcheck_Order_Blueprint = Blueprint('MCA_Clearcheck_Order', __name__)
@Clearcheck_Order_Blueprint.route('/api/funder/advances/pre_funded/clearcheck_order/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Clearcheck_Order():





    if not session.get("email"):
        return redirect("../../user_settings/login/")

    else:

        mongoDB = db[session.get("user_database")]

        user_table = mongoDB.Users.find_one({ "email": session.get("email") })
        access_status = user_table["access_status"]
        notification_count = user_table["notification_count"]

        if access_status != "admin":
            return redirect(url_for('MCA_Login'))


        company_id_var = request.args.get('company_id_var', None)

        get_company = mongoDB.Company.find_one({"company_ID": company_id_var})
        clear_decrypted = get_company["clear_decrypted"]
        business_email = get_company["business_email"]
        print(clear_decrypted, file=sys.stderr)





        response_text = ''
        report_description = ''
        order_date = ''
        completed_date = ''
        last_four_ssn = ''
        ssn_status = ''
        address_history = ''
        county_criminal = ''
        address_list = []
        county_crim_list= []



        URL_1 = "https://sandbox.clearchecks.com/api/reports/all?api_token=" + clear_decrypted
        response_1 = (requests.get(URL_1)).json()
        print('response_1 - ', response_1, file=sys.stderr)
        report_key = response_1['data'][0]['report_key']
        print('REPORT KEY - ', report_key, file=sys.stderr)



        URL_2 = "https://sandbox.clearchecks.com/api/reports/" + report_key + "/status?api_token=" + clear_decrypted
        response_2 = (requests.get(URL_2)).json()
        print('response_2 - ', response_2, file=sys.stderr)


        URL_3 = "https://sandbox.clearchecks.com/api/report/" + report_key + "?api_token=" + clear_decrypted
        response_3 = (requests.get(URL_3)).json()
        response_text = (requests.get(URL_3)).text
        print('response_3 - ', response_3, file=sys.stderr)
        report_description = response_3['report_description']
        order_date = response_3['order_date']['date'][:10]
        try:
            completed_date = response_3['completed_date']['date'][:10]
        except:
            completed_date = 'None'
        last_four_ssn = response_3['subject']['ssn']
        ssn_status = response_3['ssn_trace']['message']
        address_history = response_3['address_history']['addresses']
        try:
            county_criminal = response_3['county_criminal']['county_records']
        except:
            county_criminal = 'None'
        criminal_records_count = response_3['criminal_records']['count']
        liens = response_3['blj']['liens']
        bankruptcies = response_3['blj']['bankruptcies']
        judgments = response_3['blj']['judgments']




        address_list = []
        for add in address_history:
            try:
                name = add['name']['first_name'] + ' ' + add['name']['middle_name'] + ' ' + add['name']['last_name']
            except:
                name = add['name']['first_name'] + ' ' + add['name']['last_name']
            address = add['address']['street_number'] + ' ' + add['address']['street_name'] + ' ' + add['address']['street_suffix'] + ', ' + add['city'] + ', ' + add['state'] + ' ' + add['zipcode']
            dob_match = add['dob_match']['day'] + '/' + add['dob_match']['month'] + '/' + add['dob_match']['year']
            date_range = add['record_date']['first'] + ' to ' + add['record_date']['last']
            address_list.append([name, address, dob_match, date_range])


        criminal_records_list = []
        if criminal_records_count > 0:
            records_list = response_3['criminal_records']['records']
            for rec in records_list:
                try:
                    crim_name = rec['first_name'] + ' ' + rec['middle_name'] + ' ' + rec['last_name']
                except:
                    crim_name = rec['first_name'] + ' ' + rec['last_name']
                crim_dob = rec['fulldob']
                crim_state = rec['state']
                crim_address = rec['address'] + ' ' + rec['city']
                case_number = rec['case_number']
                jurisdiction = rec['jurisdiction']
                jurisdictioncounty = rec['jurisdictioncounty']
                offenses_list = []
                for off in rec['offenses']:
                    offensedescription = off['offensedescription']
                    arrestdate = off['arrestdate']
                    casetype = off['casetype']
                    offensedate = off['offensedate']
                    offensecode = off['offensecode']
                    chargefilingdate = off['chargefilingdate']
                    off_court = off['court']
                    off_comments = off['comments']
                    offenses_list.append([offensedescription, arrestdate, casetype, offensedate, offensecode, chargefilingdate, off_court, off_comments])
                criminal_records_list.append([crim_name, crim_dob, crim_state, crim_address, case_number, jurisdiction, jurisdictioncounty, offenses_list])

        print('criminal_records_list - ',criminal_records_list, file=sys.stderr)

        county_crim_list = []
        try:
            for crim in county_criminal:
                county_crim_list.append([crim['state'], crim['county'], crim['result'].upper()])
        except:
            print('none')


        liens_list = []
        for ii in liens:

            creditors_list = []
            for cred in ii['creditors']:
                creditors_list.append(cred['name'])

            properties_list = []
            for prop in ii['properties']:
                properties_list.append(prop['name'])

            businesses_list = []
            for biz in ii['businesses']:
                businesses_list.append(biz['name'])

            cases_list = []
            for case in ii['cases']:
                cases_list.append([case['deed_category'], case['case_description'], case['date'], case['doc_number'], case['page_number'], case['book_number'], case['orig_doc_number'],
                case['orig_page_number'], case['orig_book_number'], case['recording_date'], case['damar_type'], case['tax_period_start_date'], case['tax_period_end_date'], case['refile_extend_last_date'],
                case['abstract_issue_date'], case['stay_ordered'], case['stay_ordered_date'], case['document_filing_date'], case['orig_document_date'], case['orig_recording_date'], case['created_at'],
                case['updated_at'], case['tax_period_max'], case['tax_period_min']])

            debtors_list = []
            for deb in ii['debtors']:
                debtors_list.append([deb['first_name'], deb['middle_name'], deb['last_name'], deb['ssn'], deb['address'], deb['city'], deb['state'], deb['zip'], deb['phone'],
                deb['created_at'], deb['updated_at'], deb['name']])

            liens_list.append([ii['first_seen'], ii['last_seen'], ii['fips_code'], ii['case_county'], ii['case_state'], ii['amount'], ii['lien_type'], ii['issuing_agency'], creditors_list, properties_list, businesses_list, cases_list, debtors_list])




        bankruptcies_list = []
        for ii in bankruptcies:

            debtors_list = []
            for deb in ii['debtors']:
                debtors_list.append([deb['first_name'], deb['middle_name'], deb['last_name'], deb['ssn'], deb['address'], deb['city'], deb['state'], deb['zip'],
                deb['phone'], deb['created_at'], deb['updated_at'], deb['name']])

            trustees_list = []
            for tru in ii['trustees']:
                trustees_list.append([tru['first_name'], tru['middle_name'], tru['last_name'], tru['ssn'], tru['address'], tru['city'], tru['state'], tru['zip'],
                tru['phone'], tru['created_at'], tru['updated_at'], tru['name']])


            bankruptcies_list.append([debtors_list,  trustees_list, ii['first_seen'], ii['last_seen'], ii['chapter'], ii['converted_date'], ii['date_collected'], ii['last_date_to_file_poc'], ii['transaction_id'], ii['transaction_type'],
            ii['voluntary_flag'], ii['filing_date'], ii['full_case_number'], ii['judge_name'], ii['case_status'], ii['case_status_date'], ii['assets'], ii['screen'],
            ii['attorney']['name'], ii['attorney']['address'], ii['attorney']['city'], ii['attorney']['state'], ii['attorney']['zip'], ii['attorney']['zip4'],
            ii['attorney']['phone'], ii['attorney']['law_firm'], ii['court']['district'], ii['court']['division'], ii['court']['number'], ii['court']['name'], ii['meeting']['date'],
            ii['meeting']['address']])



        judgments_list = []
        for ii in judgments:
            judgments_list.append([ii['first_seen'], ii['last_seen']])



        if request.method == 'POST':






            print('DECRYPTED_TOKEN_OUTPUT --', clear_decrypted, file=sys.stderr)

            # you should use sandbox url, not production if you'd like to test this
            URL = "https://sandbox.clearchecks.com/api/orders/new?api_token=" + clear_decrypted

            HEADERS = {"Content-Type": "application/json","Accept": "application/json"}

            PAYLOAD = {
              "report_sku": "HIRE3",
              #"applicant_emails": [business_email],
              "applicant_emails": ['helpit6@gmail.com'],
              "drug_test": "Y",
              "drug_sku": "drug",
              "mvr": "Y",
              "employment": "Y",
              "education": "Y",
              "blj": "Y",
              "federal_criminal": "Y",
              "terms_agree": "Y"
            }

            response = (requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)).json()
            print(response, file=sys.stderr)

            order_report_key = response['applicants'][0]['report_key']
            print('order_report_id - ',order_report_key, file=sys.stderr)




    return render_template("/Funder/Advances/Pre_Funded/Clearcheck_Order/clearcheck_order.html", response_text=response_text, company_id_var=company_id_var, notification_count=notification_count, report_description=report_description, order_date=order_date, completed_date=completed_date, last_four_ssn=last_four_ssn, ssn_status=ssn_status, county_crim_list=county_crim_list, address_list=address_list, criminal_records_list=criminal_records_list, criminal_records_count=criminal_records_count, liens_list=liens_list, judgments_list=judgments_list, bankruptcies_list=bankruptcies_list)
