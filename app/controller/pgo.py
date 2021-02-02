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

@pgo.route('/ownerdashboard')
@login_required
def ownerdashboard():
  return render_template('pgo/pgo_dashboard.html')

@pgo.route('/addpg',methods=['POST','GET'])
@login_required
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

@pgo.route('/viewpg',methods=['GET','POST'])
@login_required
def viewpg():
	data=mysql_query("Select pg_mst.pgid,pg_mst.hidden,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email from pg_mst join user_mst ON pg_mst.UID=user_mst.UID where user_mst.email='{}'".format(session['email']))
	# print(data)
	file_names = get_file_list_s3(bucket ='mittrisem',prefix='pg_images/')
	# print(file_names)
	cntr=-1
	for x in data:
		cntr = cntr+1
		length =x['email']+'_'+x['pg_name']
		# print(length)
		xLen = len(length)
		lst=[]
		for y in file_names:
			if y[10:int(xLen+10)] == x['email']+'_'+x['pg_name']:
				print(y[10:int(xLen+10)])
				lst.append(y[10:])
				dict = {'images':lst}
				# print(dict)
				data[int(cntr)].update(dict)
			# print(data)    
		#    else:
		#         # print(x)
		#         dict = {'images':None}    
		#         data[int(cntr)].update(dict) 
			   
	if request.method=="POST":
		if "hidepg" in request.form:
			pgid=request.form['pgid']
			
			mysql_query("UPDATE pg_mst set hidden='{}' where pgid={}".format("yes",pgid))
			data=mysql_query("Select pg_mst.pgid,pg_mst.hidden,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email from pg_mst join user_mst ON pg_mst.UID=user_mst.UID where user_mst.email='{}'".format(session['email']))
			# print(data)
			file_names = get_file_list_s3(bucket ='mittrisem',prefix='pg_images/')
			# print(file_names)
			cntr=-1
			for x in data:
				cntr = cntr+1
				length =x['email']+'_'+x['pg_name']
				# print(length)
				xLen = len(length)
				lst=[]
				for y in file_names:
					if y[10:int(xLen+10)] == x['email']+'_'+x['pg_name']:
						print(y[10:int(xLen+10)])
						lst.append(y[10:])
						dict = {'images':lst}
						# print(dict)
						data[int(cntr)].update(dict)
			return render_template('pgo/viewpg.html',data=data)
		if "unhidepg" in request.form:
			pgid=request.form['pgid']
			mysql_query("UPDATE pg_mst set hidden='{}' where pgid={}".format("no",pgid))
			data=mysql_query("Select pg_mst.pgid,pg_mst.hidden,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email from pg_mst join user_mst ON pg_mst.UID=user_mst.UID where user_mst.email='{}'".format(session['email']))
			# print(data)
			file_names = get_file_list_s3(bucket ='mittrisem',prefix='pg_images/')
			# print(file_names)
			cntr=-1
			for x in data:
				cntr = cntr+1
				length =x['email']+'_'+x['pg_name']
				# print(length)
				xLen = len(length)
				lst=[]
				for y in file_names:
					if y[10:int(xLen+10)] == x['email']+'_'+x['pg_name']:
						print(y[10:int(xLen+10)])
						lst.append(y[10:])
						dict = {'images':lst}
						# print(dict)
						data[int(cntr)].update(dict)
			return render_template('pgo/viewpg.html',data=data)
		if "deletepg" in request.form:
			pgid=request.form['pgid']
			mysql_query("DELETE from pg_mst where pgid={}".format(pgid))
			data = mysql_query("Select pg_mst.pgid,pg_mst.hidden,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc,user_mst.email from pg_mst join user_mst ON pg_mst.UID=user_mst.UID where user_mst.email='{}'".format(session['email']))
			# print(data)
			file_names = get_file_list_s3(bucket ='mittrisem',prefix='pg_images/')
			# print(file_names)
			cntr=-1
			for x in data:
				cntr = cntr+1
				length =x['email']+'_'+x['pg_name']
				# print(length)
				xLen = len(length)
				lst=[]
				for y in file_names:
					if y[10:int(xLen+10)] == x['email']+'_'+x['pg_name']:
						print(y[10:int(xLen+10)])
						lst.append(y[10:])
						dict = {'images':lst}
						# print(dict)
						data[int(cntr)].update(dict)
			return render_template('pgo/viewpg.html',data=data)			
	return render_template('pgo/viewpg.html',data=data)


