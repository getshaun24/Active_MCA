from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
import gridfs
import codecs
import magic
import base64
from base64 import b64encode
from project import db
from flask_login import login_required


Display_Images_Blueprint = Blueprint('MCA_Display_Images', __name__)
@Display_Images_Blueprint.route('/api/funder/merchants/merchant_details/display_images/', methods=['GET', 'POST']) # <- from '/'
@login_required
def MCA_Display_Images():



    if session.get("access_status") != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]

    image_var_full = request.args.get('image_var', None)
    company_id_var = image_var_full[-32:]
    image_var = image_var_full[:-35]

    print('company_id_var', company_id_var, file=sys.stderr)
    print('image_var', image_var, file=sys.stderr)

    fs = gridfs.GridFS(mongoDB)

    image = fs.get_last_version(filename=image_var)
    print('1111111111111', image, file=sys.stderr)
    print('1111111111111', file=sys.stderr)
    base64_data = codecs.encode(image.read(), 'base64')
    print('2222222222222', file=sys.stderr)
    image = base64_data.decode('utf-8')
    print('3333333333333', image, file=sys.stderr)

    m = magic.Magic()
    media_type = m.from_buffer(base64.b64decode(image))

    print('media_type', media_type, file=sys.stderr)
    print('44444444', file=sys.stderr)

    is_pdf = False
    if 'PDF' in media_type:
        print('is_pdf  !!!   !!!   !!!   !!!', file=sys.stderr)
        is_pdf = True




    if request.method == 'POST':
        session.clear()
        return redirect("MCA_Public_Homepage")



    return render_template("/Funder/Merchants/Merchant_Details/Display_Images/display_images.html", company_id_var=company_id_var, is_pdf=is_pdf, access_status=session.get('access_status'), notification_count=session.get('notification_count'), image=image)
