from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
from .controller import *

admin = Blueprint('admin',
				 __name__,
				 template_folder='templates',
				 static_folder='static/auth',
				 url_prefix='/admin')

@admin.app_errorhandler(HTTPException)
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

@admin.route('/adminDashboard')
def admindashboard():
	pdata=mysql_query("select count(pgid) as pg from pg_mst")
	odata=mysql_query("select count(uid)  from user_mst where utmid={}".format(2))
	udata=odata=mysql_query("select count(uid) from user_mst where utmid={}".format(3))
	return render_template('admin/admin_dashboard.html',pdata=pdata,odata=odata,udata=udata)

@admin.route('/Ownerdetails',methods=['GET','POST'])
def owner():
	data=mysql_query("select uid,fname,email,gender,dob,id_proof,authorised from user_mst where utmid={}".format(2))
	if request.method=="POST":
		if "button1" in request.form:
			id=request.form['button1']
			print(id)
			mysql_query("UPDATE user_mst SET authorised='{}' where uid={}".format("Deactivated",id))
			return redirect(url_for('admin.owner'))
		if "button2" in request.form:
			id=request.form['button2']
			mysql_query("UPDATE user_mst SET authorised='{}' where uid={}".format("Activated",id))
			return redirect(url_for('admin.owner'))
	return render_template('admin/ownerinfo.html',data=data)

@admin.route('/userdetails',methods=['GET','POST'])
def user():
	data=mysql_query("select uid,fname,email,gender,dob,id_proof,authorised from user_mst where utmid={}".format(3))
	if request.method=="POST":
		if "button1" in request.form:
			id=request.form['button1']
			print(id)
			mysql_query("UPDATE user_mst SET authorised='{}' where uid={}".format("Deactivated",id))
			return redirect(url_for('admin.owner'))
		if "button2" in request.form:
			id=request.form['button2']
			mysql_query("UPDATE user_mst SET authorised='{}' where uid={}".format("Activated",id))
			return redirect(url_for('admin.owner'))
	return render_template('admin/ownerinfo.html',data=data)

@admin.route('/pgdetails',methods=['GET','POST'])
def pg():
	data=mysql_query("select pg_mst.pgid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.status,fname,lname from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid")
	if request.method=="POST":
		if "button1" in request.form:
			id=request.form['button1']
			mysql_query("UPDATE pg_mst SET status='{}' where pgid={}".format("Deactivated",id))
			return redirect(url_for('admin.pg'))
		if "button2" in request.form:
			id=request.form['button2']
			mysql_query("UPDATE pg_mst SET status='{}' where pgid={}".format("Activated",id))
			return redirect(url_for('admin.pg'))
	return render_template('admin/pginfo.html',data=data)


@admin.route('/generatereports')
def report():
	return render_template('admin/reports.html')

@admin.route('/userwise',methods=['GET','POST'])
def userwise():
	if request.method=="POST":
		usertype=request.form['usertype']
		city=request.form['city']
		state=request.form['state']
		authorization=request.form['authorization']	
		print(usertype)
		if "button1" in request.form:
			if usertype=='Owner':
				res=mysql_query("select UID,fname,lname,email,phone,gender,dob,authorised,addr1,addr2,area,city,state from user_mst where UTMID={} AND (city='{}' OR state='{}' OR authorised='{}');".format(2,city,state,authorization))
				print(res)
				return render_template('admin/userwise.html',res=res,usertype=usertype)
			elif usertype=='User':
				res=mysql_query("select UID,fname,lname,email,phone,gender,dob,authorised,addr1,addr2,area,city,state from user_mst where UTMID={} AND (city='{}' OR state='{}' OR authorised='{}');".format(3,city,state,authorization))
				print(res)
				return render_template('admin/userwise.html',res=res,usertype=usertype)
			else:
				res=mysql_query("select UID,fname,lname,email,phone,gender,dob,authorised,addr1,addr2,area,city,state from user_mst where UTMID='{}' OR city='{}' OR state='{}' OR authorised='{}';".format(usertype,city,state,authorization))
				print(res)
				return render_template('admin/userwise.html',res=res,usertype=usertype)
	return render_template('admin/userwise.html')


