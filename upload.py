from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os
import urllib.request

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#blueprint setup
upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# class Mycloset(db.client): 참조 flask_mongoengine
#     file = db.StringField()
#     style = db.StringField()
#     season = db.StringField()
#     kind = db.StringField()
#     color = db.StringField()

@upload_bp.route('/')
def upload():
    return render_template('upload.html')


@upload_bp.route('/upload_file', methods=['POST'])
def upload_file():
    name = request.args.get('name'),
    style = request.args.get('style'),
    season = request.args.get('season'),
    kind = request.args.get('kind'),
    color = request.args.get('color')

    doc = {
        'name': name,
        'style': style,
        'season': season,
        'kind': kind,
        'color': color
    }
    db.mycloset.insert_one(doc)

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File successfully uploaded ' + file.filename + ' to the database!')
        return redirect('/')
    else:
        flash('Only png, jpg, jpeg, gif')
        return render_template('login.html')
    return render_template('upload.html')