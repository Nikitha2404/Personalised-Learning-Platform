from flask import render_template,url_for,redirect,request,session
from website import app
import psycopg2
import os


def db_conn():
    conn = psycopg2.connect(database="projdb", host="localhost", user="postgres",password="admin@123",port="5432")
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

def get_questions(LessonId):
    conn = db_conn()
    cur = conn.cursor()
    
    select_query = f'''SELECT question,option1,option2,option3,option4,option5,correctanswer,difficulty FROM questionbank where lesson_id={LessonId};'''
    cur.execute(select_query)
    questions = cur.fetchall()
    # print(questions)

    return questions

def calculate_score(difficulty, time_taken,answered):
    # Assign weights based on difficulty
    weight_difficulty = 3 if difficulty == "hard" else 2 if difficulty == "medium" else 1 
    # Calculate score for the question
    score = ((weight_difficulty * answered )/(int(time_taken)))*10
    return score

def adaptive_algorithm(index,user_answer,correct_answer,difficulty,time_taken):
    if user_answer == correct_answer:
        answered = 1
    else:
        answered = 0
    question_score = calculate_score(difficulty, time_taken,answered)
    #score=score + question_score
    print(difficulty," ",time_taken," ",question_score)
    if(question_score<=3):
        difficulty='easy'
        index[0]+=1
    elif(question_score>3 and question_score<=6):
        difficulty='medium'
        index[1]+=1
    else:
        difficulty='hard'
        index[2]+=1
    
    print(index)
    print("Score:",question_score)
    return question_score,difficulty,index

# Flask route to render the quiz template

@app.route('/courses/<int:CourseId>/lessons/<int:LessonId>/quiz', methods=['GET', 'POST'])
def quiz(CourseId, LessonId):
    questions = get_questions(LessonId)
    easy_questions = [q for q in questions if q[-1].lower() == 'easy']
    medium_questions = [q for q in questions if q[-1].lower() == 'medium']
    hard_questions = [q for q in questions if q[-1].lower() == 'hard']

    if 'index' not in session:
        session['index'] = [1, 0, 0]
        session['current_question'] = 1
        session['score'] = 0
        session['currentscore'] = 0

    if request.method == 'POST':
        user_answer = request.form['user_answer']
        correct_answer = request.form['correct_answer']
        difficulty = request.form['difficulty']
        time_taken = request.form.get('time_taken')

        # Your code for converting user_answer to 'A', 'B', 'C', 'D', or 'E'
        if user_answer == request.form['option1']:
            user_answer = 'A'
        elif user_answer == request.form['option2']:
            user_answer = 'B'
        elif user_answer == request.form['option3']:
            user_answer = 'C'
        elif user_answer == request.form['option4']:
            user_answer = 'D'
        else:
            user_answer = 'E'

        currentscore, difficulty, index = adaptive_algorithm(
            session['index'], user_answer, correct_answer, difficulty, time_taken)

        session['score'] += currentscore

        if difficulty == 'easy':
            current_question_data = get_question_data(easy_questions, index[0])
        elif difficulty == 'medium':
            current_question_data = get_question_data(medium_questions, index[1])
        else:
            current_question_data = get_question_data(hard_questions, index[2])

        session['index'] = index

        if session['current_question'] == 5:  # Assuming there are 5 questions
            return render_template('quiz_result.html', score=session['score'])

        session['current_question'] += 1

    else:
        
        current_question_data = get_question_data(
            easy_questions, session['index'][0])

    return render_template('quiz.html',
                           question=current_question_data[0],
                           options=current_question_data[1:6],
                           correct_answer=current_question_data[6],
                           difficulty=current_question_data[7],
                           course_id=CourseId, lesson_id=LessonId)


def get_question_data(questions_list, index):
    return questions_list[index]
