from flask import render_template, request, jsonify, session, Blueprint
from pymongo import MongoClient
from bson.objectid import ObjectId

closet = Blueprint('closet', __name__)

#MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

def objectIDtoStr(list):
    result = []
    for document in list:
        document['_id'] = str(document['_id'])
        result.append(document)
    return result

# 옷장 목록 페이지 렌더링
@closet.route('/')
def mycloset():
    # 로그인 했으면(세션에 사용자 id가 있으면)
    if "user_id" in session:
        return render_template('closet.html')  # 내 옷장 렌더링
    else:
        return render_template('login.html')  # 로그인 페이지로 이동


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
        clothes = objectIDtoStr(list(db.clothes.find({'user_id': user_id}, {'user_id': False})))
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
            'clothes_color': request.args.get('color')
        }

        # MongoDB 쿼리문 작성
        query = [{'user_id': user_id}]
        for key in conditions:
            temp = conditions[key]

            # 조건이 주어진 key에 대해서만 쿼리문 작성
            if temp is not None:
                if type(temp) is list:  # 중복 선택이 가능한(리스트로 저장된) 카테고리
                    query.append({key: {'$in': temp}})
                else:   # 단일 값을 가지는 카테고리
                    query.append({key: temp})

        # 해당 사용자의 옷들을 가져오고, 데이터가 있다면 empty를 False로 설정
        clothes = objectIDtoStr(list(db.clothes.find({'$and': query}, {'user_id': False})))
        if clothes:
            empty = False

        return jsonify({'status': status, 'clothes': clothes, 'empty': empty})
    except:
        status = 'FAIL'
        return {'status': status, 'msg': '옷 목록을 가져오는데 실패했습니다.'}

# 옷 정보 수정
@closet.route('/update', methods=['POST'])
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