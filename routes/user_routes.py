from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint
from passlib.hash import sha256_crypt
from models.user_model import *
from flask_pymongo import PyMongo
from functools import wraps
from config.database import Mongo


mongo = Mongo()
user_route = Blueprint('user_route', __name__)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        if 'is_logged_in' in session:
            return f(*args, **kwargs)
        flash('Unauthorized, Please login', 'danger')
        return redirect(url_for('login'))
    return wrap

@user_route.route('/', methods = ['GET', 'POST'])
def landing():
    return render_template('landing.html')

@user_route.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    session.pop('is_logged_in', None)
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})
        if login_user:
            password = login_user['password']
            password_candidate = request.form['password']
            if sha256_crypt.verify(password_candidate, password):
                session['email'] = request.form['email']
                session['is_logged_in'] = True
                return redirect(url_for('dashboard'))

        flash('Invalid Password or Email combination', 'danger')
    return render_template('login.html', form=form)

@user_route.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    session.pop('is_logged_in', None)        
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})
        if existing_user is None:
            hashpass = sha256_crypt.encrypt(str(form.password.data))
            users.insert({'firstname': request.form['firstname'],
                          'lastname': request.form['lastname'],
                          'username' : request.form['username'],
                          'email': request.form['email'],
                          'password': hashpass})
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('user_route.login'))
        flash('Email already exists', 'danger')
    return render_template('signup.html', form=form)

@user_route.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'danger')
    return redirect(url_for('user_route.login'))

@user_route.route('/feed', methods = ['POST' , 'GET'])
def feed():
    form = feed(request.form)
    posts = mongo.db.posts
    if request.method == 'POST':
        new_post = {
            'title' : request.form['title'],
            # 'image' : request.form['image'],
            # 'author' : session['username'],
            'body' : request.form['body'],
            'time' : datetime.now()
        }
        posts.insert(new_post)
    post_list = posts.find({})
    return render_template('feed.html', form=form, posts=post_list)

class feed(Form):
    title = StringField('Title')
    body = TextField('Body')
@user_route.route('/profile', methods = ['GET', 'POST'])

# @is_logged_in
def profile():
    return render_template('profile.html')
