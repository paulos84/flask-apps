from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
        return 'you are logged in'

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)