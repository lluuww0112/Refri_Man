import pymysql 

# 데이터베이스 설정
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "ajdcjddl2"
DB_NAME = "Refri"


# 데이터베이스 연결 함수
def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor  # 쿼리 결과를 dict로 반환
    )
    return connection