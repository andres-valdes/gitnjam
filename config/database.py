from flask import Flask
from flask_pymongo import PyMongo

def Mongo():
    app = Flask(__name__) 
    app.config['MONGO_DBNAME'] = 'gitnjam'
    app.config['MONGO_URI'] = 'mongodb://localhost/gitnjam'
    mongo = PyMongo(app) 
    return mongo
