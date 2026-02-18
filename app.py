from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file

from datetime import datetime

from openpyxl import Workbook

from io import BytesIO



app = Flask(__name__)

app.secret_key = "vinfast_secret_key_2026"



# Lưu dữ liệu trong RAM (mất khi server restart - phù hợp dùng trong ngày)

DATA = []



USERNAME = "admin"

PASSWORD = "123456"





@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:

            session["logged_in"] = True

            return redirect(url_for("index"))

        else:

            flash("Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")





@app.route("/logout")

def logout():

    session.clear()

    return redirect(url_for("login"))





@app.route("/", methods=["GET", "POST"])

def index():

    if "logged_in" not in session:

        return redirect(url_for("login"))



    if request.method == "POST":

        record = {

            "name": request.form["name"],

            "phone": request.form["phone"],

            "repair": request.form["repair"],

            "total": request.form["total"],

            "method": request.form["method"],

            "date": datetime.now().strftime("%d-%m-%Y"),

        }



        DATA.append(record)

        flash("Đã lưu thành công!")

        return redirect(url_for("list_today"))



    return render_template("index.html")





@app.route("/list")

def list_today():

    if "logged_in" not in session:

        return redirect(url_for("login"))



    today = datetime.now().strftime("%d-%m-%Y")

    today_data = [d for d in DATA if d["date"] == today]



    return render_template("list.html", data=today_data, today=today)





@app.route("/export")

def export_excel():

    if "logged_in" not in session:

        return redirect(url_for("login"))



    today = datetime.now().strftime("%d-%m-%Y")

    today_data = [d for d in DATA if d["date"] == today]



    wb = Workbook()

    ws = wb.active

    ws.append(["Họ và Tên", "SĐT", "Thông tin sửa chữa", "Thành tiền", "CK/TM"])



    for d in today_data:

        ws.append([d["name"], d["phone"], d["repair"], d["total"], d["method"]])



    output = BytesIO()

    wb.save(output)

    output.seek(0)



    filename = f"vinfast_{today}.xlsx"

    return send_file(output, as_attachment=True, download_name=filename)





if __name__ == "__main__":

    app.run()