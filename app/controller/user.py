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
@user.route('/pg_ads')
def pg_ads():
	data = mysql_query("Select pg_mst.pg_name,pg_mst.addr_1,pg_mst.addr_2,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email,GROUP_CONCAT(facility_mst.amenity) as facilities from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid inner join facility_mst on facility_mst.pgid=pg_mst.pgid group by pg_mst.pgid")
	file_names = get_file_list_s3(bucket='mittrisem', prefix='pg_images/')
	# print(file_names)
	cntr = -1
	for x in data:
		cntr = cntr + 1
		length = x['email'] + '_' + x['pg_name']
		xLen = len(length)
		lst = []
		for y in file_names:
			if y[10:int(xLen + 10)] == x['email'] + '_' + x['pg_name']:
				print(y, cntr)
				lst.append(y[10:])
				dict = {'images': lst}
				data[int(cntr)].update(dict)
			print(data)

	return render_template('user/pg_ads.html',data=data)


@user.route('/search',methods=['POST','GET'])
def search():
	if request.method == "POST":
		if "button1" in request.form:
			pgname=request.form['byname']
			gen=request.form['sel1']
			area=request.form['byarea']
			data = mysql_query("Select user_mst.email,pg_mst.pgid,pg_mst.pg_name,pg_mst.addr_1,pg_mst.addr_2,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc, GROUP_CONCAT(facility_mst.amenity) as facilities from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid inner join facility_mst on facility_mst.pgid=pg_mst.pgid group by pg_mst.pgid having pg_mst.pg_name='{}' or pg_mst.pg_gender='{}' or pg_mst.area='{}' ".format(pgname,gen,area))
			for x in data:
				print(x['pgid'])
			file_names = get_file_list_s3(bucket='mittrisem', prefix='pg_images/')
			# print(file_names)
			cntr = -1
			for x in data:
				cntr = cntr + 1
				length = x['email'] + '_' + x['pg_name']
				xLen = len(length)
				lst = []
				for y in file_names:
					if y[10:int(xLen + 10)] == x['email'] + '_' + x['pg_name']:
						print(y, cntr)
						lst.append(y[10:])
						dict = {'images': lst}
						data[int(cntr)].update(dict)
					
			print(data)	
			return render_template('user/pg_ads.html',data=data)
	return render_template('user/pg_ads.html')