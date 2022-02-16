from flask import Flask, render_template, request, redirect, url_for, flash
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# class Mycloset(db.client): 참조 flask_mongoengine
#     file = db.StringField()
#     style = db.StringField()
#     season = db.StringField()
#     kind = db.StringField()
#     color = db.StringField()

@app.route('/', methods=['GET'])
def upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # file = request.files['file']
    # style = request.form['uniform_style']
    # season = request.form['uniform_season']
    # kind = request.form['uniform_kind']
    # color = request.form['uniform_color']
    # filename = secure_filename(file.filename)

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

        # doc = {
        #     'file': file,
        #     'style': style,
        #     'season': season,
        #     'kind': kind,
        #     'color': color
        # }
        # db.mycloset.insert_one(doc)
        # flash('File successfully uploaded ' + file.filename + ' to the database!')
        # return redirect('/')
        else:
            flash('Only png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template('upload.html')
