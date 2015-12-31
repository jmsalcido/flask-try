from flask import render_template, flash, redirect, request, url_for, g
from flask.ext.login import login_user, logout_user, current_user
from app import app, db
from .forms import LoginForm, RegisterForm
from .models import User
import datetime


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    if g.user.is_authenticated:
        user = User.query.filter_by(username=g.user.username).first()
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
    return render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "GET" and not g.user.is_authenticated:
        return render_template('login.html', title='Sign In', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = find_user(request.form["username"])
            if user is None or not user.verify_password(request.form["password"]):
                flash("The username or password is invalid.")
                return render_template('login.html', title='Sign In', form=form)
            login_user(user, remember=form.remember_me.data)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "GET" and not g.user.is_authenticated:
        return render_template("register.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username = request.form["username"]
            password = request.form["password"]
            existing_user = User.query.filter_by(username=username).first()
            if existing_user is not None:
                flash('There is a username with the name {0}'.format(username))
                return render_template("register.html", form=form)
            user = User(username, password, request.form["email"])
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered')
            return redirect(url_for("login"))
        return render_template("register.html", form=form)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<username>', methods=['GET'])
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User with username: {0} was not found".format(username))
        return redirect(url_for('index'))
    posts = [
        {'id': 1, 'author': user, 'body': 'This is a test post #1'},
        {'id': 2, 'author': user, 'body': 'This is a test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


def find_user(username):
    return db.session.query(User).filter(User.username == username).first()
