from flask import Blueprint, jsonify, request
from DB import get_db_connection


# Blueprint 설정
search_BP = Blueprint('Search', __name__)


# 특정 유저소유의 냉장고 ID를 불러옴
@search_BP.route('/get_Refri_ID', methods=['POST'])
def get_Refri_ID():
    new_data = request.json
    User_ID = new_data.get('User_ID')
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = """select Refri_ID, Refri_Name from Refri where user_id=%s order by Refri_Name"""
        cursor.execute(sql, (User_ID, ))
        result = cursor.fetchall()
    connection.close()
    return jsonify(result)



# 특정 냉장고 ID의 contain을 불러옴
@search_BP.route('/fridge_search', methods=['POST'])
def search_fridge():
    new_data = request.json
    refri_id =new_data.get('Refri_ID')

    if not refri_id:
        return jsonify({"message": "해당 냉장고에는 음식이 저장되지 않았습니다", "status" : 0})
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Refri_ID가 일치하는 모든 음식 정보를 검색
            sql = """
            SELECT *
            FROM contain
            WHERE Refri_ID = %s
            """
            cursor.execute(sql, (refri_id,))
            data = cursor.fetchall()  # 결과 가져오기

        return jsonify(data)  # 검색 결과 반환
    finally:
        connection.close()
