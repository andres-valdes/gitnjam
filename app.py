from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint
from flask_pymongo import PyMongo
from wtforms import Form, StringField, PasswordField, validators, IntegerField, DateField
from passlib.hash import sha256_crypt
from flask_socketio import SocketIO, send

from models.user_model import *

from routes.user_routes import user_route

app = Flask(__name__)
app.register_blueprint(user_route)

app.config['MONGO_DBNAME'] = 'gitnjam'
app.config['MONGO_URI'] = 'mongodb://admin:admin@ds129066.mlab.com:29066/gitnjam'
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
mongo = PyMongo(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_logged_in' in session:
            return f(*args, **kwargs)
        flash('Unauthorized, Please login', 'danger')
        return redirect(url_for('user_route.login'))
    return wrap

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('greet')
def handleGreet(greet):
    print('another event that could be ballin.....' + greet)
    return 'cool story bro'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

socketio = SocketIO(app)

@app.route('/chat', methods= ['POST', 'GET'])
def chat():
    return render_template('chat.html')

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
    app.config['SECRET_KEY'] = 'gitnjam'
    socketio.run(app, port = 2000)
    app.run(threaded=True, host="0.0.0.0", port=2000, debug=True)
