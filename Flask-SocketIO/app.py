from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# the flask server is listening for a message
@socketio.on('message')
def receive_message(message):
    print ('############: {}'.format(message))
    send('This is a message from the flask app server')

if __name__ == '__main__':
    #socketio is just a wrapper around the flask app server
    socketio.run(app)


# socket.io needs to be installed on the client side
# the flask app is the server