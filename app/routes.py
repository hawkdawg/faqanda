from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Beanie'}

    questions = [
            {
                'author': {'username': 'Hank'},
                'body': 'What is a tennis ball?'
            },
            {
                'author': {'username': 'Dan'},
                'body': 'Why are there tennis balls?'
            }
    ]
    answers = [
            {
                'author': {'username': 'Beanie'},
                'body': 'You chase tennis balls.'
            },
            {
                'author': {'username': 'Beanie'},
                'body': 'To chase.'
            }
    ]
    return render_template('index.html', title='Home', user=user, questions=questions, answers=answers)
