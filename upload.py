from flask import Flask, render_template, request, redirect, flash, Blueprint, session
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from markupsafe import escape
import os

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

@upload_bp.route('/upload_file', methods=['POST'])
def upload_file():

    user_id = escape(session['user_id'])
    name = request.form['img_name']
    style = request.form.getlist('style')
    season = request.form.getlist('season')
    kind = request.form['kind']
    color = request.form['color']

    doc = {
        'user_id': user_id,
        'image_path': '../static/uploads/' + name,
        'clothes_style': style,
        'clothes_season': season,
        'clothes_kind': kind,
        'clothes_color': color
    }

    db.clothes.insert_one(doc)
    # return jsonify({'msg': ' 성공적으로 작성되었습니다.'})
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('upload.html')