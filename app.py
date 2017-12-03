from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint
from flask_pymongo import PyMongo
from wtforms import Form, StringField, PasswordField, validators, IntegerField, DateField
from passlib.hash import sha256_crypt

from models.user_model import *

from routes.user_routes import user_route

app = Flask(__name__) 
app.register_blueprint(user_route)

app.config['MONGO_DBNAME'] = 'gitnjam'
app.config['MONGO_URI'] = 'mongodb://localhost/gitnjam'
mongo = PyMongo(app) 

def is_logged_in(f): 
    @wraps(f)
    def wrap(*args, **kwargs): 
        if 'is_logged_in' in session:
            return f(*args, **kwargs)
        flash('Unauthorized, Please login', 'danger')
        return redirect(url_for('user_route.login'))
    return wrap

@app.errorhandler(404)
def page_not_found(error): 
    return render_template('page_not_found.html'), 404
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'gitnjam'
    app.run(host="0.0.0.0", port=2000, debug=True)