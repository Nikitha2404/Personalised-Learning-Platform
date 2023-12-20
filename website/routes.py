from flask import render_template,url_for,redirect,request
from website import app
import psycopg2
import os

def db_conn():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres",password="pgpassword",port="5432")
    return conn

@app.route('/')
def index():
    conn = db_conn()
    print(conn)
    cur = conn.cursor()
    return 'Hello'



