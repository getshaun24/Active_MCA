from flask_mail import Mail
from flask import current_app, g
from werkzeug.local import LocalProxy

def get_mail():
	if '_mail' not in g:
		mail = g._mail = Mail(current_app)
	return mail

mail = LocalProxy(get_mail)