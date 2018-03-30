import sys
from flask import Flask, jsonify, request, url_for
from flask_login import LoginManager, current_user, login_required
from models import db, Puppy, User
from schemas import ma, puppy_schema, user_schema
from slugify import slugify


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///puppy.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
ma.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Set up a login manager so that when the request comes if the authorization header exists it will load the user
@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if not api_key:
        return None
    return User.query.filter_by(api_key=api_key).first()


@app.route("/whoami")
def who_am_i():
    """  Test it out:
    $ curl localhost:5000/whoami
    { "name": "anonymous")
      After creating User:
    $ curl localhost:5000/whoami -H "Authorization: abc123"
    { "name": "Gary Larry") """
    if current_user.is_authenticated:
        name = current_user.name
    else:
        name = "anonymous"
    return jsonify({"name": name})


@app.route("/profile")
@login_required
def user_profile():
    return user_schema.jsonify(current_user)

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
    return jsonify({"message": "deleted"})


@app.errorhandler(404)
def page_not_found(error):
    resp = jsonify({"error": "not found"})
    resp.status_code = 404
    return resp


@app.errorhandler(401)
def unauthorized(error):
    resp = jsonify({"error": "unauthorized"})
    resp.status_code = 401
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
