from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


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
    question_comments = db.relationship(
            'QuestionComment',
            backref='author',
            lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    '''user loader function: write logged state of the user to the user session'''
    return User.query.get(int(id))

QuestionTag = db.Table(
        'question_tag',
        db.Column('q_id', db.Integer, db.ForeignKey('question.q_id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')))


class Question(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    q_title = db.Column(db.String(140))
    q_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.CLOB)
    question_comments = db.relationship(
            'QuestionComment',
            backref='comments',
            lazy='dynamic')
    tags = db.relationship(
            'Tag',
            secondary=QuestionTag,
            backref=db.backref('Question', lazy='dynamic'),
            lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.q_title)


    def tag_question(self, tag):
        if not self.is_tagged(tag=tag):
            self.tags.append(tag)

    def untag_question(self, tag):
        if self.is_tagged(tag=tag):
            self.tags.remove(tag)

    def is_tagged(self, tag):
        return self.tags.filter(
                QuestionTag.c.tag_id == tag.tag_id).count() > 0

class QuestionComment(db.Model):
    qc_id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, db.ForeignKey('question.q_id'))
    qc_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted = db.Column(db.Integer)
    body = db.Column(db.String(500))  # TODO determine best size

    def __repr__(self):
        return '<Question Comment> {} - {}'.format(self.qc_id, self.body)


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    deleted = db.Column(db.Integer)
    questions = db.relationship(
            'Question',
            secondary=QuestionTag,
            backref=db.backref('Tag', lazy='dynamic'),
            lazy='dynamic')

    def __repr__(self):
        return '<Tag Name> {}'.format(self.name)

#
#class Answer(db.Model):
#    pass
#
#class AnswerDetail(db.Model):
#    pass
#
#class AnswerComment(db.Model):
#    pass


