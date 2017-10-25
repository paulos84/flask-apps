
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


@catalog.route('/product-create', methods=['POST',])
def create_product():
    name = request.form.get('name')
    price = request.form.get('price')
    product = Product(name, price)
    db.session.add(product)
    db.session.commit()
    return 'Product created.'


class ProductForm(FlaskForm):
    name = StringField('name')
    price = IntegerField('price')


@catalog.route('/form', methods=['GET', 'POST'])
def product_form():
    form = ProductForm()

    if form.validate_on_submit():
        return 'The username is {}. The password is {}'.format (form.username.data, form.password.data)
    return render_template('form.html', form=form)


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


@catalog.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return 'The username is {}. The password is {}'.format (form.username.data, form.password.data)
    return render_template('form.html', form=form)

