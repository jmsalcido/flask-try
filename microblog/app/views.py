from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="{0}", remember_me={1}'
              .format(form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # need to create register form.
    return render_template("index.html", title="Register")
