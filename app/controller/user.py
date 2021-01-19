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



@user.route('/bookingstatus',methods=['GET','POST'])
def userbookinginfo():
	uid=mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	if request.method=="POST":
		if "button1" in request.form:
			value=request.form['button1']
			data=mysql_query("select user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Deactivated"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "button2" in request.form:
			value=request.form['button2']
			data=mysql_query("select user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Activated"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "button3" in request.form:
			value=request.form['button3']
			data=mysql_query("select user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Declined"))
			return render_template('user/userbooking.html',data=data,value=value)

	return render_template('user/userbooking.html')

@user.route('/pg_details')
def pg_details():
	return render_template('user/pg_details.html')


