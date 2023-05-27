from flask import Blueprint, session, url_for, request, jsonify
from flask_session import Session
import sys
from project import db
from project.api.models import User

from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


Two_Factor_Blueprint = Blueprint('MCA_Two_Factor', __name__)
@Two_Factor_Blueprint.route('/Login/Two_Factor/', methods=['GET', 'POST']) # <- from '/'
@jwt_required
def MCA_Two_Factor():

    code = request.json.get('two_factor', None)
    if code is None:
        return jsonify({'msg': 'No code entered.'}), 400
        
    if int(code) == int(current_user.two_factor_code):
        return jsonify({'msg': 'Access token is valid.'}), 201

    else:
        # Possibly want to unset tokens and have them log in again.
        # Not sure what the best practice is.
        return jsonify({'msg': 'Token is invalid'})