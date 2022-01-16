from . import db # import the database from the website package
from flask_login import UserMixin # custom user class to inherit from
from sqlalchemy.sql import func # import the func function from sqlalchemy and gives default values by itself

class User(db.Model, UserMixin): # create a new class to inherit from the UserMixin class
    id = db.Column(db.Integer, primary_key=True) # create a new column called id with type Integer and primary key
    email = db.Column(db.String(150), unique=True, nullable=False) # create a new column called email with type String and unique and has to be filled
    password = db.Column(db.String(150), nullable=False) # create a new column called password with type String and has to be filled
    first_name = db.Column(db.String(150))

class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    course_acronym = db.Column(db.String(15))
    course_number = db.Column(db.Integer)
    question = db.Column(db.String(500))

    answers = db.relationship('Answer', back_populates='question')
    
class Answer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer = db.Column(db.String(1000))

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', back_populates='answers')