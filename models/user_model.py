from wtforms import Form, TextField, StringField, validators, PasswordField
from flask_admin.contrib.pymongo import ModelView
from config.database import Mongo
from flask_pymongo import PyMongo

from flask import Flask

app = Flask(__name__) 
app.config['MONGO_DBNAME'] = 'gitnjam'
app.config['MONGO_URI'] = 'mongodb://localhost/gitnjam'
mongo = PyMongo(app) 

class LoginForm(Form):
    email = StringField('Email',
                        [validators.DataRequired(),
                         validators.Length(min=6, max=50)])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.Length(min=8, max=50)])

class SignupForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.Length(min=8, max=50),
                              validators.EqualTo('confirm_password',
                                                 message='Passwords do not match')])
    confirm_password = PasswordField('Confirm Password',
                                     [validators.DataRequired()])

class Users(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])

class UserView(ModelView):
    column_list = ('firtname', 'lastname', 'email', 'role')
    form = Users