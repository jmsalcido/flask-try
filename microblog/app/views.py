from flask import render_template
from app import app
import datetime


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'José'}
    posts = [
        {
            'author': {'nickname': 'One'},
            'body': 'Beautiful day in Los Mochis!',
            'date': datetime.date.today()
        },
        {
            'author': {'nickname': 'Two'},
            'body': 'I hate everyone.',
            'date': datetime.date.today()
        }
    ]
    return render_template('index.html', title="Home", user=user, posts=posts)
