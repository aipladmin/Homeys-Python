from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import string
from .controller import *
import random
import string
from datetime import date
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
	data = mysql_query("Select pg_mst.pgid,pg_name,pg_mst.addr_1,pg_mst.addr_2,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email,GROUP_CONCAT(facility_mst.amenity) as facilities from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid inner join facility_mst on facility_mst.pgid=pg_mst.pgid group by pg_mst.pgid")
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
			# print(data)

	return render_template('user/pg_ads.html',data=data)


@user.route('/search',methods=['POST','GET'])
def search():
	if request.method == "POST":
		if "button1" in request.form:
			pgname=request.form['byname']
			gen=request.form['sel1']
			area=request.form['byarea']
			data = mysql_query("Select pg_mst.pgid,user_mst.email,pg_mst.pgid,pg_mst.pg_name,pg_mst.addr_1,pg_mst.addr_2,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc, GROUP_CONCAT(facility_mst.amenity) as facilities from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid inner join facility_mst on facility_mst.pgid=pg_mst.pgid group by pg_mst.pgid having pg_mst.pg_name ='{}' or pg_mst.pg_gender='{}' or pg_mst.area ='{}' ".format(pgname,gen,area))
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
	tdate=date.today()
	# code to generate random transaction id 
	letters_and_digits=string.ascii_letters + string.digits
	tid=''.join((random.choice(letters_and_digits) for i in range(8)))
	if request.method=="POST":
		if "button1" in request.form:
			value=request.form['button1']
			data=mysql_query("select user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid  where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Deactivated"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "button2" in request.form:
			value=request.form['button2']
			data=mysql_query("select booking_mst.uid,booking_mst.rid,booking_mst.pgid,user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount,room_mst.rent from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid join room_mst on booking_mst.rid=room_mst.rid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Activated"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "button3" in request.form:
			value=request.form['button3']
			data=mysql_query("select user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Declined"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "payment" in request.form:
			rid=request.form['rid']
			pgid=request.form['pgid']
			uid=request.form['uid']
			mysql_query("INSERT INTO transaction_mst VALUES('{}',{},{},{},'{}','{}')".format(tid,uid,pgid,rid,tdate,'success'))
			return render_template('user/userbooking.html')
	return render_template('user/userbooking.html')

@user.route('/pg_details',methods=['GET','POST'])
def pg_details():
	pgid = request.args.get('PGID')
	data = mysql_query("select * from user_mst inner join pg_mst ON user_mst.UID=pg_mst.UID where pg_mst.pgid={}".format(pgid))


	#common amenities
	amenity_com=mysql_query("select amenity from facility_mst where pgid='{}' and amenity_type='{}'".format(pgid,"common"))
	
	amenity_com_list=[]
	for x in amenity_com:
		amenity_com_list.append(x['amenity'])

	#special amenities
	amenity_spe=mysql_query("select amenity from facility_mst where pgid='{}' and amenity_type='{}'".format(pgid,"special"))	
	amenity_spe_list=[]
	for x in amenity_spe:
		amenity_spe_list.append(x['amenity'])

	#making list of facilities
	common=["AC","Cooking Allowed","Food","Parking","Laundry","Television","Guests Allowed"]
	special=["GYM","Swimming","Pool","Vehicles Provided","Dry Cleaning"]
	
	# The Variable Passed
	amenity_com_selected=[]
	amenity_com_unselected =[]
	for x in common:
		if x in amenity_com_list:
			amenity_com_selected.append(x)
		else:
			amenity_com_unselected.append(x)
	print("Selected",set(amenity_com_selected),"Unselected",set(amenity_com_unselected))

	# The variable Passed
	amenity_spe_selected=[]
	amenity_spe_unselected =[]
	for x in special:
		if x in amenity_spe_list:
			amenity_spe_selected.append(x)
		else:
			amenity_spe_unselected.append(x)

	# if request.method == "POST":
	# 	if "button1" in request.form:
	# 		uid = mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	# 		pgid = request.form['button1']
	# 		print("######################################################################")
	# 		print(pgid)
	# 		mysql_query("INSERT into wishlist values({},{},{})".format(1,pgid,uid[0]['uid']))
	# 		return redirect(url_for('user.pg_details',PGID=pgid))

	return render_template('user/pg_details.html',data=data,amenity_com_selected=amenity_com_selected,amenity_com_unselected=amenity_com_unselected,amenity_spe_selected=amenity_spe_selected,amenity_spe_unselected=amenity_spe_unselected)


@user.route('/Payment Status')
def payment():
	uid=mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	data=mysql_query("select pg_mst.pg_name,pg_mst.pg_gender,user_mst.phone,user_mst.fname,user_mst.lname,transaction_mst.status,pg_mst.area,pg_mst.city,transaction_mst.tid,transaction_mst.date from transaction_mst inner join pg_mst on transaction_mst.pgid=pg_mst.pgid inner join user_mst on pg_mst.uid=user_mst.uid where transaction_mst.uid={}".format(uid[0]['uid']))
	return render_template('user/userpayment.html',data=data)


@user.route('/favourites')
def favourites():
	return render_template('user/favourites.html')
