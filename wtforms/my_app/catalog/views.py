from flask import request, jsonify, Blueprint, render_template
from my_app import app, db
from my_app.catalog.models import Product
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, AnyOf


catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."


@catalog.route('/products')
def products():
    products = Product.query.all()
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': str(product.price)
                            }
    return jsonify(res)

# from Python console: >>>requests.post('http://127.0.0.1:5000/product-create', 
#                                       data={'name': 'iPhone 2000', 'price': '49.95'}) 
@catalog.route('/product-create', methods=['POST',])
def create_product():
    name = request.form.get('name')
    price = request.form.get('price')
    product = Product(name, price)
    db.session.add(product)
    db.session.commit()
    return 'Product created.'


class ProductForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='Product name is required')])
    price = FloatField('price')


@catalog.route('/product-entry', methods=['GET', 'POST'])
def product_entry():
    form = ProductForm()
    #if route only handles POST request then could just use form.validate()
    if form.validate_on_submit():
        name = form.data['name']
        price = form.data['price']
        product = Product(name, price)
        db.session.add(product)
        db.session.commit()
        return 'Product name entered: {}. Product price entered: {}'.format(form.name.data, form.price.data)
    return render_template('product_entry.html', form=form)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required')])
    password = PasswordField('password')


@catalog.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        return 'The username is {}. The password is {}'.format(form.username.data, form.password.data)
    return render_template('form.html', form=form)

