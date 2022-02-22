from flask import render_template, request, jsonify, session, Blueprint, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import hashlib
import os
# from img_set import *

ootd_rank = Blueprint('ootd_rank', __name__)

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

# 코디 업로드
@ootd_rank.route('/upload', methods=['POST'])
def upload():
    status = 'SUCCESS'
    try:
        # 로그인 했으면(세션에 사용자 id가 있으면) id로 닉네임 가져오기
        if "user_id" in session:
            user_id = session['user_id']
            user_name = db.member.find_one({'user_id': user_id})['user_name']
        else:
            return render_template('login.html')  # 로그인 페이지로 이동
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '사용자 정보를 확인하는데 실패했습니다.'}

    try:
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        ootd_img = request.files['file']

        if ootd_img and allowed_file(ootd_img.filename):
            nameform = f'{user_id}_{date}'  # 파일이름 규칙 정하기
            extension = ootd_img.filename.split('.')[-1]  # 기존 파일명에서 확장자만 빼서 저장
            file_name = hashlib.sha256(nameform.encode()).hexdigest()  # 파일명 암호화

            save_to = f'{file_name}.{extension}'
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_to)
            ootd_img.save(save_path)
        else:
            return {'status': 'FAIL', 'msg': '파일 확인에 실패했습니다.'}

        ### aws s3 업로드 오류 ###
        # s3 = s3_connection()
        # s3.put_object(
        #     Bucket = BUCKET_NAME,
        #     Body = ootd_img,
        #     Key = save_path,
        #     ContentType = ootd_img.content_type)

        doc = {
            'user_name': user_name,
            'image_path': '../static/uploads/' + save_to,
            'upload_date': date,
            'likes': 0
        }
        db.rank.insert_one(doc)

        return {'status': status}
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '코디를 등록하는 데 실패했습니다.'}

# 전체 코디 데이터 전송
@ootd_rank.route('/load', methods=['GET'])
def load():
    status = 'SUCCESS'
    try:
        empty = True   # 코디 데이터 여부

        # 전체 코디 데이터를 가져오고, 데이터가 있다면 empty를 False로 설정
        ootds = list(db.rank.find({}, {'_id': False}))
        if ootds:
            empty = False

        return jsonify({'status': status, 'ootds': ootds, 'empty': empty})
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '전체 코디 목록을 가져오는데 실패했습니다.'}

# 코디 데이터 정렬
@ootd_rank.route('/sort', methods=['GET'])
def sort():
    status = 'SUCCESS'
    try:
        empty = True   # 코디 데이터 여부

        sort = request.args.get('sort')
        if sort == 'like_desc':
            ootds = list(db.rank.find({}, {'_id': False}).sort('likes', -1))
        elif sort == 'date_asc':
            ootds = list(db.rank.find({}, {'_id': False}).sort('upload_date', 1))
        elif sort == 'date_desc':
            ootds = list(db.rank.find({}, {'_id': False}).sort('upload_date', -1))
        else:
            flash('잘못된 정렬 조건입니다.')

        if ootds:
            empty = False

        return jsonify({'status': status, 'ootds': ootds, 'empty': empty})
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '코디 목록을 가져오는데 실패했습니다.'}

####################### 이 아래로는 수정해야함 ############################
# 옷 정보 수정
@ootd_rank.route('/update', methods=['POST'])
def update():
    status = 'SUCCESS'
    try:
        clothes_id = request.form['clothes_id'] # 수정하려는 옷 정보
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '옷 정보를 확인하는데 실패했습니다.'}

    try:
        # 수정 데이터 딕셔너리 생성
        doc = {
            'clothes_style': request.form.getlist('style'),
            'clothes_season': request.form.getlist('season'),
            'clothes_kind': request.form['kind'],
            'clothes_color': request.form['color']
        }

        # DB에 수정 사항 반영
        db.clothes.update_one({'_id': ObjectId(clothes_id)}, {'$set': doc})

        return {'status': status}
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '정보를 수정하는데 실패했습니다.'}