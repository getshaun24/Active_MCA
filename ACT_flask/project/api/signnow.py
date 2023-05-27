import signnow_python_sdk
from flask import current_app, g
from werkzeug.local import LocalProxy

def get_signnow_token():

	signnow_access_token = getattr(g, "_signnow_access_token", None)
	
	if signnow_access_token is None:
		signnow_python_sdk_config = signnow_python_sdk.Config(client_id=current_app.config['SIGNNOW_ID'], client_secret=current_app.config['SIGNNOW_SERCRET'], environment=current_app.config['SIGNNOW_ENV'])
		signnow_bearer_token = signnow_python_sdk.OAuth2.request_token(current_app.config['SIGNNOW_USERNAME'], current_app.config['SIGNNOW_PASS'], '*')
		signnow_access_token = g._signnow_access_token = signnow_bearer_token['access_token']

	return signnow_access_token

signnow_access_token = LocalProxy(get_signnow_token)
