from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from markupsafe import escape

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.mycloset

#blueprint setup
board_bp = Blueprint('board', __name__)

@board_bp.route('/')
def board_list():
    logged = False
    if "user_id" in session:
        logged = True
    return render_template('board.html', logged=logged)

@board_bp.route('/write')
def board_write():
    if 'user_id' in session:
        user_id = escape(session['user_id'])
        return render_template('write.html', user_id=user_id)
    else :
        return redirect(url_for('login.login_page'))

@board_bp.route('/write_sub', methods=['POST'])
def write_sub():
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

    db.board.insert_one(doc)
    return redirect(url_for('board.board_list'))