from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_eg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

#instantiate flask_login
login_manager = LoginManager()
#initializes the instance
login_manager.init_app(app)
#send un-logged in user to login page instead of 'Unauthorized' for protected page(s)
login_manager.login_view = 'login'
#for 'get_flashed_messages' in login.html
login_manager.login_message = 'You need to login'



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


#this function allows flask_login to connects a User instance with a user that flask_login handles
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login')
def login():
    return render_template('login.html')


# <form action="/logmein' method="POST"> within login.html redirects user to this route:
@app.route('/logmein', methods=['POST'])
def logmein():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if not user:
        return '<h1>User not found!</h1>'
    login_user(user)
    return 'You are now logged in!'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'


@app.route('/home')
@login_required
def home():
    return 'The current user is: ' + current_user.username


if __name__ == '__main__':
    app.run(debug=True)
