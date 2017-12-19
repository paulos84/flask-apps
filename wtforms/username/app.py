from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcsRTMUAAAAAOxdw4blz72M9dZicdy2I9WK12GD'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcsRTMUAAAAAF_ciSpCr3thgyoybOoeaRCS6fPG'


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required'),
                                                   Length(min=5, max=10, message='Must be 5-10 characters')])
    password = PasswordField('password', validators=[InputRequired('Password is required'),
                                                     AnyOf(values=['password', 'secret'], message='Invalid password')])
    recaptcha = RecaptchaField()
    

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        return 'The username is {}. The password is {}'.format(form.username.data, form.password.data)
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
