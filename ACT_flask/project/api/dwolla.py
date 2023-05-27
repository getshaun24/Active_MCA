import dwollav2
from flask import current_app, g
from werkzeug.local import LocalProxy

def get_dwolla_token():

	# dwolla_app_token = getattr(g, "_dwolla_token", None)

	# if dwolla_app_token is None:
		
	dwolla_client = dwollav2.Client(key=current_app.config['DWOLLA_APP_KEY'], secret=current_app.config['DWOLLA_APP_SECRET'], environment=current_app.config['DWOLLA_APP_ENV']) # optional - defaults to production
	dwolla_app_token = g._dwolla_token = dwolla_client.Auth.client()

	return dwolla_app_token

dwolla_app_token = LocalProxy(get_dwolla_token)