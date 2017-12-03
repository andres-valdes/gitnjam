from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint
from passlib.hash import sha256_crypt
from models.user_model import SignupForm, LoginForm, Form
from wtforms import Form, TextField, StringField, validators, PasswordField, TextAreaField
from flask_pymongo import PyMongo
from functools import wraps
from config.database import Mongo 


from flask import Flask

app = Flask(__name__) 
app.config['MONGO_DBNAME'] = 'gitnjam'
app.config['MONGO_URI'] = 'mongodb://localhost/gitnjam'

mongo = PyMongo(app) 

user_route = Blueprint('user_route', __name__)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        if 'is_logged_in' in session:
            return f(*args, **kwargs)
        flash('Unauthorized, Please login', 'danger')
        return redirect(url_for('user_route.login'))
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
                session['username'] = login_user['username']
                session['is_logged_in'] = True
                return redirect(url_for('user_route.feed', form=form))

        flash('Invalid Password or Email combination', 'danger')
    return render_template('login.html', form=form)

@user_route.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    users = mongo.db.users
    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})
        if not existing_user:
            hashpass = sha256_crypt.encrypt(str(form.password.data))
            users.insert({
                          'email': request.form['email'],
                          'username': request.form['username'],
                          'password': hashpass})
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('user_route.login', form=form))
        flash('Email already exists', 'danger')
    return render_template('signup.html', form=form)

@user_route.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'danger')
    return redirect(url_for('user_routes.login'))

@user_route.route('/feed', methods = ['POST' , 'GET'])
@is_logged_in
def feed():
    form = Feed(request.form)
    posts = mongo.db.posts
    if request.method == 'POST' and form.validate():
        new_post = {
            'title' : request.form['title'],
            # 'image' : request.form['image'],
            'author' : session['username'],
            'body' : request.form['body'],
        }
        posts.insert(new_post)
    post_list = reversed(list(posts.find({})))
    return render_template('feed.html', form=form, posts=post_list, users=mongo.db.users)

@user_route.route('/profile', methods = ['GET', 'POST'])
@is_logged_in
def redir_profile():
    return profile(session['username'])

class Feed(Form):
    title = StringField('Project Title',  [validators.Length(min=1, max=50)])
    body = TextAreaField('Project Description',  [validators.Length(min=5, max=500)])
@user_route.route('/profile/<string:username>', methods = ['GET', 'POST'])
@is_logged_in
def profile(username):
    posts = mongo.db.posts
    post_list = reversed(list(posts.find({})))
    posts_by_user = []
    for post in post_list:
        if post['author'] == username:
            posts_by_user.append(post)
    return render_template('profile.html', posts_by_user=posts_by_user, user=mongo.db.users.find_one({'username' : username}))
