import os
from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException,RequestEntityTooLarge
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import string

from werkzeug.utils import secure_filename
from .controller import *
 
pgo = Blueprint('pgo', 
                __name__,
                url_prefix='/pgo',
                template_folder='templates',
                static_folder='static/auth')

@pgo.app_errorhandler(HTTPException)
@pgo.app_errorhandler(RequestEntityTooLarge)
@pgo.app_errorhandler(413)
def handle_exception(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response



@pgo.route('/')
def pgotest():
    return render_template('pgo/pgo_dashboard.html')

@pgo.route('/addpg',methods=['POST','GET'])
def addpg():
    if request.method == "POST":
        #! FILE UPLOAD LIMIT IS 5 MB.
        try:
            allfiles = request.files.getlist('files')
            print(allfiles)
            for file in allfiles:
                if file.filename == '':
                    print('No file selected')
                    return 'No file selected'
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = str(session['email']+'_'+filename)
                    print("filename:   "+str(filename))
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    idproofPath = os.path.join(dir_path,"uploads",filename)
                    file.save(idproofPath)
        
            mysql_query("INSERT INTO pg_mst(UID,pg_name,pg_gender,addr_1,addr_2,area,city,state,pincode,total_rooms,prop_desc) VALUES({},'{}','{}','{}','{}','{}','{}','{}',{},{},'{}')".format(session['user_master']['UID'],request.form['pg_name'],request.form['pgtype'],request.form['adressline1'],request.form['adressline2'],request.form['area'],request.form['city'],request.form['state'],request.form['pincode'],request.form['total_rooms'],request.form['prop_desc'] ))
        
            PGID= mysql_query.last_row_id
            print(PGID)
            for x in request.form.getlist('common_facilities'):
                mysql_query("insert into facility_mst(PGID,amenity,amenity_type) values({},'{}','common')".format(PGID,x))
            for x in request.form.getlist('special_facilities'):
                mysql_query("insert into facility_mst(PGID,amenity,amenity_type) values({},'{}','special')".format(PGID,x))    
            
        except Exception as e:
            print(e)
            flash(str(e),'danger')
            return redirect(url_for('pgo.addpg'))
        else:
            flash('PG Added.','success')
            return redirect(url_for('pgo.addpg'))
    return render_template('pgo/addpg.html')

@pgo.route('/viewpg')
def viewpg():
    return render_template('pgo/viewpg.html')

