import os

from flask import Flask, render_template, session
from pymongo import MongoClient

from user import user_bp, blueprint
from upload import upload_bp
from mycloset import closet
from trade import trade_bp
from ranking import ootd_rank

#Flask App Setup
app = Flask(__name__)

# http / https 환경설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

#MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

#시크릿키 랜덤적용
app.secret_key = os.urandom(24)

#blueprint load
app.register_blueprint(blueprint,url_prefix="/login")
app.register_blueprint(user_bp,url_prefix="/login")
app.register_blueprint(trade_bp, url_prefix='/trade')
app.register_blueprint(closet, url_prefix='/mycloset')
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(ootd_rank, url_prefix='/ootd')

@app.route('/')
def home():
    #로그인 상태에 따라 index 로딩시 상태변수 전달 / 로그인페이지 => 로그아웃으로 변경
    logged = False
    if "user_id" in session:
        logged = True
    return render_template('index.html', logged = logged)

# 커뮤니티 페이지 렌더링
@app.route('/community')
def community():
    return render_template('community.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)