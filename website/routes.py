from flask import render_template,url_for,redirect,request
from website import app
import psycopg2
import os

def db_conn():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres",password="pgpassword",port="5432")
    return conn

@app.route('/')
def course():

    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM course;'''
    cur.execute(select_query)
    data = cur.fetchall()

    return render_template('course.html',data=data)

@app.route('/11')
def syllogisum():
     
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM lesson where course_id=11;'''
    cur.execute(select_query)
    data = cur.fetchall()

    return render_template('lesson.html',data=data)


@app.route('/111')
def syllogisuml1():
     
    return render_template('material.html')

@app.route('/quiz')
def quiz():

    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM questionbank where lesson_id=1;'''
    cur.execute(select_query)
    data = cur.fetchall()

    return render_template('quiz.html',data=data)