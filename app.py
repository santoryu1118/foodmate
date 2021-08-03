from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import *
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungle

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    # jwt 토큰을 암호화 할 시크릿 키 값 - 본인만 알고있기
    JWT_SECRET_KEY = "foodporn"
)

# JWT 확장 module을 flask 어플리케이션에 등록
jwt = JWTManager(app)

id = 'lee'
pw = 'qwer'

@app.route('/')
def home():
    return render_template('login-page.html')

#사용자 정보가 일치하냐 안하냐에 따라 다른 결과 반환
# 일치 : 엑세스 토큰(입장권)은 서버에 사용자임을 인증 받았다는 뜻
# 실패 : 실패했다는 문구 반환

@app.route('/api/login', methods = ['POST'])
def login():
    user_id = request.form['id_give']
    user_pw = request.form['pw_give']

    if(user_id == id and user_pw == pw):
        return jsonify(
            result = 'success',
            # identity : 서버가 해당 토큰 요청 받은 후, identity값을 통해 사용자 식별, must unique

            access_token = create_access_token(identity = user_id, expires_delta= False)
        )
    else:
        return jsonify(result = 'Invalid Password')

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000, debug=True)