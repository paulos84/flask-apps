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


class UserAPI(Resource):  #The API class that handles a single user
  def __init__(self):
    #Initialize

  def get(self, id):
    #GET requests

  def put(self, id):
    #PUT requests

  def delete(self, id):
    #DELETE requests


class UserListAPI(Resource):  #The API class that handles the whole group of Users
  def __init__(self):

  def get(self):

  def post(self):


api.add_resource(UserAPI, '/api/user/<int:id>', endpoint = 'user')
api.add_resource(UserListAPI, '/api/users/', endpoint = 'users')


class CityAPI(Resource):
  def __init__(self):

  def get(self, id):

  def put(self, id):

  def delete(self, id):


class CityListAPI(Resource):
  def __init__(self):

  def get(self):

  def post(self):


api.add_resource(CityListAPI, '/api/cities/', endpoint = 'cities')
api.add_resource(CityAPI, '/api/city/<int:id>', endpoint = 'city')



if __name__ == '__main__':
    app.run(debug=True)
