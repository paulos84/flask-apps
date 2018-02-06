from flask import Flask, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
import logging

# flask debug toolbar is plugin to jinja2 template, need to declare before app.run()

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route('/')
def hello_world():
        return redirect(url_for('fibonacci', num=50))


@app.route('/fib')
@app.route('/fib/<int:n>')
def fib(n=50):
    a,b = 0, 1
    while a<n:
        yield a
        a, b = b, a+b
    return render_template('fib.html', fib_seq=', [i for i in fib()])


if __name__ == '__main__':
    app.run()
