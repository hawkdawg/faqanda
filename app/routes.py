from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():

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
            questions=questions,
            answers=answers)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # redirect to page user was trying to go to
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template(
            'login.html',
            title='Sign In',
            form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a FAQandAer!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    questions = [
            {'author': user,
            'q_title': 'title lorem ipsum # 1',
            'body': "1 body lorem ipsum dolor sit amet, soleat forensibus"},

            {'author': user,
            'q_title': 'test title lorm ipsum # 2',
            'body': "2 lorem ipsum dolor sit amet, soleat forensibus signiferumque?"}]

    return render_template('user.html', user=user, questions=questions)
