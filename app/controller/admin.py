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
                 static_folder='static/dash',
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

@admin.route('/')
def admintest():
    return render_template('admin/admin_test.html')