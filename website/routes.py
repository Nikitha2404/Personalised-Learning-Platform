from flask import render_template,url_for,redirect,request
from website import app
import psycopg2
import os

def db_conn():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres",password="pgpassword",port="5432")
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/courses')
def course():

    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM course;'''
    cur.execute(select_query)
    data = cur.fetchall()

    return render_template('course.html',data=data)

@app.route('/courses/<int:CourseId>/lessons')
def lessonList(CourseId):
     
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM lesson where course_id={CourseId};'''
    cur.execute(select_query)
    data = cur.fetchall()

    return render_template('lessons.html',data=data)

@app.route('/courses/<int:CourseId>/lessons/<int:LessonId>')
def getMaterial(CourseId, LessonId):

    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM lesson where lesson_id={LessonId} AND course_id={CourseId};'''
    cur.execute(select_query)
    data = cur.fetchall()
    print(data)

    return render_template('material.html',data=data)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')