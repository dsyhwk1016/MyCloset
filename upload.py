from flask import Flask, render_template, redirect, request, flash
from werkzeug import secure_filename  # 파일 업로드 위한 설정값
import os

import urlib.request

import app

app.secret_key ="mycloset"

UPLOAD_FOLDER = './static/uploads'
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(file_name):
    return '-' in filename and filename.rsplit('.', 1).lower() in ALLOWED_EXTENSIONS

# 업로드 HTML 렌더링
@app.route('/upload')
def render_file():
    return render_template('upload.html')


# 파일 업로드 처리
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # 저장할 경로 + 파일명
        file.save('./static/uploads/' + secure_filename(file.filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공!'
