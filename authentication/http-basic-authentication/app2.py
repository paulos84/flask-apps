
# Basic HTTP authentication for multiple routes using decorators

from flask import Flask, request, make_response
from functools import wraps

app = Flask(__name__)

#create a decorators required user to be logged in
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

@app.route('/')
def index():
    if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
        return 'you are logged in'
    #the 3rd arguments tells browser that a login is required
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/page')
@auth_required
def page():
    return 'you are on the page'


if __name__ == '__main__':
    app.run(debug=True)
