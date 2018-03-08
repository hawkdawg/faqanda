from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, EditFAQandAForm, AskQuestionForm
from app.models import User, Question
from app.email import send_password_reset_email

@app.before_request
def before_request():
    '''applies to all the routes in the app'''
    # TODO maybe don't need this
    if current_user.is_authenticated:
        current_user.last_visited = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    form = AskQuestionForm() # may need to be q and a form
    if form.validate_on_submit():
        question = Question(
                body=form.question.data,
                title=form.question_title.data,
                author=current_user)
        db.session.add(question)
        db.session.commit()
        flash('Your question has been posted.')
        return redirect(url_for('index')) # keep refresh from resubmitting post req

    questions = Question.get_recent_questions(limit=100)

    answers = [
            {
                'author': {'username': 'beanie'},
                'body': 'You chase tennis balls.'
            },
            {
                'author': {'username': 'beanie'},
                'body': 'To chase.'
            }
    ]
    return render_template(
            'index.html',
            title='Home',
            questions=questions,
            form=form,
            answers=answers)

@app.route('/', methods=['GET', 'POST'])
@app.route('/ask_question', methods=['GET', 'POST'])
@login_required
def ask_question():

    form = AskQuestionForm() # may need to be q and a form
    if form.validate_on_submit():
        question = Question(
                body=form.question.data,
                title=form.question_title.data,
                author=current_user)
        db.session.add(question)
        db.session.commit()
        flash('Your question has been posted.')
        return redirect(url_for('ask_question')) # keep refresh from resubmitting post req

    return render_template(
            'ask_question.html',
            title='Ask Question',
            form=form)



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
    questions = current_user.get_users_questions(user_id=user.id)

    return render_template('user.html', user=user, questions=questions)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # if user is already registered with about me field
    elif request.method == 'GET':  # user is req form to view
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)
from app.forms import ResetPasswordForm


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/edit_faqanda/<question_id>', methods=['GET', 'POST'])
@login_required
def edit_faqanda(question_id):
    form = EditFAQandAForm()
    question = Question.query.filter_by(id=question_id).first_or_404()
    if form.validate_on_submit():
        question.title=form.question_title.data
        question.body=form.question.data
        question.author=current_user
        question.id=question_id
        db.session.add(question)
        db.session.commit()
        flash('Your question has been posted.')

        return redirect(
                url_for('edit_faqanda', question_id=question_id))
    elif request.method == 'GET':
        question = Question.query.filter_by(id=question_id).first()
        form.question_title.data = question.title
        form.question.data = question.body
    return render_template('edit_faqanda.html', title='Edit FAQandA', form=form)
