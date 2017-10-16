
# Basic HTTP authentication for a single route

from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
        return 'you are logged in'
    #the 3rd arguments tells browser that a login is required
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

#only index page requires login, i.e. /page is not protected

@app.route('/page')
def page():
    return 'you are logged in'


if __name__ == '__main__':
    app.run(debug=True)
