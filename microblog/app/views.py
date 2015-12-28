from flask import render_template, flash, redirect, request, url_for
from app import app, db
from .forms import LoginForm, RegisterForm
from .models import User
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
    if request.method == "GET":
        if form.validate_on_submit():
            flash('Login requested for form="{0}", remember_me={1}'
                  .format(form.data, str(form.remember_me.data)))
        return render_template('login.html',
                               title='Sign In',
                               form=form)
    elif request.method == "POST":
        pass
    return redirect('/index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # need to create register form.
    form = RegisterForm()
    if request.method == "GET":
        return render_template("register.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username = request.form["username"]
            password = request.form["password"]
            existing_user = db.session.query(User).filter(User.username == username).first()
            if existing_user is not None:
                flash('There is a username with the name {0}'.format(username))
                return redirect(url_for("register"))
            user = User(username, password, request.form["email"])
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered')
            # register should happen.
            return redirect(url_for("login"))
        return render_template("register.html", form=form)
    return render_template("index.html", title="Register")
