from flask import render_template, request, redirect, flash, Blueprint, session, url_for
from pymongo import MongoClient
from markupsafe import escape
from datetime import datetime
import hashlib
from img_set import *

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

# blueprint setup
upload_bp = Blueprint('upload', __name__)

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

    file = request.files['image']

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
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_to)
        file.save(save_path)

    s3 = s3_connection()
    s3.upload_file(
        Filename=save_path,  # 업로드할 파일의 경로
        Bucket=BUCKET_NAME,
        Key=f'clothes/{save_to}',  # 파일명
        ExtraArgs={"ContentType": 'image/jpg', "ACL": 'public-read'}
    )
    s3_path = f'https://whatisinmycloset.s3.ap-northeast-2.amazonaws.com/clothes/{save_to}'
    os.remove(save_path)

    doc = {
        'user_id': user_id,
        'image_path': s3_path,
        'clothes_style': style,
        'clothes_season': season,
        'clothes_kind': kind,
        'clothes_color': color
    }

    db.clothes.insert_one(doc)

    return redirect(url_for('closet.mycloset'))