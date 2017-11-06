from flask import Flask 
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

#mail = Mail()
#mail.init_app(app)



@app.route('/')
def index():
    msg = Message('Hello, how are you?', recipients=['@hotmail.co.uk'])
    msg.body = '<b>This is the body of the test email</b>'
    #msg.html = '<b>This is a test email</b>'
    mail.send(msg)
    return 'Message sent!'


if __name__ == '__main__':
    app.run()