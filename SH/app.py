from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import pandas as pd

# API추가
from DB import get_db_connection
from API.Register import regist_BP
from API.fridge import fridge_BP


app = Flask(__name__)

# CORS 정책 추가, 도메인 별로도 설정할 수 있지만 걍 전역적으로 정책추가 
CORS(app)


# API 요청 포인트 추가
app.register_blueprint(regist_BP, url_prefix='/Regist')
app.register_blueprint(fridge_BP, url_prefix='/Fridge')
 

# 예시 엔드포인트: 모든 데이터 조회
@app.route('/get_data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM User"
        cursor.execute(sql)
        data = cursor.fetchall()  # 모든 결과를 가져옴
    connection.close()
    return jsonify(data)


# 예시 엔드포인트: 데이터 삽입
@app.route('/insert_data', methods=['POST'])
def insert_data():
    new_data = request.json  # JSON 형식으로 데이터 수신
    name = new_data.get('name')
    age = new_data.get('age')
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO your_table (name, age) VALUES (%s, %s)"
        cursor.execute(sql, (name, age))
        connection.commit()  # 변경 사항을 커밋
    connection.close()
    return jsonify({"message": "Data inserted successfully!"}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5001)
