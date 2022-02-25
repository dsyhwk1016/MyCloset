from flask import render_template, request, jsonify, session, Blueprint, flash, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import hashlib
from img_set import *

ootd_rank = Blueprint('ootd_rank', __name__)

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

@ootd_rank.route('/')
def ootd():
    return render_template('ootd_rank.html')

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
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        ootd_img = request.files['file']
        comment = request.form['comment']

        if ootd_img and allowed_file(ootd_img.filename):
            nameform = f'{user_id}_{date}'  # 파일 이름 포맷
            extension = ootd_img.filename.split('.')[-1]
            file_name = hashlib.sha256(nameform.encode()).hexdigest()  # 파일명 암호화

            save_to = f'{file_name}.{extension}'    # 파일명.확장자
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_to)  # 로컬 저장 경로
            ootd_img.save(save_path)    # 로컬에 파일 저장
        else:
            status = 'FAIL'
            return {'status': status, 'msg': '파일 확인에 실패했습니다.'}

        s3 = s3_connection()
        s3.upload_file(
            Filename=save_path, # 업로드 할 파일의 위치
            Bucket=BUCKET_NAME,
            Key=f'ootd/{save_to}',   # s3 저장 위치 및 파일명
            ExtraArgs={"ContentType": 'image/jpg', "ACL": 'public-read'}
        )
        s3_path = f'https://whatisinmycloset.s3.ap-northeast-2.amazonaws.com/ootd/{save_to}'
        os.remove(save_path)    # 로컬에 저장된 파일 삭제

        doc = {
            'user_name': user_name,
            'image_path': s3_path,
            'comment': comment,
            'upload_date': date,
            'likes': 0
        }
        db.rank.insert_one(doc)

        return render_template('ootd_rank.html')
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '코디를 등록하는 데 실패했습니다.'}

# 전체 코디 데이터 전송
@ootd_rank.route('/load', methods=['GET'])
def load():
    status = 'SUCCESS'
    try:
        empty = True   # 코디 데이터 여부

        # 전체 코디 데이터 가져오기
        top3 = list(db.rank.find({}, {'_id': False}).sort('likes', -1))[:3]  # 좋아요 내림차순 상위 3개 데이터
        recent_ootd = list(db.rank.find({}, {'_id': False}).sort('upload_date', -1))   # 전체 최신순 정렬
        if recent_ootd:
            empty = False

        return jsonify({'status': status,'top3': top3, 'ootds': recent_ootd, 'empty': empty})
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

'''
# 코디 정보 수정
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
'''