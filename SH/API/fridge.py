from flask import Blueprint, jsonify, request
import pymysql

import pandas as pd
from datetime import datetime
import uuid

from DB import get_db_connection


# Fridge Blueprint 생성
fridge_BP = Blueprint('Fridge', __name__)


# 냉장고 추가
@fridge_BP.route('/add_Refri', methods=['GET', 'POST'])
def add_frid():
    data = request.json
    refri_ID = generate_token() # 랜덤 아이디 생성, 자동으로 중복없이 생성해줌 
    refri_Name = data.get('Refri_Name')
    User_ID = data.get('User_ID')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "select * from Refri where Refri_ID=%s"
        cursor.execute(sql, (refri_ID))        
        result = cursor.fetchall()
        if(len(result) == 0) : # 존재하지 않는 냉장고라면 추가 
            sql = """
                insert into Refri
                values(%s, %s, %s);
            """
            cursor.execute(sql, (refri_ID, refri_Name, User_ID))
            connection.commit()
            connection.close()
            return jsonify({'message' : '냉장고가 추가되었습니다', 'status' : 1})
        else:
            connection.close()
            return jsonify({'message' : '이미 존재하는 냉장고 입니다', 'status' : 0})


# 냉장고 삭제 메소드 
@fridge_BP.route('/delete_Refri', methods=['DELETE'])
def delete_Refri():
    data = request.json
    refri_ID = data.get('Refri_ID')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = """
            delete from Refri where Refri_ID=%s
        """
        cursor.execute(sql, (refri_ID, ))
        connection.commit()
    connection.close()

    return jsonify({"message" : "성공적으로 삭제되었습니다", "status" : 1})


# 냉장고에 음식 추가 또는 업데이트
# 동일한 음식이 다른 날짜로 추가되는 경우 기존 데이터를 수정하는 것이 아닌 새 행을 추가
# 최종적으로 현재 냉장고 재고 취합 데이터를 유저에게 보여주는 방식
    # 사과(15일, 2), 사과(17일, 1)라면 취합 한 형태로 사과(3)으로 보여주도록 함
@fridge_BP.route('/add_food', methods=['POST']) 
def add_food():
    # 요청 데이터 가져오기
    food_data = request.json
    refr_id = food_data.get('Refri_ID')
    food_name = food_data.get('Food_Name')
    input_date = food_data.get('Input_Date')  # 현재 날짜로 설정
    exp_date = food_data.get('Exp_Date')  
    cat_name = food_data.get('Cat_Name')
    count = food_data.get('Count')
    type_ = food_data.get('Type')


    # 필수 필드 확인
    if not all([refr_id, food_name, input_date, count, cat_name, exp_date, type_]):
        return jsonify({"error": "refri_id, food_name, input_date, count, cat_id, exp_date, and type are required"}), 400

    # 날짜 유효성 확인 및 변환
    try:
        input_date_str = datetime.strptime(input_date, '%Y-%m-%d').strftime('%Y-%m-%d')  # 입력일도 문자열로 변환
        exp_date_str = datetime.strptime(exp_date, '%Y-%m-%d').strftime('%Y-%m-%d')  # 유통기한도 문자열로 변환
    except ValueError:
        return jsonify({"error": "Date format should be YYYY-MM-DD", 'status' : 0})

    # 데이터베이스 연결
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # 음식 중복 여부 확인
        sql = """
            SELECT * 
            FROM contain 
            WHERE 
                Refri_ID = %s AND
                food_name = %s AND 
                input_date = %s AND
                exp_date = %s AND
                cat_name = %s;
        """
        
        cursor.execute(sql, (refr_id, food_name, input_date_str, exp_date_str, cat_name))
        result = cursor.fetchone()

        if result:
            # 이미 냉장고에 동일 정보의 음식이 있을 경우 수량 및 유통기한 업데이트
            new_count = int(result['count']) + int(count)
            update_sql = '''
                UPDATE contain 
                SET count = %s, input_date = %s, exp_date = %s, type = %s
                WHERE food_name = %s AND cat_name = %s AND Refri_ID = %s AND
                    input_date = %s AND exp_date = %s 
            '''
            cursor.execute(update_sql, (new_count, input_date_str, exp_date_str, type_, food_name, cat_name, refr_id, input_date_str, exp_date_str))
            message = "재고가 업데이트 되었습니다."
        else:
            # 냉장고에 음식이 없을 경우 새로 추가
            insert_sql = '''
                INSERT INTO contain (Refri_id, food_name, input_date, exp_date, cat_name, count, type, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
            '''
            cursor.execute(insert_sql, (refr_id, food_name, input_date_str, exp_date_str, cat_name, count, type_))
            message = f"{food_name}가 {count}만큼 추가되었습니다"

        # 변경사항 커밋
        connection.commit()

    # 연결 종료
    connection.close()
    return jsonify({"message": message, 'status' : 1})



# 음식삭제
@fridge_BP.route('/delete_food', methods=['DELETE'])
def delete_food():
    # 요청 데이터 가져오기
    food_data = request.json
    refr_id = food_data.get('Refri_ID')
    food_name = food_data.get('Food_Name')
    input_date = food_data.get('Input_Date')
    exp_date = food_data.get('Exp_Date')  
    cat_name = food_data.get('Cat_Name')
    count = food_data.get('Count')
    type_ = food_data.get('Type')
    

    # 필수 필드 확인
    if not all([refr_id, food_name, input_date, exp_date]):
        return jsonify({"error": "Refri_ID, food_name, input_date, and exp_date are required"}), 400

    # 데이터베이스 연결
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # 음식 존재 여부 확인
        sql_check = '''
        SELECT * FROM contain
        WHERE Refri_ID = %s AND food_name = %s AND input_date = %s AND exp_date = %s 
        AND cat_name=%s AND count=%s AND type=%s
        '''
        cursor.execute(sql_check, (refr_id, food_name, input_date, exp_date, cat_name, count, type_))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "The specified food item does not exist."}), 404

        # 음식 삭제
        delete_sql = '''
        DELETE FROM contain
        WHERE Refri_ID = %s AND food_name = %s AND input_date = %s AND exp_date = %s 
        AND cat_name=%s AND count=%s AND type=%s
        '''
        cursor.execute(delete_sql, (refr_id, food_name, input_date, exp_date, cat_name, count, type_))
        connection.commit()

    # 연결 종료
    connection.close()
    return jsonify({"message": f"{food_name}가 성공적으로 삭제되었습니다", 'status' : 1})


def generate_token():
    return str(uuid.uuid4())