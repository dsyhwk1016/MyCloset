from flask import Flask, render_template, request, redirect, flash, Blueprint, session, url_for
from pymongo import MongoClient
from markupsafe import escape
from datetime import datetime
import os
import hashlib

app = Flask(__name__)

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# blueprint setup
upload_bp = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/')
def upload():
    logged = False
    if "user_id" in session:
        logged = True
        return render_template('upload.html', logged=logged)
    else:
        return render_template('login.html', logged=logged)


@upload_bp.route('/closet', methods=['POST'])
def upload_file():
    user_id = escape(session['user_id'])
    style = request.form.getlist('style')
    season = request.form.getlist('season')
    kind = request.form['kind']
    color = request.form['color']

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        today = datetime.now()
        file_time = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'{user_id}_{file_time}'  # 파일이름 규칙 : user_id +저장시간
        extension = file.filename.split('.')[-1]  # 기존 파일명에서 확장자만 빼서 저장
        file_name = hashlib.sha256(filename.encode()).hexdigest()  # 파일명 암호화 저장
        save_to = f'{file_name}.{extension}'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_to))

    doc = {
        'user_id': user_id,
        'image_path': '../static/uploads/' + save_to,
        'clothes_style': style,
        'clothes_season': season,
        'clothes_kind': kind,
        'clothes_color': color
    }

    db.clothes.insert_one(doc)

    return redirect(url_for('closet.mycloset'))
