from flask import Blueprint, request, current_app, jsonify
from flask_session import Session
import sys
from project.api.mail import mail
from project import db
from random import randint
from flask_mail import Message
import bcrypt
from project.api.models import User

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies

Login_Blueprint = Blueprint('MCA_Login', __name__)
@Login_Blueprint.route('/api/login/login/', methods=['GET', 'POST']) # <- from '/'
def MCA_Login():

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Here we do some code to make sure the username and password is correct.
    user = User(email, db)
    if user.id is None:
        return jsonify(msg="Account not registered"), 401
    if not user.check_password(password):
        return jsonify(msg="Incorrect password"), 401

    # Set access token. 
    two_factor_code = '111'
    two_factor_recipient = current_app.config['EMAIL_LIST'].split(';')

    if current_app.config['ENV'] == 'production':
        two_factor_code = randint(100000, 999999)
        two_factor_recipient = [user.email]

    user.update_two_factor_code(code=two_factor_code, db=db)

    # Send access token to via email
    msg = Message(sender="getresources@fastmail.com",
        recipients=two_factor_recipient,
        subject="GET - 2 Factor Code",
        body="Please Use The Following Code: \n \n " + str(two_factor_code)
    )
    # mail.send(msg)

    # Set cookies so that we have an identity to check the two factor code for in the next step.
    # access_token = create_access_token(identity=user)
    response = jsonify({"msg": "Credentials are good"})
    # set_access_cookies(response, access_token)

    # Return message and redirect to MFA page.
    
    return response, 201