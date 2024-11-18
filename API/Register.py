from flask import Blueprint, jsonify, request
import pymysql
import pandas as pd

from DB import get_db_connection


regist_BP = Blueprint('Regist', __name__)


# ID확인 및 DB에 존재하지 않을 경우 추가
@regist_BP.route('/USER_regists', methods=['POST', 'GET']) 
def User_resist():
    new_data = request.json
    ID = new_data.get('ID')
    Name = new_data.get('name')
    PSW = new_data.get('PSW')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = 'select ID from User where ID=%s'
        cursor.execute(sql, ID)
        data = cursor.fetchall()
        if(check_already_resisted(data, ID)):
            # 가입정보 이미 존재함을 메시징
            connection.close()
            return jsonify({'message' : '해당 유저는 이미 가입되어 있습니다', 'status' : 0})
        sql = 'insert into User value(%s, %s, %s)'
        cursor.execute(sql, (ID, Name, PSW))
        connection.commit()
    connection.close()
    return jsonify({'message' : '가입되었습니다', 'status' : 1})
    
# ID 중복여부 확인
def check_already_resisted(data, ID):
    data = pd.DataFrame(data)
    if(len(data) == 0):
        return 0
    return 1


# 로그인 요청
@regist_BP.route('/login_request', methods=['POST', 'GET'])
def login_request():
    new_data = request.json
    ID = new_data.get('ID')
    PSW = new_data.get('PSW')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = 'select PSW from User where ID=%s'
        cursor.execute(sql, ID)
        data = cursor.fetchone()
    connection.close()

    if(data == None):
        return jsonify({'message' : '해당 유저는 존재하지 않습니다', 'status' : 0})
    elif(data['PSW'] != PSW):
        return jsonify({'message' : '비밀번호가 틀렸습니다', 'status' : 0})
    else:
        return jsonify({'message' : '환영합니다', 'status' : 1})