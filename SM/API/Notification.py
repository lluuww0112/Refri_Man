from flask import Blueprint, jsonify, request
from datetime import datetime
from DB import get_db_connection

# Blueprint 설정
notification_BP = Blueprint('Notification', __name__)

@notification_BP.route('/check_expiry', methods=['GET'])
def check_expiry():
    """
    contain 테이블에서 input_date를 기준으로 유통기한이 임박했거나 지난 음식의 알림을 반환합니다.
    특정 냉장고 ID(Refri_ID)에 대해 확인합니다.
    """
    today = datetime.now().date()  # 현재 날짜

    # Refri_ID 가져오기
    refri_id = request.args.get('Refri_ID')  # 쿼리 매개변수에서 Refri_ID 가져오기
    if not refri_id:
        return jsonify({"message": "Please provide a Refri_ID."}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 유통기한이 임박한 항목 (input_date 기준으로 exp_date가 가까운 것)
            sql_expiry_soon = """
            SELECT food_name, input_date, exp_date 
            FROM contain 
            WHERE Refri_ID = %s 
              AND DATEDIFF(exp_date, input_date) <= DATEDIFF(%s, input_date)
              AND DATEDIFF(exp_date, %s) >= 0
            """
            cursor.execute(sql_expiry_soon, (refri_id, today, today))
            expiry_soon = cursor.fetchall()  # 임박한 유통기한 결과 가져오기

            # 유통기한이 지난 항목
            sql_expired = """
            SELECT food_name, input_date, exp_date 
            FROM contain 
            WHERE Refri_ID = %s 
              AND DATEDIFF(exp_date, %s) < 0
            """
            cursor.execute(sql_expired, (refri_id, today))
            expired = cursor.fetchall()  # 이미 유통기한이 지난 결과 가져오기

        # 데이터 처리
        response = {
            "expiry_soon": [
                {
                    "food_name": item["food_name"],
                    "input_date": item["input_date"].strftime('%Y-%m-%d'),
                    "exp_date": item["exp_date"].strftime('%Y-%m-%d'),
                    "days_left": (item["exp_date"] - today).days
                }
                for item in expiry_soon
            ],
            "expired": [
                {
                    "food_name": item["food_name"],
                    "input_date": item["input_date"].strftime('%Y-%m-%d'),
                    "exp_date": item["exp_date"].strftime('%Y-%m-%d'),
                }
                for item in expired
            ]
        }

        return jsonify(response)
    finally:
        connection.close()
