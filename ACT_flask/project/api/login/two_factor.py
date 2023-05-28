from flask import Blueprint, session, url_for, request, jsonify
from flask_session import Session
import sys
from project import db
from project.api.models import User

from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies, create_access_token


Two_Factor_Blueprint = Blueprint('MCA_Two_Factor', __name__)
@Two_Factor_Blueprint.route('/api/login/two_factor/', methods=['GET', 'POST']) # <- from '/'
def MCA_Two_Factor():

    email = request.json.get('email', None)
    two_factor = request.json.get('two_factor', None)

    if two_factor is None or two_factor == "":
        return jsonify({'msg':'Two factor code not entered'}), 401

    user = User(email=email, db=db)
    if int(two_factor) != int(user.two_factor_code):
        return jsonify({'msg': 'Code is not correct'}), 401


    # try:
    #     investor_info = db.investor_info.find_one({ "investor_ID": user.user_id })
    #     dashboard_config = investor_info['dashboard_config']
    # except:
    #     dashboard_config = 'None'


    access_token = create_access_token(identity=user)
    response = jsonify({'msg':'Login successful', 'access_status':user.access_status})
    set_access_cookies(response, access_token)


    return response, 200