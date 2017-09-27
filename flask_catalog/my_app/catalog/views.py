from flask import request, jsonify, Blueprint
from my_app import app, db
from my_app.catalog.models import Product

catalog = Blueprint('catalog', __name__)

@catalog.route('/') @catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."