@admin.route('/pgownerwise',methods=['GET','POST'])
def pgownerwise():
	if request.method=="POST":
		evalue=request.form['button1']
		gender=request.form['gender']
		authorization=request.form['authorization']	
		fromdate=request.form['fromdate']
		todate=request.form['todate']
		if "button1" in request.form:
			res=mysql_query("select UID,fname,lname,email,phone,gender,dob,authorised,addr1,addr2,area,city,state,pincode,id_method,id_proof from user_mst where (UTMID={}) AND (gender='{}' AND authorised='{}' OR dob BETWEEN '{}' AND '{}');".format(2,gender,authorization,fromdate,todate))
			print(evalue)
			return render_template('admin/pgownerwise.html',res=res,evalue=evalue)
	return render_template('admin/pgownerwise.html')


@admin.route('/pgwise',methods=['GET','POST'])
def pgwise():
	if request.method=="POST":
		evalue=request.form['button1']
		pg_name=request.form['pg_name']
		total_rooms=request.form['total_rooms']
		preference=request.form['preference']
		hidden=request.form['hidden']
		city=request.form['city']
		if "button1" in request.form:
			res=mysql_query("select pg_mst.PGID,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.addr_1,pg_mst.addr_2,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.total_rooms,pg_mst.prop_desc,pg_mst.status,pg_mst.hidden,fname,lname,email,phone from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid WHERE pg_mst.pg_name='{}' OR pg_mst.total_rooms='{}' OR pg_mst.pg_gender='{}' OR pg_mst.hidden='{}' OR pg_mst.city='{}';".format(pg_name,total_rooms,preference,hidden,city))
			print(evalue)
			return render_template('admin/pgwise.html',res=res,evalue=evalue)
	return render_template('admin/pgwise.html')


@admin.route('/pgroomwise',methods=['GET','POST'])
def pgroomwise():
	if request.method=="POST":
		evalue=request.form['button1']
		total_beds=request.form['total_beds']
		hidden=request.form['hidden']
		rent=request.form['rent']
		token_amt=request.form['token_amt']
		if "button1" in request.form:
			res=mysql_query("select room_mst.*,pg_name,pg_gender,addr_1,addr_2,area,city,state,total_rooms,prop_desc from room_mst inner join pg_mst on room_mst.PGID=pg_mst.PGID WHERE room_mst.total_beds='{}' OR room_mst.rhidden='{}' OR room_mst.rent BETWEEN {} OR room_mst.token_amt BETWEEN {};".format(total_beds,hidden,rent,token_amt))			
			print(evalue)
			return render_template('admin/pgroomwise.html',res=res,evalue=evalue)
	return render_template('admin/pgroomwise.html')


@admin.route('/bookingwise',methods=['GET','POST'])
def bookingwise():
	if request.method=="POST":
		evalue=request.form['button1']
		status=request.form['status']
		fromdate=request.form['fromdate']
		todate=request.form['todate']
		booking_amt=request.form['booking_amt']
		if "button1" in request.form:
			res=mysql_query("select booking_mst.*,pg_mst.pg_name,pg_mst.pg_gender,room_mst.RID,room_mst.token_amt,user_mst.fname,user_mst.lname,user_mst.phone,transaction_mst.tid,transaction_mst.date,transaction_mst.tstatus from booking_mst INNER JOIN pg_mst ON booking_mst.PGID=pg_mst.PGID INNER JOIN room_mst ON booking_mst.RID=room_mst.RID INNER JOIN transaction_mst on transaction_mst.bid=booking_mst.BID INNER JOIN user_mst ON booking_mst.UID=user_mst.UID WHERE booking_mst.status='{}' OR booking_mst.amount BETWEEN {} OR (booking_mst.book_date BETWEEN '{}' AND '{}');".format(status,booking_amt,fromdate,todate))			
			print(evalue)
			print(res)
			return render_template('admin/bookingwise.html',res=res,evalue=evalue)
	return render_template('admin/bookingwise.html')


@admin.route('/feedbackwise',methods=['GET','POST'])
def feedbackwise():
	if request.method=="POST":
		evalue=request.form['button1']
		fromdate=request.form['fromdate']
		todate=request.form['todate']
		if "button1" in request.form:
			res=mysql_query("select feedback.*,user_mst.fname,user_mst.lname,user_mst.email from feedback INNER JOIN user_mst ON feedback.UID=user_mst.UID WHERE feedback.feed_date BETWEEN '{}' AND '{}';".format(fromdate,todate))			
			print(evalue)
			print(res)
			return render_template('admin/feedbackwise.html',res=res,evalue=evalue)
	return render_template('admin/feedbackwise.html')