import sys
from flask import Flask, jsonify, request, url_for
from models import db, Puppy
from schemas import ma, puppy_schema
from slugify import slugify


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///puppy.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
ma.init_app(app)

# Marshmallow converts internal representation of a resource into an external representation which Flask can render

@app.route("/<slug>")
def get_puppy(slug):
    # Get the internal representation
    puppy = Puppy.query.filter(Puppy.slug==slug).first_or_404()
    # Transform it to an external representation
    return puppy_schema.jsonify(puppy)


@app.route("/", methods=["POST"])
def create_puppy():
    puppy, errors = puppy_schema.load(request.form)
    if errors:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

    puppy.slug = slugify(puppy.name)
    db.session.add(puppy)
    db.session.commit()

    resp = jsonify({"message": "created"})
    resp.status_code = 201
    location = url_for("get_puppy", slug=puppy.slug)
    resp.headers["Location"] = location
    return resp


@app.route("/<slug>", methods=["POST"])
def edit_puppy(slug):
    """ Editing is very similar to creating, check to see if the instance exists and if it does, Marshmallow will know
    that instead of creating a Puppy object it should update the values already found on that instance """
    puppy = Puppy.query.filter(Puppy.slug==slug).first_or_404()
    puppy, errors = puppy_schema.load(request.form, instance=puppy)
    if errors:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

    puppy.slug = slugify(puppy.name)
    db.session.add(puppy)
    db.session.commit()

    resp = jsonify({"message": "updated"})
    resp.status_code = 201
    location = url_for("get_puppy", slug=puppy.slug)
    resp.headers["Location"] = location
    return resp


@app.route("/<slug>", methods=["DELETE"])
def remove_puppy(slug):
    puppy = Puppy.query.filter(Puppy.slug==slug).first_or_404()
    db.session.delete(puppy)
    db.session.commit()
    return ({"message": "deleted"})


@app.errorhandler(404)
def page_not_found(error):
    resp = jsonify({"error": "not found"})
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    if "createdb" in sys.argv:
        with app.app_context():
            db.create_all()
        print("Database created!")

    elif "seeddb" in sys.argv:
        with app.app_context():
            p1 = Puppy(slug="rover", name="Rover",
                       image_url="http://example.com/rover.jpg")
            db.session.add(p1)
            p2 = Puppy(slug="spot", name="Spot",
                       image_url="http://example.com/spot.jpg")
            db.session.add(p2)
            db.session.commit()
        print("Database seeded!")

    else:
        app.run(debug=True)
