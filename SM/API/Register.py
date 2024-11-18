from flask import Blueprint, jsonify, request
import pymysql
import pandas as pd

from DB import get_db_connection

regist_BP = Blueprint('Regist', __name__)


# ID확인 및 DB에 존재하지 않을 경우 추가
@regist_BP.route('/USER_regists', methods=['GET', 'POST']) 
def User_resist():
    # new_data = request.json
    # ID = new_data.get('ID')
    # Name = new_data.get('name')
    # PSW = new_data.get('PSW')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = 'select ID from User where ID=%s'
        cursor.execute(sql, '1111')
        data = cursor.fetchall()
        if(check_already_resisted(data, '1111')):
            # insert 쿼리 사용
            # sql = 'insert into User values(%s, %s, %s)'
            print('Exists')
    connection.close()
    return jsonify(data)
            

# ID 중복여부 확인
def check_already_resisted(data, ID):
    data = pd.DataFrame(data)
    if(len(data) == 0):
        return 0
    return 1