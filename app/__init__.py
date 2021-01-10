import os
import sqlite3
from flask import Flask
from flask_mail import Mail
from flaskext.mysql import MySQL

from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

import sentry_sdk
from sentry_sdk import capture_exception
from sentry_sdk.integrations.flask import FlaskIntegration

from .config import Config

mail = Mail()
def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_url_path=''
    )

    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024   # 5 MB limit
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # app.config['SESSION_TYPE'] = 'sqlalchemy'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # quiet warning message

    # db = SQLAlchemy(app)
    # app.config['SESSION_SQLALCHEMY']=db
    
    # sess = Session(app)
    # db.init_app(app)
    # db.create_all()
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # db_path = os.path.join(BASE_DIR, "db.sqlite3")
    # print(db_path)


    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USE_SSL']=True
    app.config['MAIL_USERNAME'] = 'developer.websupp@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jvlfatxjxjigmryg'
    app.config['MAIL_DEFAULT_SENDER'] = 'developer.websupp@gmail.com'
    app.config['MAIL_USE_TLS'] = False 
    mail.init_app(app)

    sentry_sdk.init(
    dsn="https://3cbd60be648047aeaaa21a66b5be645d@o416140.ingest.sentry.io/5552589",
    integrations=[FlaskIntegration()])

    from app.controller import (
        auth,admin,user,pgo
    )

    app.register_blueprint(auth.auth)
    app.register_blueprint(admin.admin)
    app.register_blueprint(user.user)
    app.register_blueprint(pgo.pgo)

    return app
