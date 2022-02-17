from flask import render_template, request, jsonify,  url_for, redirect, session, current_app, Blueprint, escape
from pymongo import MongoClient

closet = Blueprint('closet', __name__)

#MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

# 옷장 목록 페이지 렌더링
@closet.route('/')
def mycloset():
    return render_template('closet.html')

# 전체 옷 데이터 전송
@closet.route('/load', methods=['GET'])
def load():
    status = 'SUCCESS'
    try:
        # 현재 로그인한 사용자의 id와 닉네임 가져오기
        user_id = session['user_id']
        user_name = db.member.find_one({'user_id':user_id})['user_name']
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '사용자 정보를 확인하는데 실패했습니다.'}

    try:
        empty = True   # 옷장 비었는지 여부

        # 해당 사용자의 옷들을 가져오고, 데이터가 있다면 empty를 False로 설정
        clothes = list(db.clothes.find({'user_id': user_id}, {'_id': False, 'user_id': False}))
        if clothes:
            empty = False

        return jsonify({'status': status, 'user_name': user_name, 'clothes': clothes, 'empty': empty})
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '전체 옷장 목록을 가져오는데 실패했습니다.'}


# 특정 옷만 출력(카테고리)
@closet.route('/find', methods=['GET'])
def find():
    status = 'SUCCESS'
    try:
        user_id = session['user_id']    # 현재 로그인한 사용자 정보
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '사용자 정보를 확인하는데 실패했습니다.'}

    try:
        empty = True   # 옷장 비었는지 여부

        # 검색 조건 딕셔너리 생성
        conditions = {
            'clothes_style': request.args.get('style'),
            'clothes_season': request.args.get('season'),
            'clothes_kind': request.args.get('kind'),
            'clothes_color': request.args.get('color'),
            'clothes_name': request.args.get('title')
        }

        # MongoDB 쿼리문 작성
        query = []
        for key in conditions:
            temp = conditions[key]

            # 조건이 주어진 key에 대해서만 쿼리문 작성
            if temp is not None:
                if type(temp) is list:  # 중복 선택이 가능한(리스트로 저장된) 카테고리
                    query.append({key: {'$in': temp}})
                elif key == 'title':    # 이름으로 검색할 경우
                    query.append({key: {'$regex': temp}})
                else:   # 단일 값을 가지는 카테고리
                    query.append({key: temp})

        # 해당 사용자의 옷들을 가져오고, 데이터가 있다면 empty를 False로 설정
        clothes = list(db.clothes.find({'$and': [{'user_id': user_id}, {'$or': query}]}, {'_id': False, 'user_id': False}))
        if clothes:
            empty = False

        return jsonify({'status': status, 'clothes': clothes, 'empty': empty})
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '옷 목록을 가져오는데 실패했습니다.'}

# 옷 정보 수정
@closet.route('/modify', methods=['POST'])
def modify():
    status = 'SUCCESS'
    try:
        user_id = session['user_id']    # 현재 로그인한 사용자 정보
        clothes_name: request.args.get('title') # 수정하려는 옷 정보
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '사용자 혹은 옷 정보를 확인하는데 실패했습니다.'}

    try:
        # 수정 데이터 딕셔너리 생성
        doc = {
            'clothes_style': request.args.get('style'),
            'clothes_season': request.args.get('season'),
            'clothes_kind': request.args.get('kind'),
            'clothes_color': request.args.get('color')
        }

        # DB에 수정 사항 반영
        db.clothes.update_one({'$and': [{'user_id': user_id}, {'clothes_name': clothes_name}]}, {'$set': doc})

        return {'status': status}
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '정보를 수정하는데 실패했습니다.'}