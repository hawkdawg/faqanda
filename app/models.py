from datetime import datetime
from time import time
import jwt
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from app import app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    questions = db.relationship(
            'Question',
            backref='author',
            lazy='dynamic')
    about_me = db.Column(db.String(240))
    deleted = db.Column(db.Boolean, default=False)
    last_visited = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        ''' expirers in 10 minutes = 600 seconds'''
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def get_users_questions(self, user_id):
        return Question.query.filter_by(user_id=user_id)


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            print('HERE')
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    '''user loader function: write logged state of the user to the user session'''
    return User.query.get(int(id))

QuestionTag = db.Table(
        'question_tag',
        db.Column('q_id', db.Integer, db.ForeignKey('question.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.CLOB)
    tags = db.relationship(
            'Tag',
            secondary=QuestionTag,
            backref=db.backref('Question', lazy='dynamic'),
            lazy='dynamic')

    answer = db.relationship(
            'Answer',
            backref='question',
            lazy='dynamic')



    def __repr__(self):
        return '<Question {}>'.format(self.title)


    def tag_question(self, tag):
        if not self.is_tagged(tag=tag):
            self.tags.append(tag)

    def untag_question(self, tag):
        if self.is_tagged(tag=tag):
            self.tags.remove(tag)

    def is_tagged(self, tag):
        return self.tags.filter(
                QuestionTag.c.tag_id == tag.tag_id).count() > 0

    @staticmethod
    def get_recent_questions(limit):
        return Question.query.order_by(Question.date.desc()).limit(limit).all()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    deleted = db.Column(db.Boolean, default=False)
    questions = db.relationship(
            'Question',
            secondary=QuestionTag,
            backref=db.backref('Tag', lazy='dynamic'),
            lazy='dynamic')

    def __repr__(self):
        return '<Tag Name> {}'.format(self.name)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    choosen = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.CLOB)

    def __repr__(self):
        return '<Answer ID> {}'.format(self.id)


