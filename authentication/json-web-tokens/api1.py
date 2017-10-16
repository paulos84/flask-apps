

#Authenticating an API using JSON Web Tokens

from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thesecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://localhost:5000/route?=aqsfgsgsdhf393sdf
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            #jwt.decode(my_token, 'secret_key')
            data = jwt.decode(token, app.config['SECRET_KEY'])
        # a broad exception used for this simple example
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)


@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can see this'})

@app.route('/protected')
def protected():
    return jsonify({'message': 'This is only viewable for people with token'})

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)
