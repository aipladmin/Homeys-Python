from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import string
from .controller import *
 
user = Blueprint('user',
                __name__,
                url_prefix='/user',
                template_folder='templates',
               static_folder='static/auth')

@user.app_errorhandler(HTTPException)
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

@user.app_errorhandler(HTTPException)
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

  
@user.route('/')
def user_dash():
    return render_template('user/user_dashboard.html')

# @user.route('/usernd')


@user.route('/pg_ads')
def pg_ads():
    return render_template('user/pg_ads.html')

# search Pg function Starts From here :

@user.route('/Search_pg')
def searchpg():
    data = mysql_query("Select pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email  from pg_mst join user_mst where utmid={}".format(2))
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



    return render_template('user/searchpg.html',data=data)

# Searh pg ends here 

