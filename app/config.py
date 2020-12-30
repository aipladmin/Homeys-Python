import sqlite3
from sqlite3 import Error
from datetime import datetime,timedelta
from flask import g,sessions



# basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
class Config(object):

    TESTING = True
    DEBUG = True
   
    FLASK_ENV='development'
    SECRET_KEY = 'doFddfVtb1tT9RnJWM3rx0ZiijRvKGYc'
    
    