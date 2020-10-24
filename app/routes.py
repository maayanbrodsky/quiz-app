from pathlib import Path

from flask import render_template, request, send_file

from app import app
from app.forms import QuizQuestions
from app.generator import genereate_question_list, generate_quizzes


def get_numbers(form_results):
    form_values = [(value[1:3], value[3:5], value[5:]) for value in list(form_results) if value[0] == 'q']
    new_values = []
    for value in form_values:
        new_nums = []
        for num in value:
            if num[0] == '0':
                num = num[1]
            new_nums.append(num)
        new_nums = [int(num) for num in new_nums]
        new_values.append(tuple(new_nums))
    return new_values


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    path = Path(__file__).parent / 'static'
    form = QuizQuestions()
    if request.method == 'GET':
        return render_template('questions.html', title='question selection', form=form)
    if request.method == 'POST':
        question_list = get_numbers(request.values)
        print(question_list)
        questions = genereate_question_list(question_list)
        generate_quizzes(questions)
        return send_file(path / 'quiz_files.zip')
        # return redirect('/file-download')


# @app.route("/")
# def file_sender():
#     return flask.send_file("static/quiz.txt")


# @app.route('/file-download')
# def file_download():
#     return send_file("/static/quiz.txt")
    # return render_template('file-download.html', title='download')
