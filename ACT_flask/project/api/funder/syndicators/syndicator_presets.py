from flask import Blueprint, session, url_for, request, redirect, render_template
from flask_session import Session
import pymongo
import sys
from project import db


Syndicator_Presets_Blueprint = Blueprint('MCA_Syndicator_Presets', __name__)
@Syndicator_Presets_Blueprint.route('/api/funder/syndicators/syndicator_presets/', methods=['GET', 'POST']) 
def MCA_Syndicator_Presets():

    access_status = session.get('access_status')

    if access_status != 'admin':
        return redirect(url_for('logout'))


    mongoDB = db[session.get("user_database")]

    notification_count = session.get('notification_count')


    all_syndicators = []
    for synd in mongoDB.Syndicators.find():
        all_syndicators.append(synd['syndicator_business_name'])
    all_syndicators = sorted(all_syndicators, key=lambda v: (v.upper(), v[0].islower()))


    # Gets Syndicator presets and transforms the dict into a nested array
    preset_count = 1
    all_presets = []
    preset_names = []
    for preset in mongoDB.Synd_preset.find():
        kv_list = []
        for k, v in preset['preset_dict'].items():
            if k == 'preset_name':
                preset_names.append(v)
            kv_list.append([k, v])
        all_presets.append(kv_list)
        preset_count += 1

    print("preset ------------------->>  ", all_presets, file=sys.stderr)
    preset_len = len(all_presets)
    print("preset_len ------------------->>  ", preset_len, file=sys.stderr)



    if request.method == 'POST':


        form_data = request.form
        print(form_data, file=sys.stderr)


        try:
            delete_it = form_data["preset_del"]
            print("DELETE IT: -------> ", delete_it, file=sys.stderr)
            if delete_it:
                for preset in mongoDB.Synd_preset.find():
                    print("preset id: -------> ", preset["_id"], file=sys.stderr)
                    for k, v in preset['preset_dict'].items():
                        print("kk ", v, file=sys.stderr)
                        if v == delete_it:
                            print("deleting: -------> ", file=sys.stderr)
                            mongoDB.Synd_preset.delete_one({ "_id": preset["_id"] })
                            return redirect(url_for('MCA_Syndicator_Manager'))

        except:
            print("Did not delete", file=sys.stderr)



        print("11111 ------------------->>  ", file=sys.stderr)


        preset_dict = {}
        preset_dict['preset_name'] = form_data['preset_name']
        for elm in all_syndicators:
            if form_data[elm] != '':
                print("elm ------------------->>  ", form_data[elm], file=sys.stderr)
                preset_dict[elm] = form_data[elm]



        print("preset_dict ------------------->>  ", preset_dict, file=sys.stderr)

        set_preset = {"preset_dict": preset_dict}

        mongoDB.Synd_preset.insert_one(set_preset)



    return render_template("/Funder/Syndicators/Syndicator_Presets/syndicator_presets.html", preset_names=preset_names, all_presets=all_presets, all_syndicators=all_syndicators, access_status=access_status, notification_count=notification_count)
