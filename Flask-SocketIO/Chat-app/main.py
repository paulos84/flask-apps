from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# listen for standard message event
# when a message comes in from someone will be sent out to everyone connnected to server
@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)





#like http routes socketio message uses decorated function



if __name__ == '__main__':
    socketio.run(app)