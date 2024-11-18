from flask import Flask, jsonify, request
import pymysql
import pandas as pd

from API.Register import regist_BP
from API.fridge import fridge_BP
from API.insert import add_food  # add_food 엔드포인트
from API.delete import delete_food  # delete_food 엔드포인트


app = Flask(__name__)
app.register_blueprint(regist_BP, url_prefix='/Regist')
app.register_blueprint(fridge_BP, url_prefix='/Fridge')


# 데이터베이스 설정
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "ghdwhdgy0328!"
DB_NAME = "Refri"


# 데이터베이스 연결 함수
def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor  # 쿼리 결과를 dict로 반환
    )
    return connection


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
