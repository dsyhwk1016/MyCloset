from flask import Flask, render_template
from dotenv import load_dotenv
import login, find_clothes

#환경변수의 값 불러오기
load_dotenv()

#Flask App Setup
app = Flask(__name__)

app.register_blueprint(login.loginBp)
app.register_blueprint(find_clothes.closet)

@app.route('/upload')
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)