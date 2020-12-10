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
 
pgo = Blueprint('pgo', __name__,url_prefix='/pgo',template_folder='templates',
                 static_folder='static/dash')

@pgo.route('/')
def pgotest():
    return render_template('pgo/pgo_test.html')