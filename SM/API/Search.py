from flask import Blueprint, jsonify, request
from DB import get_db_connection

# Blueprint 설정
search_BP = Blueprint('Search', __name__)

@search_BP.route('/fridge_search', methods=['GET'])
def search_fridge():
    """
    Query parameter 'Refri_ID'를 사용하여 해당 냉장고 ID에 있는 모든 음식 정보를 검색합니다.
    """
    refri_id = request.args.get('Refri_ID')  # 검색할 Refri_ID 가져오기
    if not refri_id:
        return jsonify({"message": "Please provide a Refri_ID."}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Refri_ID가 일치하는 모든 음식 정보를 검색
            sql = """
            SELECT food_name, input_date, exp_date, cat_id, count, type
            FROM contain
            WHERE Refri_ID = %s
            """
            cursor.execute(sql, (refri_id,))
            data = cursor.fetchall()  # 결과 가져오기

        if not data:
            return jsonify({"message": "No food items found for the given Refri_ID."}), 404
        
        return jsonify(data)  # 검색 결과 반환
    finally:
        connection.close()
