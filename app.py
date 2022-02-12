import hashlib
import os

from flask import Flask, render_template, request, jsonify,  url_for, redirect, session, current_app
from pymongo import MongoClient
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv


#환경변수의 값 불러오기
load_dotenv()

#Flask App Setup
app = Flask(__name__)

#Google Setup
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')

# http / https 환경설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

#MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

#google blueprint Setup
blueprint = make_google_blueprint(
    client_id = client_id,
    client_secret = client_secret,
    reprompt_consent= True,
    scope=["profile", "email"],
)
app.register_blueprint(blueprint,url_prefix="/login")


@app.route('/')
def home():
    #로그인 상태에 따라 index 로딩시 상태변수 전달 / 로그인페이지 => 로그아웃으로 변경
    logged = False
    if google.authorized:
        logged = True
        google_chk()

    if "user_id" in session:
        logged = True
    return render_template('index.html', logged = logged)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    input_user_id = request.form['user_id']
    input_user_pw = request.form['user_pw']

    shapw = hashlib.sha256(input_user_pw.encode()).hexdigest()  # 패스워드 암호화

    db_user = list(db.member.find({'user_id' : input_user_id}, {'_id' : False}))

    if input_user_id != db_user[0]['user_id']: #입력한 ID가 DB에 있는지 확인
        return render_template(url_for('login_page'), id_chk = False)

    if input_user_id == db_user[0]['user_id'] and shapw == db_user[0]['user_pw']: #아이디 / 비밀번호 체크
        session['user_id'] = input_user_id #user_id 세션에 아이디 정보 입력
        return redirect(url_for('home'))

    return redirect((url_for('login_page'))) #맞는게 없으면 다시 로그인페이지로 이동

@app.route('/google_check') #구글 첫로그인시 자동으로 member 컬렉션에 ID와 Name 입력
def google_chk():
    if google.authorized:
        resp = "/oauth2/v2/userinfo"
        google_data = google.get(resp).json()

        user_id = google_data['email']
        user_name = google_data['given_name']

        chk = list(db.member.find({'user_id' : user_id},{'_id' : False}))

        if chk:
            return redirect(url_for('home'))
        else:
            doc = {
                'user_id' : user_id,
                'user_name' : user_name
            }

            db.member.insert_one(doc)
            return redirect(url_for('home'))  # 로그인 완료 후 home으로 이동
    else:
        return redirect(url_for('home'))

@app.route('/google_login')
def google_login(): #구글 로그인 선택시 구글로그인 화면으로 이동
    return redirect(url_for('google.login'))

@app.route('/logout', methods=['GET']) #로그아웃
def logout():
    if google.authorized: #구글 인증된 상태
        token = current_app.blueprints["google"].token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={
                "token" : token
            },
            headers={"content-type" : "application/x-www-form-urlencoded"}
        )
        del blueprint.token #토큰 삭제
    else:
        session.pop('user_id') #구글로그인이 아닌 일반로그인의 경우 세션삭제
    return redirect(url_for('home'))


@app.route('/register', methods=['POST', 'GET']) #회원가입시 호출
def register():
    if request.method == 'POST': # 회원가입 Form 이 Submit 되었을시 실행(POST방식)

        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_name = request.form['user_name']

        shapw = hashlib.sha256(user_pw.encode()).hexdigest() #패스워드 암호화

        doc = {
            'user_id' : user_id,
            'user_pw' : shapw,
            'user_name' : user_name
        }

        db.member.insert_one(doc) #member 컬렉션에 insert

        return redirect(url_for('home')) #로그인 완료 후 home으로 이동

    elif request.method == 'GET': #ID와 닉네임 중복체크시 호출
        if request.args.get('type') == 'id': #ID중복체크시 실행
            user_id = request.args.get('user_id') #GET방식으로 넘어온 파라미터를 변수에 저장

            chk = list(db.member.find({'user_id' : user_id} , {'_id' : False})) #member 컬렉션에서 동일한 ID가 있는지 검사

            if(chk):
                return jsonify({'msg' : '이미 가입된 ID입니다', 'status' : False})
            else:
                return jsonify({'msg' : '가입이 가능한 ID입니다', 'status' : True})

        elif request.args.get('type') == 'name': #닉네임 중복체크시 실행
            user_name = request.args.get('user_name') #GET방식으로 넘어온 파라미터를 변수에 저장

            chk = list(db.member.find({'user_name' : user_name}, {'_id' : False})) #member 컬렉션에서 동일한 닉네임이 있는지 검사

            if(chk):
                return jsonify({'msg' : '이미 가입된 닉네임입니다', 'status' : False})
            else:
                return jsonify({'msg' : '가입이 가능한 닉네임입니다', 'status' : True})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
