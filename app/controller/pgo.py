from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import string
from .controller import *
 
pgo = Blueprint('pgo', 
                __name__,
                url_prefix='/pgo',
                template_folder='templates',
                static_folder='static/auth')

@pgo.app_errorhandler(HTTPException)
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



@pgo.route('/')
def pgotest():
    return render_template('pgo/pgotest.html')

@pgo.route('/addpg')
def addpg():
    return render_template('pgo/addpg.html')

