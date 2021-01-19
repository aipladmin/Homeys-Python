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
	odata=mysql_query("select count(uid)  from user_mst where user_mst.utmid={}".format(2))
	udata=odata=mysql_query("select count(uid) from user_mst where user_mst.utmid={}".format(3))
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
	data=mysql_query("select pg_mst.pgid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.status,user_mst.fname,user_mst.lname from pg_mst inner join user_mst on pg_mst.uid=user_mst.uid")
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