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
            mysql_query("INSERT INTO pg_mst(UID,pg_name,pg_gender,addr_1,addr_2,area,city,state,pincode,total_rooms,prop_desc) VALUES({},'{}','{}','{}','{}','{}','{}','{}',{},{},'{}')".format(session['user_master']['UID'],request.form['pg_name'],request.form['pgtype'],request.form['adressline1'],request.form['adressline2'],request.form['area'],request.form['city'],request.form['state'],request.form['pincode'],request.form['total_rooms'],request.form['prop_desc'] ))
        
            PGID= mysql_query.last_row_id
            print(PGID)
            for x in request.form.getlist('common_facilities'):
                mysql_query("insert into facility_mst(PGID,amenity,amenity_type) values({},'{}','common')".format(PGID,x))
            for x in request.form.getlist('special_facilities'):
                mysql_query("insert into facility_mst(PGID,amenity,amenity_type) values({},'{}','special')".format(PGID,x))    
            
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
                    data = mysql_query("select image_1,image_2,image_3 from pg_mst")
                    print(data)
                    if data[0]['image_1'] is None:
                        print('done')
                        mysql_query("update pg_mst SET image_1='{}' where PGID={}".format(filename,PGID))
                    if data[0]['image_2'] is None:
                        mysql_query("update pg_mst SET image_2='{}' where PGID={}".format(filename,PGID))
                    if data[0]['image_3'] is None:
                        mysql_query("update pg_mst SET image_3='{}' where PGID={}".format(filename,PGID))
                    file_name=idproofPath 
                    print(file_name)
                    bucket="mittrisem"
                    object_name="pg_images/"+filename
                    upload_file(file_name=file_name, bucket=bucket, object_name=object_name)
           
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
    data = mysql_query("Select user_mst.email,pg_mst.pg_name from pg_mst inner join user_mst ON pg_mst.UID=user_mst.UID where user_mst.email='{}'".format(session['email']))
    # print(data)
    file_names = get_file_list_s3(bucket ='mittrisem',prefix='pg_images/')
    # print(file_names)
    cntr=-1
    for x in data:
        cntr = cntr+1
        length =x['email']+'_'+x['pg_name']
        xLen = len(length)
        lst=[]
        for y in file_names:
            if y[10:int(xLen+10)] == x['email']+'_'+x['pg_name']:
                print(y,cntr)
                lst.append(y[10:])
                dict = {'images':lst}
                data[int(cntr)].update(dict)
                print(data)    
        #    else:
        #         # print(x)
        #         dict = {'images':None}    
        #         data[int(cntr)].update(dict) 
               
                   
            
    return render_template('pgo/viewpg.html',data=data)

@pgo.route('/updatepg')
def updatepg():
    return render_template('pgo/updatepg.html')

@pgo.route('/rooms')
def rooms():
    return render_template('pgo/rooms.html')
