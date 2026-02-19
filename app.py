from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file

from datetime import datetime

from openpyxl import Workbook

from io import BytesIO

import os



app = Flask(__name__)

@app.route("/")

def health_check():

    return "OK", 200
app.secret_key = "vinfast_secret_key_2026"



# Lưu dữ liệu trong RAM (mất khi restart server - phù hợp dùng trong ngày)

DATA = []



USERNAME = "admin"

PASSWORD = "123456"





# =========================

# LOGIN

# =========================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:

            session["logged_in"] = True

            return redirect(url_for("index"))

        else:

            flash("Sai tài khoản hoặc mật khẩu!")

    return render_template("login.html")





# =========================

# LOGOUT

# =========================

@app.route("/logout")

def logout():

    session.clear()

    return redirect(url_for("login"))





# =========================

# TRANG CHÍNH - NHẬP DỮ LIỆU

# =========================

@app.route("/", methods=["GET", "POST"])

def index():

    if not session.get("logged_in"):

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





# =========================

# DANH SÁCH TRONG NGÀY

# =========================

@app.route("/list")

def list_today():

    if not session.get("logged_in"):

        return redirect(url_for("login"))



    today = datetime.now().strftime("%d-%m-%Y")

    today_data = [d for d in DATA if d["date"] == today]



    return render_template("list.html", data=today_data, today=today)





# =========================

# XUẤT EXCEL

# =========================

@app.route("/export")

def export_excel():

    if not session.get("logged_in"):

        return redirect(url_for("login"))



    today = datetime.now().strftime("%d-%m-%Y")

    today_data = [d for d in DATA if d["date"] == today]



    wb = Workbook()

    ws = wb.active

    ws.title = "Báo cáo"



    ws.append(["Họ và Tên", "SĐT", "Thông tin sửa chữa", "Thành tiền", "CK/TM"])



    for d in today_data:

        ws.append([d["name"], d["phone"], d["repair"], d["total"], d["method"]])



    output = BytesIO()

    wb.save(output)

    output.seek(0)



    filename = f"vinfast_{today}.xlsx"



    return send_file(

        output,

        as_attachment=True,

        download_name=filename,

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )





# =========================

# CHẠY SERVER

# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)