from flask import render_template,url_for,redirect,request
from website import app
import psycopg2
import os

def db_conn():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres",password="K$ham@29",port="5432")
    return conn

@app.route('/')
def index():
    return render_template('course.html')




