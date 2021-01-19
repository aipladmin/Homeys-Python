from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import random,string,os
from werkzeug.utils import secure_filename

from .controller import *

auth = Blueprint('auth',
                __name__,
                template_folder='templates/auth',
                static_folder='static/auth',
                url_prefix='/')


def password_generator(length):
    letters = string.ascii_lowercase
    rpassword = ''.join(random.choice(letters) for i in range(length))
    return rpassword

@auth.app_errorhandler(HTTPException)
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

@auth.route('/')
@auth.route('/main')
def mainpage():
    return render_template('mainpage.html')

@auth.route('/pymongo')
def pymongo_testrun():
    
    # print("db_operations:   "+str(db_operations))
    data = db_operations.find({'personal_info.email':"parikh.madhav1999@gmail.com",'personal_info.password':'MADHAVPARIKH'},{'personal_info.entity':1,'_id':0})
    ls_data = list(data)
    json_data = dumps(ls_data)
    print("data:  "+str(json_data))
    return str(json_data)

@auth.route('/login')
def login():
    return render_template('index.html')

@auth.route('/loginscr', methods=['POST'])
def loginscr():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = mysql_query("select user_mst.UID,user_type_mst.role,user_mst.fname,user_mst.mname,user_mst.lname from user_mst inner join  user_type_mst ON user_mst.UTMID=user_type_mst.UTMID where user_mst.email='{}' and user_mst.password='{}'".format(email,password))
        print(len(data))
        if len(data) == 1:
            session['email'] = email
            session['role'] = data[0]['role']
            session['name'] = str(data[0]['fname'])+' '+str(data[0]['lname'])
            if session['role']=="Owner":
                return redirect(url_for('pgo.ownerdashboard'))
            elif session['role']=="Admin":
                return redirect(url_for('admin.admindashboard')) 
            elif session['role']=="User":
                return redirect(url_for('user.pg_ads'))

        else:
            flash('Unauthorized','danger')
            return render_template('flash.html')
        
        
        # return redirect(url_for('admin.admintest'))
    return 'loginotp'


@auth.route('/forgotpassword',methods=['POST'])
def forgotpassword():
    
    otp = password_generator(8)
    mysql_query("update user_mst set password='{}' where email='{}';".format(otp,request.form['email']))
    deets = {'Emailid':request.form['email'],'Subject':'Change Password Request','OTP':otp,'salutation':"salutation"}
    Status = send_mail(**deets)
    
    return redirect(url_for('auth.login'))

# LOGOUT CODE
@auth.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    session.pop('role', None)
    session.pop('name',None)
    return redirect(url_for('auth.login'))

@auth.route('/register',methods=['GET','POST'])
def register():

    if request.method == "POST":
        file = request.files['file_idproof']
        if file.filename == '':
           print('No file selected')
           return 'No file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(request.form['email']+'_'+filename)
            print("filename:   "+str(filename))
            dir_path = os.path.dirname(os.path.realpath(__file__))
            idproofPath = os.path.join(dir_path,"uploads",filename)
            file.save(idproofPath)
            # print(dir_path,idproofPath)
            
            file_name=idproofPath 
            print(file_name)
            bucket="mittrisem"
            object_name="id_proofs/"+filename
            upload_file(file_name=file_name, bucket=bucket, object_name=object_name)

            data = request.form
            data = data.to_dict(flat=False)
            ins_value=[]
            key_value=[]
            # print(data.keys())
            for key,value in data.items():
                ins_value.append(value[0])
            ins_value = tuple(ins_value)
            
            for keyes in data.keys():
                key_value +=[keyes]
            
            key_value =  tuple(key_value)
            
            simplified_key_value =  ','.join(key_value) 
            
            mysql_query('insert into user_mst({}) values{}'.format(simplified_key_value,ins_value))
            
        return redirect(url_for('auth.login'))
    return render_template('register.html')


# @auth.route('/index')
# @login_required
# def index_template():
#     try:
#         pass
#     except expression as identifier:
#         pass
#     return render_template('index.html')

@auth.route('/Dashboard',methods=['GET'])
@login_required
def Dashboard():
    return render_template('adminDashboard.html')
        
    

@auth.route('/updateprofile',methods=['GET','POST'])
@login_required
def updateProfile():
    if request.method == "POST":
        mysql_query(''' UPDATE `homies`.`user_mst`
                        SET
                        `fname` = '{}',
                        `mname` = '{}',
                        `lname` = '{}',
                        `email` = '{}',
                        `phone` = {},
                        `dob` = '{}',
                        `gender` = '{}',
                        `password` = '{}',
                        `addr1` = '{}',
                        `addr2` = '{}',
                        `area` = '{}',
                        `city` = '{}',
                        `state` ='{}',
                        `pincode` = {}
                        WHERE `UID` = {} '''.format(request.form['fname'],request.form['mname'],request.form['lname'],request.form['email'],
                                                    request.form['phone'],request.form['dob'],request.form['gender'],request.form['password'],
                                                    request.form['addr1'],request.form['addr2'],request.form['area'],request.form['city'],
                                                    request.form['state'],request.form['pincode'],request.form['submit']))
        flash("Profile Updated","success")
        return redirect(url_for('auth.updateProfile'))
    personalinfo = mysql_query("select * from user_mst where email='{}'".format(session['email']))
    print(personalinfo)
    return render_template('updateProfile.html',data=personalinfo)