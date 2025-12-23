from flask import Flask, render_template, request,session
import mysql.connector
import random
from datetime import datetime
import requests
import os
from datetime import date

app = Flask(__name__)

app.secret_key = '12345678'
conn_data = {
     "host":'localhost',
    "user":'root',
    "password":'',
    "database":'mail_phishing'
}


@app.route('/register', methods=["GET"])
def register():
    return render_template('register.html')


@app.route('/add_account', methods=["POST"])
def add_account():
       
        conn = mysql.connector.connect(
                    host=conn_data["host"],
                    user=conn_data["user"],
                    password=conn_data["password"],
                    database=conn_data["database"]
            )
        name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO users (fullname, email, password)
                VALUES (%s, %s, %s)
            """, (name, email, password))
        conn.commit()
        conn.close()
        return render_template('login.html')


@app.route('/login', methods=["GET"])
def login():
    return render_template('login.html')


@app.route('/login_act', methods=["POST"])
def login_act():
    email = request.form.get('email')
    password = request.form.get('password')
    conn = mysql.connector.connect(
                    host=conn_data["host"],
                    user=conn_data["user"],
                    password=conn_data["password"],
                    database=conn_data["database"]
            )
    cursor = conn.cursor()
    cursor.execute("""
                SELECT id FROM users WHERE email = %s and password=%s
            """, (email,password))
    result = cursor.fetchall()
    if result:
         result = result[0]
    cursor.close()
    if result:
        session['user_id'] = result[0]
        return render_template('Home.html',message="done")
    return render_template('login.html',message="error")
    


app.run()