from flask import Flask
import boto3

app = Flask(__name__)

# AWS S3 Key Set
AWS_ACCESS_KEY = "AKIASHQEP7CQPMBH525U"
AWS_SECRET_KEY = "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"
BUCKET_NAME = "sowhatcoding"

# Image Setup
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def s3_connection():
    s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
    return s3