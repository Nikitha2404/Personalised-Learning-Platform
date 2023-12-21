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

def get_questions():
    conn = db_conn()
    cur = conn.cursor()
    
    select_query = f'''SELECT question,option1,option2,option3,option4,option5,correctanswer FROM questionbank;'''
    cur.execute(select_query)
    questions = cur.fetchall()
    print(questions)

    return questions

# Flask route to render the quiz template
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        current_question = int(request.form['current_question'])
        user_answer = request.form['user_answer']
        correct_answer = request.form['correct_answer']
        score = int(request.form['score'])

        if user_answer == 'Only conclusion 1 follows':
            user_answer = 'A'
        elif user_answer == 'Only conclusion 2 follows':
            user_answer = 'B'
        elif user_answer == 'Either 1 or 2 follows':
            user_answer = 'C'
        elif user_answer == 'Neither 1 nor 2 follows':
            user_answer = 'D'
        else:
            user_answer - 'E'

        if user_answer == correct_answer:
            score += 1

        if current_question == 5:  # Assuming there are 10 questions
            return render_template('quiz_result.html', score=score)

        current_question += 1

    else:
        current_question = 1
        score = 0

    questions = get_questions()
    current_question_data = questions[current_question - 1]

    return render_template('quiz.html',
                           current_question=current_question,
                           score=score,
                           question=current_question_data[0],
                           options=current_question_data[1:6],
                           correct_answer=current_question_data[6])
