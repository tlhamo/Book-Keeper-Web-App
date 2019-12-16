from app import datab
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin

class RegisterForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
	email    = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(min=6, max=75)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100)])

readers = datab.Table('readers',
    datab.Column('user_id', datab.Integer, datab.ForeignKey('user.id')),
    datab.Column('book_id', datab.Integer, datab.ForeignKey('book.id'))
    )

class User(datab.Model, UserMixin):
    id = datab.Column(datab.Integer, primary_key=True)
    username = datab.Column(datab.String(20), unique=True)
    email = datab.Column(datab.String(75), unique=True)
    password = datab.Column(datab.String(100))
    books = datab.relationship('Book', secondary=readers, backref=datab.backref('bookworms',lazy='dynamic'))

class Author(datab.Model):
    id = datab.Column(datab.Integer, primary_key=True)
    name = datab.Column(datab.String())
    books = datab.relationship('Book', backref='owner')

class Book(datab.Model):
    id = datab.Column(datab.Integer, primary_key=True)
    title = datab.Column(datab.String(50), unique=True)
    year = datab.Column(datab.Integer)
    rating = datab.Column(datab.Integer)
    image_url = datab.Column(datab.String)
    owner_id = datab.Column(datab.Integer, datab.ForeignKey('author.id'))
