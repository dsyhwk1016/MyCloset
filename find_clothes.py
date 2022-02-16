from flask import render_template, request, jsonify,  url_for, redirect, session, current_app, Blueprint
from pymongo import MongoClient
from flask_dance.contrib.google import google

closet = Blueprint('closet', __name__, url_prefix='/')

#MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

user_id = ''
# if google.authorized:
#     resp = "/oauth2/v2/userinfo"
#     google_data = google.get(resp).json()
#
#     user_id = google_data['email']
# else:
#     user_id = session.get('user_id')

# 옷장 목록 페이지 렌더링
@closet.route('/mycloset')
def mycloset():
    empty = False
    clothes = list(db.clothes.find({'user_id': user_id}, {'_id': False, 'user_id': False, 'clothes_name': False}))
    if clothes == []:
        empty = True
    return jsonify({'clothes': clothes, 'empty': empty})

# 특정 옷만 출력
@closet.route('/mycloset/find', methods=['GET'])
def mylist():
    empty = False
    query = []
    conditions = {'style': request.args.get('style'), 'season': request.args.get('season'), 'kind': request.args.get('kind'), 'color': request.args.get('color'), 'name': request.args.get('name')}

    for key in conditions:
        temp = conditions[key]
        if conditions[key] is not None:
            query.append({key: {'$eq': temp}})

    clothes = list(db.clothes.find({'$and': [{'user_id': user_id}, {'$or': query}]}, {'_id': False, 'user_id': False, 'clothes_name': False}))
    if clothes == []:
        empty = True

    return jsonify({'clothes': clothes, 'empty': empty})