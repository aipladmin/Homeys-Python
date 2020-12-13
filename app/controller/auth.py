from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import random
import string
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

@auth.route('/pymongo')
def pymongo_testrun():
    db_operations = db.restaurants
    # print("db_operations:   "+str(db_operations))
    data = db_operations.find({'_id':ObjectId('5eb3d668b31de5d588f4292a')},{'address':0,'name':0})
    ls_data = list(data)
    json_data = dumps(ls_data)
    print("data:  "+str(json_data))
    return str(json_data)

@auth.route('/')
def login():
    # cur = g.db.cursor()
    # cur.execute("select * from auth")
    # rows = cur.fetchall()
    # print(rows)
    return render_template('index.html')

@auth.route('/otp', methods=['POST'])
def loginscr():
    if request.method == 'POST':
        return redirect(url_for('admin.admintest'))
    return 'loginotp'


# LOGOUT CODE


@auth.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))

@auth.route('/register')
def register():

    return render_template('register.html')


@auth.route('/index')
@login_required
def index_template():
    return render_template('index.html')


@auth.route('/prac')
@login_required
def prac():
    return render_template('prac.htm.j2')
