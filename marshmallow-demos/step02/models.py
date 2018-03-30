from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Puppy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # index=True allows fast lookup by slug
    slug = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128), nullable=False)