#
#
#
def diff(list1, list2):
	out = []
	for ele in list1:
		if not ele in list2:
			out.append(ele)
	return out
#
@pgo.route('/updatepg',methods=['POST','GET'])
@login_required
def updatepg():
	#displaying pg information
	pgid=request.args.get('id')
	data=mysql_query("select pg_mst.pg_name,pg_mst.pg_gender,pg_mst.addr_1,pg_mst.addr_2,pg_mst.area,pg_mst.city,pg_mst.state,pg_mst.pincode,pg_mst.total_rooms,pg_mst.prop_desc from pg_mst where pg_mst.pgid='{}'".format(pgid)) 
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
			# print(x)
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
	print("Selected",set(amenity_spe_selected),"Unselected",set(amenity_spe_unselected))
	

	#Updating pg information with facilities and imges
	if request.method=='POST':
		pgid = request.form['submit']
		# uid=session['user_master']
		pg_name=request.form['pg_name']
		pg_gender=request.form['pg_type']
		area=request.form['area']
		addr_1=request.form['addressline1']
		addr_2=request.form['addressline2']
		city=request.form['city']
		state=request.form['state']
		pincode=request.form['pincode']
		total_rooms=request.form['total_rooms']
		prop_desc=request.form['prop_desc']
		mysql_query("UPDATE pg_mst set pg_name='{}',pg_gender='{}',addr_1='{}',addr_2='{}',area='{}',city='{}',state='{}',pincode={},total_rooms={},prop_desc='{}' where pgid={}".format(pg_name,pg_gender,addr_1,addr_2,area,city,state,pincode,total_rooms,prop_desc,pgid))
		mysql_query("delete from facility_mst where pgid={}".format(pgid))
		for x in request.form.getlist('common_facilities'):
			mysql_query("insert into facility_mst(PGID,amenity,amenity_type) values({},'{}','common')".format(pgid,x))
		for x in request.form.getlist('special_facilities'):
			mysql_query("insert into facility_mst(PGID,amenity,amenity_type) values({},'{}','special')".format(pgid,x))    
		return redirect(url_for('pgo.updatepg',id=pgid))
	
	return render_template('pgo/updatepg.html',pgid=pgid,data=data,
							amenity_com_selected=amenity_com_selected,amenity_com_unselected=amenity_com_unselected,amenity_spe_selected=amenity_spe_selected,amenity_spe_unselected=amenity_spe_unselected)


@pgo.route('/rooms',methods=['GET','POST'])
@login_required
def rooms():
	pgid = request.args.get('PGID')
	# print(pgid)
	data = mysql_query("select * from room_mst where pgid='{}'".format(pgid))
	if request.method == "POST":
		pgid = request.form['submit']
		print(request.form.get('amenities'))
		print(request.form.get('amenitiesTV'))
		if request.form.get('amenitiesTV') is None:
			tv = 0
		else:
			tv=1
		if request.form.get('amenities') is None:
			ac=0
		else:
			ac=1
		mysql_query(''' INSERT INTO `homies`.`room_mst`
						(`PGID`,
						`total_beds`,
						`avail_beds`,
						`AC`,
						`TV`,
						`rent`,
						`token_amt`)
						VALUES
						({},{},{},{},{},{},{}); '''.format(pgid,request.form["total_beds"],request.form['vacant_beds'],int(ac),int(tv),request.form['room_rent'],request.form['token_amount']))
		return redirect(url_for('pgo.rooms'))
	file_names = get_file_list_s3(bucket ='mittrisem',prefix='pg_images/')
	# print(file_names)
	lst=[]
	cntr=0
	for x in data:
		for y in file_names:
			if y[10:14] == 'room':
				lst.append(y)
		dict = {'images':lst}
		data[int(cntr)].update(dict)
		cntr=cntr+1
		# print(lst)
		# print(data)

	return render_template('pgo/rooms.html',pgid=pgid,data=data)


