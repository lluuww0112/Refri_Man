from flask import Blueprint, jsonify, request
from datetime import datetime
from DB import get_db_connection

# Blueprint 설정
history_BP = Blueprint('History', __name__)

@history_BP.route('/get_History', methods=['GET', 'POST'])
def get_history_with_ID():
    new_data = request.json
    user_id = new_data.get('User_ID')


    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = """
            select history_id, H.user_id, food_name, input_date, refri_name, count
            from 
                History as H
                    join refri as R
                    on H.refri_id=R.refri_id
            where
                H.user_id=%s;
        """
        cursor.execute(sql, (user_id, ))
        response = cursor.fetchall()
    connection.close()

    return jsonify(response)
