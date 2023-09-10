from flask import Flask, session, url_for
from flask import redirect, render_template, request, Response
import pymysql as sql
from datetime import *
import re


app = Flask(__name__)
app.secret_key = 'AdreanRock1314'


class connect_data:
    def __init__(self) -> None:
        self.db_setting = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "Rock30468",
            "db": "festival_data",
            "charset": "utf8"}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = None
        login_phone = request.form.get("phone")
        login_password = request.form.get('pswd')
        try:
            connection = connect_data()
            conn = sql.connect(**connection.db_setting)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT  user_id , user_password FROM user WHERE user_id = %s AND user_password = %s ;",
                (login_phone, login_password))
            result = cursor.fetchone()

            if result:
                session['username'] = request.form.get("phone")
                return redirect(url_for("insert"))
            else:
                mesg = "用户名或密码错误"
                return render_template("login.html", errmsg=mesg)
        except Exception as er:
            mesg = er
            return render_template("login.html", errmsg=mesg)

    return render_template("login.html")


@app.route("/snp", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_phone = request.form.get("phone")
        user_password = request.form.get('pswd')
        Systime = datetime.now()
        # --
        if not re.match(r"^[0][9]\d{8}$", user_phone):
            mesg = "手機格式錯誤，請重新輸入!"
            return render_template("signup.html", errmsg=mesg)
        # --
        if len(user_password) != 8:
            mesg = "密碼格式錯誤，請重新輸入!"
            return render_template("signup.html", errmsg=mesg)
        # --
        result = None
        connection = connect_data()
        conn = sql.connect(**connection.db_setting)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE user_id = %s ; ", (user_phone))
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO user (user_id , user_password , creattm) VALUES (%s , %s , %s);",
                           (user_phone, user_password, Systime))
            conn.commit()
            return redirect(url_for("login"))
        else:
            mesg = "此帳號已被註冊!"
            return render_template("signup.html", errmsg=mesg)

    return render_template("signup.html")


@app.route("/ins", methods=["GET", "POST"])
def insert():
    if "username" in session:
        if request.method == "GET":
            print(session["username"])
            return render_template("insert.html")

        else:
            # 計算POST回傳數量
            num_fields = len(request.form) // 4

            for a in range(1, num_fields+1):
                # 抓取POST回傳的數值
                id = session['username']
                item_name = request.form.get(f"pickles_name{a}")
                quantity = request.form.get(f"pickles_quantity{a}")
                kind = request.form.get(f"kind{a}")
                price = request.form.get(f"pickles_price{a}")
                # 抓取現在時間
                Systime = datetime.now()

                connection = connect_data()
                conn = sql.connect(**connection.db_setting)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO buy_food_tb (user_id ,item , count , kind , amount , creat_time) VALUES (? , ? , ? , ? , ? , ?);",
                               (id, item_name, quantity, kind, price, Systime))
                conn.commit()

    else:
        esmg = "您尚未登入!"
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
