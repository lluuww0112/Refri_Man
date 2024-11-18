from flask import Blueprint, jsonify, request
import pymysql
from DB import get_db_connection
from datetime import datetime
from API.fridge import fridge_BP  # Blueprint 가져오기

@fridge_BP.route('/delete_food', methods=['DELETE'])
def delete_food():
    # 요청 데이터 가져오기
    food_data = request.json
    refr_id = food_data.get('Refri_ID')
    food_name = food_data.get('food_name')
    input_date = food_data.get('input_date')
    exp_date = food_data.get('exp_date')

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
        '''
        cursor.execute(sql_check, (refr_id, food_name, input_date, exp_date))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "The specified food item does not exist."}), 404

        # 음식 삭제
        delete_sql = '''
        DELETE FROM contain
        WHERE Refri_ID = %s AND food_name = %s AND input_date = %s AND exp_date = %s
        '''
        cursor.execute(delete_sql, (refr_id, food_name, input_date, exp_date))
        connection.commit()

    # 연결 종료
    connection.close()
    return jsonify({"message": f"{food_name} has been successfully deleted."}), 200
