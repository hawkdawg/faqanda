from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Beanie'}

    questions = [
            {
                'author': {'username': 'Hank'},
                'title': 'T ball q 1',
                'body': 'What is a tennis ball?'
            },
            {
                'author': {'username': 'Dan'},
                'title': 'T ball q 2',
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
    return render_template(
            'index.html',
            title='Home',
            user=user,
            questions=questions,
            answers=answers)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template(
            'login.html',
            title='Sign In',
            form=form)
