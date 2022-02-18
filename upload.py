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
        'image_path': '../static/uploads/' + name,   # DB에는 이미지가 저장되는 경로를 저장해주세요! - 가영
        'clothes_style': style,
        'clothes_season': season,
        'clothes_kind': kind,
        'clothes_color': color
    }

    db.clothes.insert_one(doc)
    # return jsonify({'msg': ' 성공적으로 작성되었습니다.'})
    file = request.files['file']
    # if file not in request.files: #일단 이 부분 오류 이 부분만 잘 고치면 될것같아요
    #     flash('No file part')
    #     return redirect(request.url)
    if file.filename == '':  # 이 부분은 안오류
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # 요 부분은 현정님께서 쓰신 부분인데 파일이름넣고 / 업로드폴더에 세이브하는거같은데 제대로 작동
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ## 67번 줄에 filename 대신 '이름.확장자' 넣어서 돌려보니까 잘 저장 돼요! 이 점 참고하셔서 수정 진행하시면 될 것 같아요 - 가영

    return render_template('upload.html')