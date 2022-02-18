from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
from pymongo import MongoClient
from datetime import datetime
from markupsafe import escape
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.mycloset

#blueprint setup
trade_bp = Blueprint('trade', __name__)

@trade_bp.route('/')
def trade_list():
    logged = False
    if "user_id" in session:
        logged = True

    lists = list(db.trade.find({}, {'_id' : False}))

    return render_template('board_trade.html', lists = lists, logged=logged)

@trade_bp.route('/write')
def trade_write():
    if 'user_id' in session:
        user_id = escape(session['user_id'])
        return render_template('trade_write.html', user_id=user_id)
    else :
        return redirect(url_for('login.login_page'))

@trade_bp.route('/load_closet', methods=['GET'])
def load_closet():
    if 'user_id' in session:
        user_id = escape(session['user_id'])
        closet_list = list(db.clothes.find({'user_id' : user_id}))

        json_closet = dumps(closet_list)

        return jsonify({'msg' : '연결완료', 'closet_list' : json_closet})
    else:
        return redirect(url_for('login.login_page'))

@trade_bp.route('/trade_submit', methods=['POST'])
def trade_submit():
    user_id = escape(session['user_id'])
    write_title = request.form['title']
    write_content = request.form['content']
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    doc = {
        'user_id' : user_id,
        'title' : write_title,
        'content' : write_content,
        'datetime' : current_time
    }

    db.trade.insert_one(doc)
    return redirect(url_for('trade.trade_list'))