from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'thesecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    country = db.Column(db.String(50))
    user = db.relationship('User', backref='owner', lazy='dynamic')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)


if __name__ == '__main__':
    app.run(debug=True)
