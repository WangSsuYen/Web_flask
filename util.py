import pymysql as sql


class connect_data:
    def __init__(self) -> None:
        self.db_setting = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "Rock30468",
            "db": "festival_data",
            "charset": "utf8"}


    def connect_SQL(self):
        conn = sql.connect(**self.db_setting)
        cursor = conn.cursor()
        try:
            conn = sql.connect(**self.db_setting)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM buy_food_tb")  # 修正 SQL 查询语句的拼写错误
            data = cursor.fetchall()
            print(data)
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()
