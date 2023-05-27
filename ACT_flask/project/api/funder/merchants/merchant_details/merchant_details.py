from flask import Blueprint, session, url_for, request, redirect, render_template, flash
from flask_session import Session
import pymongo
import sys
import gridfs
from project import db
from flask_login import login_required
import datetime
import uuid


Merchant_Details_Blueprint = Blueprint('MCA_Merchant_Details', __name__)
@Merchant_Details_Blueprint.route('/api/funder/merchants/merchant_details/merchant_details/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Merchant_Details():

    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]

    fs = gridfs.GridFS(mongoDB)


    company_id_var = request.args.get('mid', None)


    company_info = mongoDB.Merchants.find_one({"company_ID": company_id_var})

    legal_company_name = company_info['legal_company_name']
    company_DBA = company_info['company_DBA']
    poc_first_name = company_info['poc_first_name']
    poc_last_name = company_info['poc_last_name']
    poc_email = company_info['poc_email']
    poc_phone = company_info['poc_phone']
    business_description = company_info['business_description']
    funder = company_info['funder']
    under_writer = company_info['under_writer']
    ISO = company_info['ISO']
    sales_rep = company_info['sales_rep']
    MCC = company_info['MCC']
    SIC = company_info['SIC']
    documents = company_info['uploaded_documents']
    #bank_statements = company_info['Uploaded_Documents']['Bank_Statements']

    owners_list = []
    for own in company_info['owners']:
        owners_list.append([own['owner_first_name'], own['owner_last_name'], own['owner_dob'], own['owner_ssn'], own['owner_address'], own['owner_city'], own['owner_state'], own['owner_country'], own['owner_postal'], own['owner_ID']] )




    doc_list = []
    print('documents --->', documents)
    for docs in documents:
        for k, v in docs.items():
            print('kkk --->', k)
            if k != "bank_statements":
                print('file name ----->', v)
                file_info = mongoDB.fs.files.find_one({"filename": v})
                print('file info ----->', file_info)
                uploadDate = file_info['uploadDate']
                timestamp = uploadDate.strftime('%m/%d/%Y')
                print(v, file=sys.stderr)
                norm_name = (v[:-33]).replace('_', ' ')
                doc_list.append([v, norm_name, timestamp])
            else:
                for b, s in v.items(): #loop through the bank statement dict
                    print('file name ----->', s)
                    file_info = mongoDB.fs.files.find_one({"filename": s})
                    print('file info ----->', file_info)
                    uploadDate = file_info['uploadDate']
                    timestamp = uploadDate.strftime('%m/%d/%Y')
                    print(s, file=sys.stderr)
                    norm_name = (s[:-33]).replace('_', ' ').title()
                    doc_list.append([s, norm_name, timestamp])






    if request.method == 'POST':


        form_data = request.form
        print(form_data, file=sys.stderr)


        try:
            print("REQUEST", file=sys.stderr)
            new_document = request.files["new_document"]
            document_name = form_data["document_name"]

            new_doc_ID = document_name + '_' + str(uuid.uuid5(uuid.NAMESPACE_DNS, (legal_company_name + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))).replace("-", "")

            mongoDB.Merchants.update({"company_ID": company_id_var}, {"$push": {"uploaded_documents":{document_name: new_doc_ID}}})

            print('11111111111111', file=sys.stderr)

            fs.put(new_document, filename=new_doc_ID)

            print('2222222222222', file=sys.stderr)

        except:
            print('No Image Upload', file=sys.stderr)





        try:
            delete_it = form_data["delete"]
            print("DELETE IT: -------> ", delete_it, file=sys.stderr)
            if form_data["delete"]:
                mongoDB.Syndicators.delete_one({"company_ID": company_id_var})
                return redirect('/merchants/merchant_manager/')

        except:
            print("Did not delete", file=sys.stderr)



        updated_legal_company_name = form_data['legal_company_name']
        updated_company_DBA = form_data['company_DBA']
        updated_poc_first_name = form_data['poc_first_name']
        updated_poc_last_name = form_data['poc_last_name']
        updated_poc_email = form_data['poc_email']
        updated_poc_phone = form_data['poc_phone']
        updated_business_description = form_data['business_description']
        updated_funder = form_data['funder']
        updated_under_writer = form_data['under_writer']
        updated_ISO = form_data['ISO']
        updated_sales_rep = form_data['sales_rep']
        updated_MCC = form_data['MCC']
        updated_SIC = form_data['SIC']

        print(updated_business_description)

        if updated_legal_company_name:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"legal_company_name": updated_legal_company_name}});
            legal_company_name=updated_legal_company_name
            flash(u'Legal Company Name Updated', 'flash_success')
        if updated_company_DBA:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"company_DBA": updated_company_DBA}});
            company_DBA=updated_company_DBA
            flash(u'Company DBA Updated', 'flash_success')
        if updated_poc_first_name:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"poc_first_name": updated_poc_first_name}});
            poc_first_name=updated_poc_first_name
            flash(u'First Name Updated', 'flash_success')
        if updated_poc_last_name:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"poc_last_name": updated_poc_last_name}});
            poc_last_name=updated_poc_last_name
            flash(u'Last Name Updated', 'flash_success')
        if updated_poc_email:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"poc_email": updated_poc_email}});
            poc_email=updated_poc_email
            flash(u'Email Updated', 'flash_success')
        if updated_poc_phone:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"poc_phone": updated_poc_phone}});
            poc_phone=updated_poc_phone
            flash(u'Phone Updated', 'flash_success')
        if updated_business_description:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"business_description": updated_business_description}});
            business_description=updated_business_description
            flash(u'Business Description Updated', 'flash_success')
        if updated_funder:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"funder": updated_funder}});
            funder=updated_funder
            flash(u'Funder Updated', 'flash_success')
        if updated_under_writer:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"under_writer": updated_under_writer}});
            under_writer=updated_under_writer
            flash(u'Under Writer Updated', 'flash_success')
        if updated_ISO:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"ISO": updated_ISO}});
            ISO=updated_ISO
            flash(u' ISO Updated', 'flash_success')
        if updated_sales_rep:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"sales_rep": updated_sales_rep}});
            sales_rep=updated_sales_rep
            flash(u' Sales Rep Updated', 'flash_success')
        if updated_MCC:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"MCC": updated_MCC}});
            MCC=updated_MCC
            flash(u' MCC Updated', 'flash_success')
        if updated_SIC:
            mongoDB.Merchants.update({"company_ID": company_id_var},{"$set": {"SIC": updated_SIC}});
            SIC=updated_SIC
            flash(u' SIC Updated', 'flash_success')

        company_info = mongoDB.Merchants.find_one({"company_ID": company_id_var})

        legal_company_name = company_info['legal_company_name']
        company_DBA = company_info['company_DBA']
        poc_first_name = company_info['poc_first_name']
        poc_last_name = company_info['poc_last_name']
        poc_email = company_info['poc_email']
        poc_phone = company_info['poc_phone']
        business_description = company_info['business_description']
        funder = company_info['funder']
        under_writer = company_info['under_writer']
        ISO = company_info['ISO']
        sales_rep = company_info['sales_rep']
        MCC = company_info['MCC']
        SIC = company_info['SIC']



    return render_template("/Funder/Merchants/Merchant_Details/Merchant_Details/merchant_details.html", doc_list=doc_list, owners_list=owners_list, mid=company_id_var, legal_company_name=legal_company_name, company_DBA=company_DBA, poc_first_name=poc_first_name, poc_last_name=poc_last_name,
    poc_email=poc_email, poc_phone=poc_phone, business_description=business_description, funder=funder, under_writer=under_writer, ISO=ISO, sales_rep=sales_rep, MCC=MCC, SIC=SIC, access_status=session.get('access_status'), notification_count=session.get('notification_count'))
