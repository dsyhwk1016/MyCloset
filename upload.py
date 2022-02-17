from flask import Flask, render_template, request, redirect, flash, Blueprint, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
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
    return render_template('upload.html')


@upload_bp.route('/upload_file', methods=['POST'])
def upload_file():  # 여기에 데이터는 받아오는데 그 이후 파일 저장 코드까지 실행이안되어서요!
    name = request.args.get('file'),
    style = request.args.get('style'),
    season = request.args.get('season'),
    kind = request.args.get('kind_select'),
    color = request.args.get('color_select'),

    doc = {
        'name': name,
        'style': style,
        'season': season,
        'kind': kind,
        'color': color
    }

    db.clothes.insert_one(doc)
    # return jsonify({'msg': ' 성공적으로 작성되었습니다.'})
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    # file = request.files['file']
    file = request.args.get('file')
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('upload.html')
# 옆에 형식대로 따오긴 했거든요..ㅠ
