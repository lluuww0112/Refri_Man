
# 서버 구현용
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# 스케쥴러 임포팅
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# DB 제어용
import pymysql
import pandas as pd

# API추가
from DB import get_db_connection
from API.Register import regist_BP
from API.fridge import fridge_BP
from API.Notification import notification_BP
from API.Search import search_BP


app = Flask(__name__)

# CORS 정책 추가
CORS(app)


# API 요청 포인트 추가
app.register_blueprint(regist_BP, url_prefix='/Regist')
app.register_blueprint(fridge_BP, url_prefix='/Fridge')
app.register_blueprint(notification_BP, url_prefix='/Notify')
app.register_blueprint(search_BP, url_prefix='/Search')
 


# 각 페이지 정의
@app.route('/')
def Login():
    return render_template('/html/Login/LogIn_page.html')

@app.route('/Registration_page')
def Regist():
    return render_template('/html/Login/Registration_page.html')

@app.route('/main_page')
def Main():
    return render_template('/html/Main/main.html')

@app.route('/contain_page')
def Contain():
    return render_template('/html/Main/contain_page.html')


# status업데이트 함수 정의
def update_status():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = """
            WITH exp_table AS (
                SELECT exp_day, refri_id  
                FROM contain
                    NATURAL JOIN category
            )
            UPDATE contain 
                JOIN exp_table  ON contain.refri_id = exp_table.refri_id  
                SET contain.status = CASE
                    WHEN DATEDIFF(contain.exp_date, CURDATE()) > exp_table.exp_day THEN 0
                    WHEN DATEDIFF(contain.exp_date, CURDATE()) = exp_table.exp_day THEN 1
                    WHEN DATEDIFF(contain.exp_date, CURDATE()) < 0 THEN 2
            END;
            """
        cursor.execute(sql)
        connection.commit()
    connection.close()


# 스케쥴러 초기화 및 실행
def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # 매일 자정에 실행
    trigger = CronTrigger(hour=0, minute=0)  
    scheduler.add_job(update_status, trigger=trigger, id='daily_task')
    
    scheduler.start()



if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True, port=5001)
