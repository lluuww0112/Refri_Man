from flask import Blueprint, jsonify, request
import pymysql
from DB import get_db_connection
from datetime import datetime
from API.fridge import fridge_BP  # Blueprint 가져오기
# Blueprint 설정
fridge_BP = Blueprint('Fridge', __name__)

# 냉장고에 음식 추가 또는 업데이트
@fridge_BP.route('/add_food', methods=['POST']) 
def add_food():
    # 요청 데이터 가져오기
    food_data = request.json
    refr_id = food_data.get('Refri_ID')
    food_name = food_data.get('food_name')
    input_date = food_data.get('input_date')  
    count = food_data.get('count')
    cat_id = food_data.get('cat_id')
    exp_date = food_data.get('exp_date')  
    type_ = food_data.get('type')

    # 필수 필드 확인
    if not all([refr_id, food_name, input_date, count, cat_id, exp_date, type_]):
        return jsonify({"error": "refri_id, food_name, input_date, count, cat_id, exp_date, and type are required"}), 400

    # 날짜 유효성 확인 및 변환
    try:
        input_date = datetime.strptime(input_date, '%Y-%m-%d')
        exp_date = datetime.strptime(exp_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Date format should be YYYY-MM-DD"}), 400

    # 데이터베이스 연결
    connection = get_db_connection()
    with connection.cursor() as cursor:
        #음식 중복 여부 확인
        #음식 중복 여부 확인
        sql = 'SELECT count FROM contain WHERE food_name = %s AND cat_id = %s AND Refr_ID = %s'
        cursor.execute(sql, (food_name, cat_id, refr_id))
        result = cursor.fetchone()

        if result:
            # 이미 냉장고에 음식이 있을 경우 수량 및 유통기한 업데이트
            new_count = result['count'] + count
            update_sql = '''
                UPDATE contain 
                SET count = %s, input_date = %s, exp_date = %s, type = %s
                WHERE food_name = %s AND cat_id = %s AND refr_id = %s
            '''
            cursor.execute(update_sql, (new_count, input_date, exp_date, type_, food_name, cat_id, refr_id))
            message = f"{food_name} quantity updated to {new_count} with new expiration date {exp_date}."
        else:
            # 냉장고에 음식이 없을 경우 새로 추가
            insert_sql = '''
            INSERT INTO contain (Refri_id, food_name, input_date, count, cat_id, exp_date, type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
        cursor.execute(insert_sql, (refr_id, food_name, input_date, count, cat_id, exp_date, type_))
        message = f"{food_name} added to contain with quantity {count}."

        # 변경사항 커밋
        connection.commit()

    # 연결 종료
    connection.close()
    return jsonify({"message": message})

