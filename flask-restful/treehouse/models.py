import datetime

from peewee import *

db = SqliteDatabase('courses.sqlite')


class BaseClass(Model):
    class meta:
        database = db


class Course(BaseClass):
    title = CharField()
    url = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)


class Review(BaseClass):
    course = ForeignKeyField(Course, related_name='review_set')
    rating = IntegerField()
    comment = TextField(default='')
    created_at = DateTimeField(default=datetime.datetime.now)


def initialize():
    db.connect()
    db.create_tables([Course, Review], safe=True)
    db.close()
