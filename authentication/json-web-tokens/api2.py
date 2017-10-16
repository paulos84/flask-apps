
#Authenticating an API using flask-SQLAlchemy and JSON Web Tokens

from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)
