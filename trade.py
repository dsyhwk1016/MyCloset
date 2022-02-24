from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
from pymongo import MongoClient
from datetime import datetime
from markupsafe import escape
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.mycloset

#blueprint setup
trade_bp = Blueprint('trade', __name__)

def objectIdDecoder(list):
  results=[]
  for document in list:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results

@trade_bp.route('/')
def trade():
    logged = False

    if 'user_id' in session:
        logged = True
    return render_template('trade_list.html', logged = logged)

@trade_bp.route('/list', methods=['GET'])
def trade_list():
    lists = objectIdDecoder(list(db.trade.find({})))
    return jsonify({'lists': lists})


@trade_bp.route('/write')
def trade_write():
    logged = False
    if 'user_id' in session:
        user_id = escape(session['user_id'])
        return render_template('trade_write.html', user_id=user_id, logged=logged)
    else :
        return redirect(url_for('login.login_page'))

@trade_bp.route('/load_closet', methods=['GET'])
def load_closet():
    if 'user_id' in session:
        user_id = escape(session['user_id'])
        closet_list = objectIdDecoder(list(db.clothes.find({'user_id' : user_id})))

        return jsonify({'closet_list' : closet_list})
    else:
        return redirect(url_for('login.login_page'))

@trade_bp.route('/trade_submit', methods=['POST'])
def trade_submit():
    user_id = escape(session['user_id'])
    cloth_id = request.form['cloth_id']
    img_path = request.form['img_path']
    status = '거래중'
    write_title = request.form['title']
    write_price = request.form['price']
    write_content = request.form['content']
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    doc = {
        'user_id' : user_id,
        'cloth_id' : cloth_id,
        'image_path' : img_path,
        'status' : status,
        'title' : write_title,
        'price' : write_price,
        'content' : write_content,
        'datetime' : current_time,
    }
    db.trade.insert_one(doc)
    return redirect(url_for('trade.trade'))

@trade_bp.route('/view')
def trade_view():
    logged = False

    if 'user_id' in session:
        logged = True
    return render_template('trade_view.html', logged=logged)

@trade_bp.route('/view/detail', methods=['GET'])
def trade_view_detail():
    trade_id = request.args.get('goods_id')
    trade_info = db.trade.find_one({'_id' : ObjectId(trade_id)}, {'_id' : False})
    comment_info = objectIdDecoder(list(db.trade_comment.find({'trade_id' : trade_id})))
    user_id = escape(session['user_id'])

    return jsonify({'trade_info' : trade_info, 'comment_info' : comment_info, 'user_id' : user_id})

@trade_bp.route('/modify')
def trade_modify():
    logged = False

    if 'user_id' in session:
        logged = True
    return render_template('trade_modify.html', logged=logged)

@trade_bp.route('/modify/detail', methods = ['GET'])
def trade_modify_detail():
    trade_id = request.args.get('goods_id')
    trade_info = db.trade.find_one({'_id' : ObjectId(trade_id)}, {'_id' : False})
    cloth_id = trade_info['cloth_id']
    cloth_info = db.clothes.find_one({'_id' : ObjectId(cloth_id)}, {'_id' : False})

    return jsonify({'trade_info' : trade_info, 'cloth_info' : cloth_info})

@trade_bp.route('/modify', methods=['POST'])
def trade_modify_submit():
    trade_id = request.form['trade_id']
    cloth_id = request.form['cloth_id']
    img_path = request.form['img_path']
    title = request.form['title']
    price = request.form['price']
    content = request.form['content']

    now = datetime.now()
    last_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    doc = {
        'cloth_id' : cloth_id,
        'image_path' : img_path,
        'title' : title,
        'price' : price,
        'content' : content,
        'last_datetime' : last_datetime
    }

    db.trade.update_one({'_id' : ObjectId(trade_id)}, {'$set' : doc})

    return redirect(url_for('trade.trade'))

@trade_bp.route('/view/comment_write', methods=['POST'])
def comment_write():
    user_id = escape(session['user_id'])
    user_info = db.member.find_one({'user_id' : user_id}, {'_id' : False})
    user_name = user_info['user_name']
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    trade_id = request.form['trade_id']
    contents = request.form['contents']

    doc = {
        'user_id' : user_id,
        'user_name' : user_name,
        'trade_id' : trade_id,
        'contents' : contents,
        'datetime' : current_time
    }

    db.trade_comment.insert_one(doc)

    return jsonify({'msg' : '댓글이 등록되었습니다'})