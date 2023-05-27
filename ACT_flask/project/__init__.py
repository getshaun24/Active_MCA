from flask import Flask, render_template, session, redirect, url_for, jsonify
from flask_session import Session
from flask_cors import CORS
from datetime import datetime, timedelta, timezone

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import current_user

import secrets 
# from . import mongo
import os
import pymongo

# from flask_login import LoginManager, login_required, logout_user
from project.api.models import User
# from project.api.mongo import db, close_mongo_db
import sys
from dotenv import load_dotenv
load_dotenv()

# Change this depending on the config you want to use.
# from config import DevelopmentConfig

# def create_app(config_class=None):

app = Flask(__name__, template_folder="", instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SECRET_KEY'] = 'active_mca'

CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin', 'Access-Control-Allow-Credentials'], supports_credentials=True)

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "super-secret_SHAUN"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

try:
	os.makedirs(app.instance_path)
except OSError:
	pass


# Initialize MongoDB
class MongoSingleton:
	print('Initializing Mongo - Singleton...', file=sys.stderr)
	_instance = None
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			cls._instance.client = pymongo.MongoClient(app.config['MONGO_CLI'], tls=True)
			print('Mongo initialized - Singleton')
		return cls._instance

global mongo
mongo = MongoSingleton().client
app.db = mongo
global db
db = mongo[app.config['MONGO_DB']]


jwt = JWTManager(app)

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
	print(user.id)
	return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
	identity = jwt_data["sub"]
	return User(identity, mongo)


# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
	try:
		exp_timestamp = get_jwt()["exp"]
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
		if target_timestamp > exp_timestamp:
			access_token = create_access_token(identity=get_jwt_identity())
			set_access_cookies(response, access_token)
		return response
	except (RuntimeError, KeyError):
		# Case where there is not a valid JWT. Just return the original response
		return response

# # Load user in current session

# login_manager = LoginManager()
# login_manager.login_view = 'MCA_Login.MCA_Login'
# login_manager.init_app(app)

# Load user in current session
# @login_manager.user_loader
# def load_user(user_id):
#     user = User(email=session.get('email'), db=db)
#     if user:
#         return user
#     return None

""" 
Clear user session and redirect to homepage.
In all of our pages all we have to do is if the logout button is clicked we just route to this endpoint. i.e.

if form_data['logout'] == 'logout':
	return redirect(url_for('/logout'))

"""
# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
# 	close_mongo_db()
# 	logout_user()
# 	session.clear()
# 	return redirect(url_for('MCA_Public_Homepage'))


# Clearcheck is Obsolete  ---- Will be Lexis Nexis Soon

# @app.route('/Active_MCA_Master/Clearcheck_Connect/', methods=['GET', 'POST']) # <- from '/'     
# def MCA_Clearcheck_Connect():
#     return render_template("/Active_MCA_Master/Clearcheck_Connect/clearcheck_connect.html", company_ID=company_ID)

# ---------------------------------  Public Pages  --------------------------------------------------->

#can make own page/blueprint eventually -- doing so requires going to everysingle page and updating the public homepage link

# @app.route('/', methods=['GET', 'POST']) # <- from '/'
# def MCA_Public_Homepage():
#     return render_template("index.html")

# @app.route('/Public/how_it_works/', methods=['GET', 'POST']) # <- from '/'
# def MCA_how_it_works():
#     return render_template("/Public/how_it_works/index.html")

# @app.route('/Public/Security/', methods=['GET', 'POST']) # <- from '/'
# def MCA_Security():
#     return render_template("/Public/Security/security.html")

# @app.route('/Public/Contact/', methods=['GET', 'POST']) # <- from '/'
# def MCA_Public_Contact():
#     return render_template("/Public/Contact/contact.html")


# ------------------------------- TEARDOWN APP CONTEXT ----------------------------------------->
# This is executed using the teardown_appcontext signal 

# @app.teardown_appcontext
# def teardown_db(exception):
# 	close_mongo_db()



# --------------------------------- BLUEPRINTS ------------------------------------------------->

# ---------------------------------  FUNDER  --------------------------------------------------->

from project.api.funder.funder_home.funder_home import Funder_Home_Blueprint
app.register_blueprint(Funder_Home_Blueprint)

# --------------------------------- Advances --------------------------------------------------->

from project.api.funder.advances.advance_manager.advance_manager import Advance_Manager_Blueprint
app.register_blueprint(Advance_Manager_Blueprint)

from project.api.funder.advances.pre_funded.edit_contract import Edit_Contract_Blueprint
app.register_blueprint(Edit_Contract_Blueprint)

from project.api.funder.advances.pre_funded.prefunded import Prefunded_Blueprint
app.register_blueprint(Prefunded_Blueprint)

from project.api.funder.advances.pre_funded.all_prefunded import All_Prefunded_Blueprint
app.register_blueprint(All_Prefunded_Blueprint)

from project.api.funder.advances.pre_funded.all_precontract import All_Precontract_Blueprint
app.register_blueprint(All_Precontract_Blueprint)

from project.api.funder.advances.pre_funded.fund import Fund_Blueprint
app.register_blueprint(Fund_Blueprint)

from project.api.funder.advances.pre_funded.bank_analysis import Bank_Analysis_Blueprint
app.register_blueprint(Bank_Analysis_Blueprint)

from project.api.funder.advances.pre_funded.clearcheck_order import Clearcheck_Order_Blueprint
app.register_blueprint(Clearcheck_Order_Blueprint)

# ------------------------------------- Merchants ---------------------------------------------->

from project.api.funder.merchants.merchant_manager import Merchant_Manager_Blueprint
app.register_blueprint(Merchant_Manager_Blueprint)

from project.api.funder.merchants.new_mca import New_MCA_Blueprint
app.register_blueprint(New_MCA_Blueprint)

from project.api.funder.merchants.new_advance import New_Advance_Blueprint
app.register_blueprint(New_Advance_Blueprint)

from project.api.funder.merchants.all_merchant_advances import All_Merchant_Advances_Blueprint
app.register_blueprint(All_Merchant_Advances_Blueprint)

from project.api.funder.merchants.merchant_details.merchant_details import Merchant_Details_Blueprint
app.register_blueprint(Merchant_Details_Blueprint)

from project.api.funder.merchants.merchant_details.display_images import Display_Images_Blueprint
app.register_blueprint(Display_Images_Blueprint)

from project.api.funder.merchants.merchant_details.edit_owners import Edit_Owners_Blueprint
app.register_blueprint(Edit_Owners_Blueprint)

from project.api.funder.merchants.merchant_details.kyc_update import KYC_Update_Blueprint
app.register_blueprint(KYC_Update_Blueprint)

from project.api.funder.merchants.merchant_profile.merchant_profile import Merchant_Profile_Blueprint
app.register_blueprint(Merchant_Profile_Blueprint)

from project.api.funder.merchants.merchant_profile.merchant_transactions import Merchant_Transactions_Blueprint
app.register_blueprint(Merchant_Transactions_Blueprint)

from project.api.funder.merchants.merchant_profile.bank_breakdown import Bank_Breakdown_Blueprint
app.register_blueprint(Bank_Breakdown_Blueprint)

from project.api.funder.merchants.merchant_profile.non_ach_payment import Non_ACH_Payment_Blueprint
app.register_blueprint(Non_ACH_Payment_Blueprint)

from project.api.funder.merchants.signnow_manager.signnow_manager import SignNow_Manager_Blueprint
app.register_blueprint(SignNow_Manager_Blueprint)

from project.api.funder.merchants.signnow_manager.contract_templates import Contract_Templates_Blueprint
app.register_blueprint(Contract_Templates_Blueprint)

# ------------------------------------- Syndicators -------------------------------------->

from project.api.funder.syndicators.syndicator_manager import Syndicator_Manager_Blueprint
app.register_blueprint(Syndicator_Manager_Blueprint)

from project.api.funder.syndicators.new_syndicator import New_Syndicator_Blueprint
app.register_blueprint(New_Syndicator_Blueprint)

from project.api.funder.syndicators.syndicator_details import Syndicator_Details_Blueprint
app.register_blueprint(Syndicator_Details_Blueprint)

from project.api.funder.syndicators.syndicator_presets import Syndicator_Presets_Blueprint
app.register_blueprint(Syndicator_Presets_Blueprint)

# ------------------------------------- ISOs -------------------------------------->

from project.api.funder.isos.iso_manager import ISO_Manager_Blueprint
app.register_blueprint(ISO_Manager_Blueprint)

from project.api.funder.isos.new_iso import New_ISO_Blueprint
app.register_blueprint(New_ISO_Blueprint)

from project.api.funder.isos.iso_details import ISO_Details_Blueprint
app.register_blueprint(ISO_Details_Blueprint)

# ------------------------------------- Users ---------------------------------------------->

from project.api.funder.users.user_manager import User_Manager_Blueprint
app.register_blueprint(User_Manager_Blueprint)

from project.api.funder.users.user_details import User_Details_Blueprint
app.register_blueprint(User_Details_Blueprint)

from project.api.funder.users.new_user import New_User_Blueprint
app.register_blueprint(New_User_Blueprint)

# ------------------------------------- Notifications -------------------------------------->

from project.api.funder.notifications.notifications import Notifications_Blueprint
app.register_blueprint(Notifications_Blueprint)

# ------------------------------------- Transactions --------------------------------------->

from project.api.funder.transactions.transactions import Transactions_Blueprint
app.register_blueprint(Transactions_Blueprint)

# ------------------------------------- Contact -------------------------------------------->

from project.api.funder.contact.contact import Funder_Contact_Blueprint
app.register_blueprint(Funder_Contact_Blueprint)

# ---------------------------------  Merchant  --------------------------------------------->

from project.api.merchant.merchant_home import Merchant_Home_Blueprint
app.register_blueprint(Merchant_Home_Blueprint)

from project.api.merchant.merchant_notifications import Merchant_Notifications_Blueprint
app.register_blueprint(Merchant_Notifications_Blueprint)

from project.api.merchant.plaid.secure_login import Secure_Login_Blueprint
app.register_blueprint(Secure_Login_Blueprint)

from project.api.merchant.plaid.secure_register import Secure_Register_Blueprint
app.register_blueprint(Secure_Register_Blueprint)

from project.api.merchant.plaid.plaid_confirm import Plaid_Confirm_Blueprint
app.register_blueprint(Plaid_Confirm_Blueprint)

from project.api.merchant.plaid.secure_account_select import Secure_Account_Select_Blueprint
app.register_blueprint(Secure_Account_Select_Blueprint)

from project.api.merchant.contact import Merchant_Contact_Blueprint
app.register_blueprint(Merchant_Contact_Blueprint)

# ---------------------------------  Syndicator  ------------------------------------------->

from project.api.syndicator.syndicator_home import Syndicator_Home_Blueprint
app.register_blueprint(Syndicator_Home_Blueprint)

from project.api.syndicator.merchant.synd_merchant_profile import Synd_Merchant_Profile_Blueprint
app.register_blueprint(Synd_Merchant_Profile_Blueprint)

from project.api.syndicator.merchant.synd_merchant_transactions import Synd_Merchant_Transactions_Blueprint
app.register_blueprint(Synd_Merchant_Transactions_Blueprint)

from project.api.syndicator.contact import Synd_Contact_Blueprint
app.register_blueprint(Synd_Contact_Blueprint)

from project.api.syndicator.register import Synd_Register_Blueprint
app.register_blueprint(Synd_Register_Blueprint)

# ---------------------------------  Login  ------------------------------------------------>

from project.api.login.login import Login_Blueprint
app.register_blueprint(Login_Blueprint)

from project.api.login.two_factor import Two_Factor_Blueprint
app.register_blueprint(Two_Factor_Blueprint)

from project.api.login.forgot_password import Forgot_Password_Blueprint
app.register_blueprint(Forgot_Password_Blueprint)

# ---------------------------------  Active_MCA_Master  ------------------------------------>

from project.api.master.data_upload import Data_Upload_Blueprint
app.register_blueprint(Data_Upload_Blueprint)

from project.api.master.active_mca_home import Active_Master_Home_Blueprint
app.register_blueprint(Active_Master_Home_Blueprint)

from project.api.master.funder_sign_up import Funder_Sign_Up_Blueprint
app.register_blueprint(Funder_Sign_Up_Blueprint)

from project.api.master.account_select import Account_Select_Blueprint
app.register_blueprint(Account_Select_Blueprint)

from project.api.master.master_plaid_confirm import Master_Plaid_Confirm_Blueprint
app.register_blueprint(Master_Plaid_Confirm_Blueprint)

# ---------------------------------  webhooks  --------------------------------------------->

from project.api.webhooks.dwolla_webhook import dwolla_webhook_Blueprint
app.register_blueprint(dwolla_webhook_Blueprint)

from project.api.webhooks.all_webhook_sub import all_webhook_sub_Blueprint
app.register_blueprint(all_webhook_sub_Blueprint)

from project.api.webhooks.ocrolus_webhook import ocrolus_webhook_Blueprint
app.register_blueprint(ocrolus_webhook_Blueprint)

from project.api.webhooks.signnow_webhook import signnow_webhook_Blueprint
app.register_blueprint(signnow_webhook_Blueprint)

# @app.template_filter('strftime')
# def _jinja2_filter_datetime(date):
# 	try:
# 		new_date = datetime.strptime(date, "%Y-%m-%d").strftime('%m/%d/%y')
# 	except:
# 		new_date = date
# 	return new_date


# @app.template_filter('currency_format')
# def _jinja2_currency_format(currency):
#     new_currency = '{:,}'.format(round(float(currency), 2))
#     print(new_currency, file=sys.stderr)
#     return new_currency

# @app.template_filter('whitespace_underscore')
# def _jinja2_whitespace_underscore(word):
#     underscored_word = word.replace("_", " ")
#     print(underscored_word, file=sys.stderr)
#     return underscored_word


# @app.template_filter('percent_color')
# def _jinja2_percent(percent):
#     if float(percent) >= 100:
#         new_color = '<span style="color:green">' + str(percent) + '%</span>'
#     elif float(percent) >= 60 and float(percent) < 100:
#         new_color = '<span style="color:#fcba03">' + str(percent) + '%</span>'
#     else:
#         new_color = '<span style="color:red">' + str(percent) + '%</span>'

#     return new_color



# @app.template_filter('status_color')
# def _jinja2_status(status_color):
#     if status_color == 'Open':
#         new_color = '<span style="color:green">Open</span>'
#     elif status_color == 'Prefund':
#         new_color = '<span style="color:#f5ed00">Prefund</span>'
#     elif status_color == 'Defaulted':
#         new_color = '<span style="color:orange">Defaulted</span>'
#     elif status_color == 'Collections':
#         new_color = '<span style="color:red">Collections</span>'
#     elif status_color == 'Legal':
#         new_color = '<span style="color:purple">Legal</span>'
#     else:
#        new_color = 'Closed'

#     return new_color

# @app.template_filter('fix_len')
# def _jinja2_fix_len(fix_len):
#     if '--- Primary ---' in fix_len:
#         fix_len = fix_len[:40] + ' ' + fix_len[40:]
#         #fix_len = fix_len[:85] + ' ' + fix_len[78:]
#     elif len(fix_len) > 39:
#         fix_len = fix_len[:36] + ' ' + fix_len[36:]
#     return fix_len


# Session(app)

	# return app

