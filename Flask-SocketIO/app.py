from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    #socketio is just a wrapper around the flask app server
    socketio.run(app)


# socket.io needs to be installed on the client side
# the flask app is the server