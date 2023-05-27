from project.__init__ import app
if __name__ == "__main__":
    app.run(host='0.0.0.0')


# import requests
# import statistics
# import base64
# from base64 import b64encode
# #import magic  #commented for error
# import os
# import io
# import re
# import datetime
# import plaid
# from plaid.api import plaid_api
# import json
# import time
# from flask import Flask
# from flask import render_template
# from flask import request
# from flask import Response
# from flask import jsonify
# from flask import redirect
# from flask import session
# from flask_session import Session
# from flask import url_for
# from flask import flash
# from flask_mail import Mail
# from flask_mail import Message
# from datetime import datetime, timedelta
# import os
# from os.path import join, dirname, realpath
# import pandas as pd
# import uuid
# import atexit
# from apscheduler.schedulers.background import BackgroundScheduler
# import dwollav2
# import sys
# import pymongo
# import hmac  ## where is this used ?
# from hashlib import sha256
# import calendar
# import math
# import statistics
# from bson.json_util import dumps #for pymongo
# import gridfs #for pymongo
# from io import BytesIO
# import codecs
# import signnow_python_sdk
# from random import random
# from requests.auth import HTTPBasicAuth
# import bcrypt
# from ratelimit import limits
# from random import randint
# import webbrowser
# import requests



# start server --> ./run.sh

# local url --> http://127.0.0.1:5000/

# app = create_app(config)


# have both variables for redundancy as to not accidentaly set wrong
# DEVELOPMENT_ENV = True
# PRODUCTION_ENV = False

# Redundancy since it is set in the config file.
# app.config.update(ENV='development')

# is_live_production_env = False
# if DEVELOPMENT_ENV == False and PRODUCTION_ENV == True:
#     is_live_production_env = True




# app = Flask(__name__, template_folder="")


# if is_live_production_env == True:
    # app.run()
# else:
    # app.config["ENV"] = 'development' #auto reloads server on template changes -- should probably be turned off for production
    # app.run(debug=True) #remove debug for production
    # app.config["TEMPLATES_AUTO_RELOAD"] = True #auto reloads server on template changes -- should probably be turned off for production
    # app.secret_key = "active_mca" #makes the app run on local server - not sure what it does exactly -- probably do not need in production?


# MONGO_CLI = os.getenv('MONGO_CLI')
# mongo_client = pymongo.MongoClient(app.config['MONGO_CLI'], tls=True)
# mongoDB_master_access = mongo_client.Master_Credentials


# MAIL_SERVER = os.getenv('MAIL_SERVER')
# MAIL_PORT = os.getenv('MAIL_PORT')
# MAIL_USERNAME = os.getenv('MAIL_USERNAME')
# MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_SERVER']=MAIL_SERVER
# app.config['MAIL_PORT'] = MAIL_PORT
# app.config['MAIL_USERNAME'] = MAIL_USERNAME
# app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# mail = Mail(app)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


# SIGNNOW_ID = os.getenv('SIGNNOW_ID')
# SIGNNOW_SERCRET = os.getenv('SIGNNOW_SERCRET')
# SIGNNOW_USERNAME = os.getenv('SIGNNOW_USERNAME')
# SIGNNOW_PASS = os.getenv('SIGNNOW_PASS')
# SIGNNOW_BASIC_AUTH = os.getenv('SIGNNOW_BASIC_AUTH')
# signnow_python_sdk_config = signnow_python_sdk.Config(client_id=app.config['SIGNNOW_ID'], client_secret=app.config['SIGNNOW_SERCRET'], environment=app.config['SIGNNOW_ENV'])
# signnow_bearer_token = signnow_python_sdk.OAuth2.request_token(app.config['SIGNNOW_USERNAME'], app.config['SIGNNOW_PASS'], '*')
# signnow_access_token = signnow_bearer_token['access_token']


# DWOLLA_APP_KEY = os.getenv('DWOLLA_APP_KEY')
# DWOLLA_APP_SECRET = os.getenv('DWOLLA_APP_SECRET')
# dwolla_client = dwollav2.Client(key=app.config['DWOLLA_APP_KEY'], secret=app.config['DWOLLA_APP_SECRET'], environment=app.config['DWOLLA_APP_ENV']) # optional - defaults to production
# dwolla_app_token = dwolla_client.Auth.client()



# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
# PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
# PLAID_SECRET = os.getenv('PLAID_SECRET')
# PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
# PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS').split(',')
# PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')
# PLAID_REDIRECT_URI = None


# host = plaid.Environment.Sandbox
# # Will need to add production and test plaid env to config file eventually

# # if app.config['ENV'] == 'production':
# #     # host = something else
# plaid_configuration = plaid.Configuration(
#     host=host,
#     api_key={
#         'clientId': app.config['PLAID_CLIENT_ID'],
#         'secret': app.config['PLAID_SECRET'],
#     }
# )
# plaid_api_client = plaid.ApiClient(plaid_configuration)
# plaid_client = plaid_api.PlaidApi(plaid_api_client)



# OCROLUS_ID = os.getenv('OCROLUS_ID')
# OCROLUS_SECRET = os.getenv('OCROLUS_SECRET')

# ocrolus_url = "https://auth.ocrolus.com/oauth/token"
# ocrolus_payload = {
#     "grant_type": "client_credentials",
#     "audience": "https://api.ocrolus.com/",
#     "client_id": app.config['OCROLUS_ID'],
#     "client_secret": app.config['OCROLUS_SECRET']
# }
# ocrolus_headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json"
# }
# ocrolus_oauth_response = (requests.post(ocrolus_url, json=ocrolus_payload, headers=ocrolus_headers)).json()
# ocrolus_access_token = ocrolus_oauth_response['access_token']



# # Clearcheck is Obsolete  ---- Will be Lexis Nexis Soon

# @app.route('/Active_MCA_Master/Clearcheck_Connect/', methods=['GET', 'POST']) # <- from '/'
# def MCA_Clearcheck_Connect():


#     return render_template("/Active_MCA_Master/Clearcheck_Connect/clearcheck_connect.html", company_ID=company_ID)





# # ------------------------------------------------------------------------------------>
# # ---------------------------------  Public Pages  --------------------------------------------------->
# # ------------------------------------------------------------------------------------>


# #can make own page/blueprint eventually -- doing so requires going to everysingle page and updating the public homepage link

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




#---------------------------------------------------------------------------------------------------------------------->
#---------------------------------------------------------------------------------------------------------------------->
#---------------------------------------------------------------------------------------------------------------------->

# app = create_app(config)
# # app.config = config

# # Redundant
# app.config.update(ENV='development')


# # Clearcheck is Obsolete  ---- Will be Lexis Nexis Soon

# @app.route('/Active_MCA_Master/Clearcheck_Connect/', methods=['GET', 'POST']) # <- from '/'     
# def MCA_Clearcheck_Connect():
#     return render_template("/Active_MCA_Master/Clearcheck_Connect/clearcheck_connect.html", company_ID=company_ID)

# # ---------------------------------  Public Pages  --------------------------------------------------->

# #can make own page/blueprint eventually -- doing so requires going to everysingle page and updating the public homepage link

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

