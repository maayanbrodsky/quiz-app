from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


from app.question_pool import question_pool


def generate_questions(question_pool):
    questions = []
    for question in question_pool:
        human_formatted = f'{question["q"]}\n'
        questions.append(human_formatted)
    return questions


questions = generate_questions(question_pool)


class QuizQuestions(FlaskForm):
    q150201 = BooleanField(questions[0])
    q150101 = BooleanField(questions[1])
    q150301 = BooleanField(questions[2])
    q150302 = BooleanField(questions[3])
    submit = SubmitField('Generate Quiz')
