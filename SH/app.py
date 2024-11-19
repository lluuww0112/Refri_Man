from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pymysql
import pandas as pd

# API추가
from DB import get_db_connection
from API.Register import regist_BP
from API.fridge import fridge_BP
from API.Notification import notification_BP
from API.Search import search_BP


app = Flask(__name__)

# CORS 정책 추가
CORS(app)


# API 요청 포인트 추가
app.register_blueprint(regist_BP, url_prefix='/Regist')
app.register_blueprint(fridge_BP, url_prefix='/Fridge')
app.register_blueprint(notification_BP, url_prefix='/Notify')
app.register_blueprint(search_BP, url_prefix='/Search')
 


# 각 페이지 정의
@app.route('/')
def Login():
    return render_template('/html/Login/LogIn_page.html')

@app.route('/Registration_page')
def Regist():
    return render_template('/html/Login/Registration_page.html')

@app.route('/main_page')
def Main():
    return render_template('/html/Main/main.html')

@app.route('/contain_page')
def Contain():
    return render_template('/html/Main/contain_page.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)
