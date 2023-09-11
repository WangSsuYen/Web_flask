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
    mesg = None
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
    mesg = None
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
    mesg = None
    succ_mesg = None
    if request.method == "GET":
        if "username" not in session:
            return redirect(url_for("login"))
        else:
            print(session["username"])
            return render_template("insert.html")

    else:
        # 計算POST回傳數量
        data_list = []
        num_fields = len(request.form) // 4

        for a in range(1, num_fields+1):
            id = session['username']
            item_name = request.form.get(f"pickles_name{a}")
            quantity = request.form.get(f"pickles_quantity{a}")
            kind = request.form.get(f"kind{a}")
            price = request.form.get(f"pickles_price{a}")

            if id == "" or item_name == "" or quantity == "" or kind == "" or price == "":
                mesg = "有空資料，請重新檢查後再送出。"
                return render_template("insert.html", errmsg=mesg)
            # 判斷每筆資料無誤後，再存入data_list
            data = {
                "id": id,
                "item_name": item_name,
                "quantity": quantity,
                "kind": kind,
                "price": price
            }
            data_list.append(data)

        connection = connect_data()
        conn = sql.connect(**connection.db_setting)
        cursor = conn.cursor()
        for data in data_list:
            id = data["id"]
            item_name = data["item_name"]
            quantity = data["quantity"]
            kind = data["kind"]
            price = data["price"]
            Systime = datetime.now()  # 抓取現在時間
            cursor.execute("INSERT INTO buy_food_tb (user_id ,item , count , kind , amount , creat_time) VALUES (%s , %s , %s , %s , %s , %s);",
                           (id, item_name, quantity, kind, price, Systime))
            conn.commit()
        succ_mesg = "資料已儲存成功!"
        return render_template("insert.html", succ_msg=succ_mesg)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
