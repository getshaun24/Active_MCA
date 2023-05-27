from project.api.models import User
from flask_login import logout_user, login_required

# Load user in current session
# @login_manager.user_loader
# def load_user(user_id):
#     user = User(email=user_id, db=mongoDB_master_access)
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
#     logout_user()
#     session.clear()
#     return redirect(url_for('MCA_Public_Homepage'))