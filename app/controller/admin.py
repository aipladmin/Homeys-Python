from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
# from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import sqlite3
import random
import string
from .controller import *

admin = Blueprint('admin',
                 __name__,
                 template_folder='templates',
                 static_folder='static/dash',
                 url_prefix='/admin')

@admin.route('/')
def admintest():
    return render_template('admin/admin_test.html')