from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
app.secret_key = 'mycloset secret key'
app.config['SESSION_TYPE'] = 'filesystem'

client = MongoClient('localhost', 27017)
db = client.mycloset


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/register', methods=['POST', 'GET']) #회원가입시 호출되는 API
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

        flash(f'{user_name} 님 회원가입 완료되었습니다')
        return redirect(url_for('home')) #로그인 완료 후 home으로 이동

    elif request.method == 'GET': #ID와 닉네임 중복체크시 호출되는 API
        if request.args.get('type') == 'id': #ID중복체크시 실행
            user_id = request.args.get('user_id') #GET방식으로 넘어온 파라미터를 변수에 저장

            chk = list(db.member.find({'user_id' : user_id} , {'_id' : False})) #member 컬렉션에서 동일한 ID가 있는지 검사

            if(chk):
                return jsonify({'msg' : '이미 가입된 ID입니다'})
            else:
                return jsonify({'msg' : '가입이 가능한 ID입니다'})

        elif request.args.get('type') == 'name': #닉네임 중복체크시 실행
            user_name = request.args.get('user_name') #GET방식으로 넘어온 파라미터를 변수에 저장

            chk = list(db.member.find({'user_name' : user_name}, {'_id' : False})) #member 컬렉션에서 동일한 닉네임이 있는지 검사

            if(chk):
                return jsonify({'msg' : '이미 가입된 닉네임입니다'})
            else:
                return jsonify({'msg' : '가입이 가능한 닉네임입니다'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
