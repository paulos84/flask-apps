from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

#flask_restless is ideal for generating APIs for db models where all you want to do is display data as it is in the db,
#or allow user to insert data into database directly without any transforming of data in between
#flask_restless easily takes care of reading and writing to database once models are set up

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))


manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Person)
manager.create_api(Pet)


if __name__ == '__main__':
    app.run()
