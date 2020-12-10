import sqlite3
import random
import string

import boto3
from botocore.exceptions import ClientError
from flask_pymongo import MongoClient,pymongo
from flaskext.mysql import *
from functools import wraps
from flask_mail import *
from flask import *
from flask import current_app

from app import create_app
from flask import *
from flaskext.mysql import MySQL
from flask_mail import Mail,Message

# mongo = PyMongo()
mysql = MySQL()

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://MadhavParikh:MJfuRI1MJWEKXkBK@cluster0.8p8et.mongodb.net/sample_restaurants?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE&w=majority")
# print(client.server_info())
db = client.sample_restaurants

app.config['MYSQL_DATABASE_USER'] = 'Sadministrator'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tk1TF3GjpEc56soEjRR6'
app.config['MYSQL_DATABASE_DB'] = 'surel'
app.config['MYSQL_DATABASE_HOST'] =  'socds.cttdwedcfzhs.ap-south-1.rds.amazonaws.com'
mysql.init_app(app)



def mysql_query(sql,sqldt):
    print(sql,sqldt)

    connection = mysql.connect()
    cursor = connection.cursor()
    if sql.split(' ')[0].lower() == "select" :
        if sqldt is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql,sqldt)
            print(cursor._executed)
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        data = results
        # data = {'data':data}

        
        cursor.close()
        connection.close()
        return data
    else:
        cursor.execute(sql,sqldt)
        print(cursor._executed)
        connection.commit()
        cursor.close()
        connection.close()
    return None

# SQLITE QUERY DRIVER
def sql_query(sql, sqldt):
    # print("SQLDT:"+sqldt)
    try:
        
        if sqldt is not None:
            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                # print(sql, "        ", sqldt)
                cur.execute(sql, sqldt)
                if sql.split(' ')[0].lower() == "select" :
                    rows = cur.fetchall()
                    # print(sql, "        ", sqldt)
                    # print("           SELECT           ")
                    # print(rows)
                    flag =1
                else:
                    # print("           NOTSELECT           ",sql)
                    con.commit()
                    flag=0

        if sqldt is None:
            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                print(sql)
                cur.execute(sql)
                rows = cur.fetchall()
                flag=1
    except con.Error as e:
        print("Error: {}".format(e.args[0]))
    finally:
        con.close()
        
        if flag == 0:
            # print('             SELECTFLAg               ')
            con.close()
            return None
        else:
            # print('             SELECT FLAG ROWS               ')
            con.close()
            return rows


# MAIL DRIVER
def send_mail(**deets):
    mail = Mail()
        # with current_app.app_context():
    #     mail = Mail()
    #     mail.send(msg)
    # print(deets['otp'])
    msg = Message(deets['Subject'], sender = 'developer.websupp@gmail.com', recipients = [deets['Emailid'] ])
    # print(msg)
    msg.html = render_template('mail.html',emailid=deets['Emailid'],otp=deets['OTP'],salutation = deets['salutation'])
    mail.send(msg)
    return "mail"




# DECORATORS
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in session and "blockid" in session:
            return f(*args, **kwargs)
        else:
            # flash('You need to login first')
            return redirect(url_for('auth.login'))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_email' in session and "role" in session:
            return f(*args, **kwargs)
        else:
            # flash('You need to login first')
            return redirect(url_for('admin.login'))
    return wrap
