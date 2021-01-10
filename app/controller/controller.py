import boto3
from .. import mail
from botocore.exceptions import ClientError
from flaskext.mysql import *
from functools import wraps
from flask_mail import *
from flask import *
from flask import current_app

from flask import *
from flaskext.mysql import MySQL
from flask_mail import Mail,Message


mysql = MySQL()
# mail=Mail()

app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MiloniMadhav'
app.config['MYSQL_DATABASE_DB'] = 'homies'
app.config['MYSQL_DATABASE_HOST'] =  'contra.cjrbdmxkv84s.ap-south-1.rds.amazonaws.com'
mysql.init_app(app)



def mysql_query(sql):
    print(sql)
    connection = mysql.connect()
    cursor = connection.cursor()
    if sql.strip().split(' ')[0].lower() == "select" :
        
        cursor.execute(sql)
        print(cursor._executed)
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        data = results
        cursor.close()
        connection.close()
        return data
    if sql.strip().split(' ')[0].lower() != "select" :
        cursor.execute(sql)
        print(cursor._executed)
        
        mysql_query.last_row_id = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()
        return None


# MAIL DRIVER
def send_mail(**deets):
 
    
    msg = Message(deets['Subject'], sender = 'developer.websupp@gmail.com', recipients = [deets['Emailid'] ])
    # print(msg)
    msg.html = render_template('mail.html',emailid=deets['Emailid'],otp=deets['OTP'],salutation = deets['salutation'])
    mail.send(msg)
    return "mail"

ALLOWED_EXTENSIONS = {'pdf','jpeg','jpg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ! AWS FILE Upload 
# todo FILELIST S3
def get_file_list_s3(bucket, prefix):
    import boto3
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)
    file_objs =  my_bucket.objects.filter(Prefix=prefix).all()
    file_names = [file_obj.key for file_obj in file_objs]
    return file_names

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        flash('Upload File Error.',"AWS S3 Error.")
        return render_template("errors.html")
    return True


# DECORATORS
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in session and 'role' in session and  'name' in session:
            return f(*args, **kwargs)
        else:
            # flash('You need to login first')
            return redirect(url_for('auth.login'))
    return wrap