@pgo.route('/Confirmbooking',methods=['GET','POST'])
def confirmbooking():
	data=mysql_query("select user_mst.phone,user_mst.phone,booking_mst.bid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,user_mst.fname,user_mst.lname,pg_mst.city,booking_mst.book_date,user_mst.gender,booking_mst.status from booking_mst inner join user_mst on booking_mst.uid=user_mst.uid inner join pg_mst on pg_mst.pgid=booking_mst.pgid ")
	if request.method=="POST":
		if "but1" in request.form:
			value=request.form['but1']
			data=mysql_query("select user_mst.email,user_mst.phone,booking_mst.bid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,user_mst.fname,user_mst.lname,pg_mst.city,booking_mst.book_date,user_mst.gender,booking_mst.status from booking_mst inner join user_mst on booking_mst.uid=user_mst.uid inner join pg_mst on pg_mst.pgid=booking_mst.pgid where booking_mst.status='{}'".format("Deactivated"))
			return render_template('pgo/bookinginfo.html',data=data,value=value)
		elif "but2" in request.form:
			value=request.form['but2']
			data=mysql_query("select user_mst.email,user_mst.phone,booking_mst.bid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,user_mst.fname,user_mst.lname,pg_mst.city,booking_mst.book_date,user_mst.gender,booking_mst.status from booking_mst inner join user_mst on booking_mst.uid=user_mst.uid inner join pg_mst on pg_mst.pgid=booking_mst.pgid where booking_mst.status='{}'".format("Activated"))
			return render_template('pgo/bookinginfo.html',data=data,value=value)
		elif "but3" in request.form:
			value=request.form['but3']
			data=mysql_query("select user_mst.email,user_mst.phone,booking_mst.bid,pg_mst.pg_name,pg_mst.pg_gender,pg_mst.area,user_mst.fname,user_mst.lname,pg_mst.city,booking_mst.book_date,user_mst.gender,booking_mst.status from booking_mst inner join user_mst on booking_mst.uid=user_mst.uid inner join pg_mst on pg_mst.pgid=booking_mst.pgid where booking_mst.status='{}'".format("Declined"))
			return render_template('pgo/bookinginfo.html',data=data,value=value)
		if "button1" in request.form:
			bid=request.form['button1']
			print(bid)
			mysql_query("UPDATE booking_mst SET status='{}' where bid={}".format("Activated",bid))
			return render_template('pgo/bookinginfo.html')
		if "decline" in request.form:
			bid=request.form['decline']
			print(bid)
			mysql_query("UPDATE booking_mst SET status='{}' where bid={}".format("Declined",bid))
			return render_template('pgo/bookinginfo.html',data=data)			
	return render_template('pgo/bookinginfo.html',data=data)



@pgo.route('/updaterooms',methods=['GET','POST'])
def updaterooms():
	if request.method=="POST":
		if "hideroom" in request.form:
			pgid=request.form['pgid']
			rid=request.form['hideroom']
			mysql_query("UPDATE room_mst set rhidden='{}' where rid={}".format("yes",rid))
			return redirect(url_for('pgo.rooms',PGID=pgid))
		if "unhideroom" in request.form:
			pgid=request.form['pgid']
			rid=request.form['unhideroom']
			mysql_query("UPDATE room_mst set rhidden='{}' where rid={}".format("no",rid))
			return redirect(url_for('pgo.rooms',PGID=pgid))
		if "deleteroom" in request.form:
			pgid=request.form['pgid']
			rid=request.form['deleteroom']
			mysql_query("DELETE from room_mst where rid={}".format(rid))
			return redirect(url_for('pgo.rooms',PGID=pgid))

		if "updateroom" in request.form:
			rid = request.form['updateroom']
			pgid = request.form['pgid']
			totalbed = request.form['totalbed']
			availbed = request.form['availbed']
			rent = request.form['rent']
			if request.form.get('ac') is None:
				ac = 0
			else:
				ac = 1
			if request.form.get('tv') is None:
				tv = 0
			else:
				tv = 1

			# token = (rent/3)
			mysql_query("UPDATE room_mst set total_beds='{}',avail_beds='{}',AC={},TV={},rent='{}' where RID={}".format(totalbed,availbed,ac,tv,rent,rid))



			#ghode tuje bas idhar wo update wala form h na usse values lani h variable me jese agar rent lana
			#h toh rent = request.form['rent'] ye jo square brackets ke andar rent h woo imput field ka naam h 
			#or phir ye update ki query pel diyo "UPDATE room_mst set values({})"
			return redirect(url_for('pgo.rooms',PGID=pgid))
	return "completed"	
