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



@user.route('/')
@user.route('/pg_ads',methods=['GET','POST'])
def pg_ads():
	data = mysql_query("Select pg_mst.status,pg_mst.pgid,pg_mst.hidden,pg_name,pg_mst.addr_1,pg_mst.addr_2,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email,GROUP_CONCAT(facility_mst.amenity) as facilities from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid inner join facility_mst on facility_mst.pgid=pg_mst.pgid group by pg_mst.pgid")
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
			data = mysql_query("Select pg_mst.status,pg_mst.hidden,pg_mst.pgid,user_mst.email,pg_mst.pgid,pg_mst.pg_name,pg_mst.addr_1,pg_mst.addr_2,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc, GROUP_CONCAT(facility_mst.amenity) as facilities from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid inner join facility_mst on facility_mst.pgid=pg_mst.pgid group by pg_mst.pgid having pg_mst.pg_name ='{}' or pg_mst.pg_gender='{}' or pg_mst.area ='{}' ".format(pgname,gen,area))
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
			data=mysql_query("select booking_mst.uid,booking_mst.bid,booking_mst.pgid,user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount,room_mst.rent from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid join room_mst on booking_mst.rid=room_mst.rid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Activated"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "button3" in request.form:
			value=request.form['button3']
			data=mysql_query("select user_mst.phone,pg_mst.pg_gender,pg_mst.pg_name,user_mst.fname,user_mst.lname,booking_mst.book_date,pg_mst.area,pg_mst.city,booking_mst.amount from pg_mst join user_mst on pg_mst.uid=user_mst.uid join booking_mst on booking_mst.pgid=pg_mst.pgid where booking_mst.UID={} and booking_mst.status='{}'".format(uid[0]['uid'],"Declined"))
			return render_template('user/userbooking.html',data=data,value=value)
		elif "payment" in request.form:
			bid=request.form['bid']
			mysql_query("INSERT INTO transaction_mst VALUES('{}','{}','{}',{})".format(tid,tdate,'success',bid))
			return redirect(url_for('user.paymentpage'))
	return render_template('user/userbooking.html')

@user.route('/pg_details',methods=['GET','POST'])
def pg_details():
	if request.method == "POST":
		uid=mysql_query("select uid from user_mst where email='{}'".format(session['email']))
		pgid=request.form['pgid']
		book_amt=request.form['amt']
		data = mysql_query("Select room_mst.RID,room_mst.PGID from room_mst where room_mst.RID={}".format(request.form['booking']))
		mysql_query("insert into booking_mst(PGID,RID,UID,amount) values({},{},{},{})".format(data[0]['PGID'],data[0]['RID'],uid[0]['uid'],book_amt))
		data = mysql_query("select * from user_mst inner join pg_mst ON user_mst.UID=pg_mst.UID where pg_mst.pgid={}".format(pgid))
		rdata=mysql_query("select * from room_mst where pgid={}".format(pgid))

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
		return render_template('user/pg_details.html',data=data,amenity_com_selected=amenity_com_selected,amenity_com_unselected=amenity_com_unselected,amenity_spe_selected=amenity_spe_selected,amenity_spe_unselected=amenity_spe_unselected,pgid=pgid,rdata=rdata)

	pgid = request.args.get('PGID')
	data = mysql_query("select * from user_mst inner join pg_mst ON user_mst.UID=pg_mst.UID where pg_mst.pgid={}".format(pgid))
	rdata=mysql_query("select * from room_mst where pgid={}".format(pgid))

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
	return render_template('user/pg_details.html',data=data,amenity_com_selected=amenity_com_selected,amenity_com_unselected=amenity_com_unselected,amenity_spe_selected=amenity_spe_selected,amenity_spe_unselected=amenity_spe_unselected,pgid=pgid,rdata=rdata)



@user.route('/Payment_Status')
def payment():
	uid=mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	data=mysql_query("select pg_mst.pg_name,pg_mst.pg_gender,user_mst.phone,user_mst.fname,user_mst.lname,transaction_mst.tstatus,pg_mst.area,pg_mst.city,transaction_mst.tid,transaction_mst.date from transaction_mst inner join booking_mst on transaction_mst.bid=booking_mst.bid inner join pg_mst on booking_mst.pgid=pg_mst.pgid inner join user_mst on user_mst.uid=pg_mst.uid where booking_mst.uid={}".format(uid[0]['uid']))
	return render_template('user/userpayment.html',data=data)


@user.route('/favourites',methods=['GET','POST'])
def favourites():
	uid = mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	data=mysql_query("select wishlist.wid,wishlist.pgid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.total_rooms from wishlist inner join pg_mst on wishlist.pgid=pg_mst.pgid where wishlist.uid='{}'".format(uid[0]['uid']))
	if request.method=="POST":
	 	if "button1" in request.form:
	 		uid = mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	 		pgid=request.form['button1']
	 		mysql_query("INSERT into wishlist(pgid,uid) values({},{})".format(pgid,uid[0]['uid']))
	 		return redirect(url_for('user.pg_details',PGID=pgid))
	 	if "delete" in request.form:
	 		wid=request.form['delete']
	 		mysql_query("DELETE from wishlist where wid={}".format(wid))
	 		return redirect(url_for('user.favourites'))
	 	if "view" in request.form:
	 		pgid=request.form['view']
	 		return redirect(url_for('user.pg_details',PGID=pgid))
	return render_template('user/favourites.html',data=data)


@user.route('/paymentpage',methods=['GET','POST'])
def paymentpage():
	if "button1" in request.form:
		return redirect(url_for('user.otp'))
	return render_template('user/payment.html')


@user.route('/otp',methods=['GET','POST'])
def otp():
	if "button1" in request.form:
		return redirect(url_for('user.transaction'))
	return render_template('user/otp.html')

@user.route('/transaction Complete',methods=['GET','POST'])
def transaction():
	uid = mysql_query("select uid from user_mst where email='{}'".format(session['email']))
	data=mysql_query("select tid,transaction_mst.date,tstatus,pg_name,fname,lname from booking_mst join transaction_mst on booking_mst.bid=transaction_mst.bid join pg_mst on booking_mst.pgid=pg_mst.pgid join user_mst on pg_mst.uid=user_mst.uid  where booking_mst.uid='{}' order by transaction_mst.tid DESC limit 1".format(uid[0]['uid']))
	if "button1" in request.form:
		return redirect(url_for('user.payment'))
	return render_template('user/transaction.html',data=data)
